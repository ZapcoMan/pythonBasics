#!/bin/bash

set -e  # 出错时立即退出

source deploy.env

# 定义回滚函数列表
declare -a ROLLBACK_CMDS=()

function run_cmd() {
  echo "[执行命令] $*"
  eval "$@"
}

function rollback() {
  echo "[回滚开始]"
  # 逆序执行回滚命令
  for (( idx=${#ROLLBACK_CMDS[@]}-1 ; idx>=0 ; idx-- )) ; do
    echo "  - 回滚：${ROLLBACK_CMDS[idx]}"
    eval "${ROLLBACK_CMDS[idx]}"
  done
  echo "[回滚完成]"
}

function safe_run() {
  # 运行命令，失败时触发回滚退出
  if ! run_cmd "$1"; then
    echo "[错误] 命令失败，开始回滚"
    rollback
    exit 1
  fi
}

function install_jdk() {
  echo "安装JDK..."
  run_cmd "mkdir -p $JDK_INSTALL_DIR"
  safe_run "tar -zxvf $JDK_TAR_PATH -C $JDK_INSTALL_DIR"
  echo -e "\
JAVA_HOME=$JDK_INSTALL_DIR/jdk1.8.0_321\n\
CLASSPATH=\$JAVA_HOME/lib/\n\
PATH=\$PATH:\$JAVA_HOME/bin\n\
export PATH JAVA_HOME CLASSPATH" >> /etc/profile
  run_cmd "source /etc/profile"

  # 回滚：删除JDK目录
  ROLLBACK_CMDS+=("rm -rf $JDK_INSTALL_DIR/jdk1.8.0_321")
}

function install_mysql() {
  echo "安装MySQL..."
  safe_run "dnf install @mysql -y"
  safe_run "systemctl enable --now mysqld"
  echo "请手动执行 mysql_secure_installation 完成安全配置"

  # 回滚：卸载MySQL
  ROLLBACK_CMDS+=("dnf remove mysql* -y")
}

function install_nginx() {
  echo "安装Nginx..."
  safe_run "yum install nginx -y"
  safe_run "systemctl enable nginx"
  safe_run "systemctl start nginx"
  safe_run "firewall-cmd --permanent --zone=public --add-service=http"
  safe_run "firewall-cmd --permanent --zone=public --add-service=https"
  safe_run "firewall-cmd --reload"

  # 回滚：卸载Nginx
  ROLLBACK_CMDS+=("yum remove nginx -y")
}

function install_redis() {
  echo "安装Redis..."
  safe_run "yum install epel-release -y"
  safe_run "yum update -y"
  safe_run "yum install redis -y"
  safe_run "systemctl enable redis"
  safe_run "systemctl start redis"
  safe_run "sed -i 's/^# requirepass .*/requirepass $REDIS_PASSWORD/' /etc/redis.conf"
  safe_run "systemctl restart redis"

  # 回滚：卸载Redis
  ROLLBACK_CMDS+=("yum remove redis -y")
}

function deploy_service() {
  echo "部署服务 $SERVICE_NAME"
  local SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
  cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=$SERVICE_NAME
After=syslog.target

[Service]
Type=simple
ExecStart=$SERVICE_JDK_PATH/bin/java -jar $SERVICE_JAR_PATH --spring.profiles.active=$SERVICE_PROFILE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

  safe_run "chmod 755 $SERVICE_FILE"
  safe_run "systemctl daemon-reload"
  safe_run "systemctl enable $SERVICE_NAME"
  safe_run "systemctl start $SERVICE_NAME"

  # 回滚：停止并删除服务文件
  ROLLBACK_CMDS+=("systemctl stop $SERVICE_NAME && rm -f $SERVICE_FILE && systemctl daemon-reload")
}

function main() {
  if [ "$ENABLE_JDK" = "true" ]; then
    install_jdk
  fi

  if [ "$ENABLE_MYSQL" = "true" ]; then
    install_mysql
  fi

  if [ "$ENABLE_NGINX" = "true" ]; then
    install_nginx
  fi

  if [ "$ENABLE_REDIS" = "true" ]; then
    install_redis
  fi

  deploy_service
  echo "[部署成功]"
}

main
