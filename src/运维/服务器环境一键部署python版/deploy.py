import subprocess
import sys
import yaml
import os

rollback_actions = []

def run_cmd(cmd):
    print(f"[执行命令] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[错误] {result.stderr.strip()}")
        raise Exception(f"命令执行失败: {cmd}")
    print(result.stdout.strip())

def rollback():
    print("\n[回滚开始]")
    for action in reversed(rollback_actions):
        try:
            action()
        except Exception as e:
            print(f"[回滚错误] {e}")
    print("[回滚完成]")

# 模块化安装步骤
def install_jdk(tar_path, install_dir):
    run_cmd(f"mkdir -p {install_dir}")
    run_cmd(f"tar -zxvf {tar_path} -C {install_dir}")
    rollback_actions.append(lambda: run_cmd(f"rm -rf {install_dir}"))

def install_mysql():
    run_cmd("dnf install @mysql -y")
    run_cmd("systemctl enable --now mysqld")
    rollback_actions.append(lambda: run_cmd("dnf remove mysql* -y"))

def install_nginx():
    run_cmd("yum install nginx -y")
    run_cmd("systemctl enable nginx")
    run_cmd("systemctl start nginx")
    rollback_actions.append(lambda: run_cmd("yum remove nginx -y"))

def install_redis(password):
    run_cmd("yum install epel-release -y")
    run_cmd("yum update -y")
    run_cmd("yum install redis -y")
    run_cmd("systemctl enable redis")
    run_cmd("systemctl start redis")
    run_cmd(f"sed -i 's/^# requirepass .*/requirepass {password}/' /etc/redis.conf")
    run_cmd("systemctl restart redis")
    rollback_actions.append(lambda: run_cmd("yum remove redis -y"))

def deploy_service(service_name, jdk_path, jar_path, profile):
    service_file = f"""
[Unit]
Description={service_name}
After=syslog.target

[Service]
Type=simple
ExecStart={jdk_path}/bin/java -jar {jar_path} --spring.profiles.active={profile}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_path = f"/etc/systemd/system/{service_name}.service"
    with open(service_path, "w") as f:
        f.write(service_file)
    run_cmd("systemctl daemon-reload")
    run_cmd(f"systemctl enable {service_name}")
    run_cmd(f"systemctl start {service_name}")
    rollback_actions.append(lambda: run_cmd(f"systemctl stop {service_name} && rm -f {service_path} && systemctl daemon-reload"))

def main(env):
    try:
        with open("deploy.yaml") as f:
            config = yaml.safe_load(f)
        if env not in config["environments"]:
            raise Exception(f"环境 {env} 不存在")

        env_conf = config["environments"][env]
        print(f"[部署开始] 环境: {env}")

        if env_conf.get("jdk", {}).get("enable"):
            install_jdk(env_conf["jdk"]["tar_path"], env_conf["jdk"]["install_dir"])

        if env_conf.get("mysql", {}).get("enable"):
            install_mysql()

        if env_conf.get("nginx", {}).get("enable"):
            install_nginx()

        if env_conf.get("redis", {}).get("enable"):
            install_redis(env_conf["redis"]["password"])

        for svc in env_conf.get("services", []):
            deploy_service(svc["name"], svc["jdk_path"], svc["jar_path"], svc["profile"])

        print("[部署完成]")

    except Exception as e:
        print(f"[部署失败] {e}")
        rollback()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python deploy.py [环境名]")
        sys.exit(1)
    main(sys.argv[1])
