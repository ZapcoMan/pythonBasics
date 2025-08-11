# V2ray搭建教程，操作简单，支持vless，vmess，socks5等协议，x-ui搭建教程v2ray服务器vps
* 搭建视频教程 [https://youtu.be/JYjRidC4kd8](https://youtu.be/JYjRidC4kd8)
1. 购买一个VPS服务器： https://www.vultr.com/?ref=8753714 最好是国外的 不过这里这个网站可以使用支付宝支付 就是有点小贵 最低也要5美元 一个月
2. 搭建工具，视频中的是一个 Java 写的 FinalShell 但是我不需要 我哪怕用终端都能操控服务器 根本不需要什么远程连接工具 远程服务器 最好是 Debain 或者 Ubuntu 
3. 更新VPS服务器
~~~shell
apt update -y && apt install -y curl && apt install -y socat
~~~
4.搭建代码： 这里主要是搭建 x-ui 来设置节点
~~~shell
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
~~~
5. 搭建完成后放行端口
~~~shell
#节点对应的端口也要放行 
iptables -I INPUT -p tcp --dport 54321 -j ACCEPT
iptables -I INPUT -p tcp --dport 443 -j ACCEPT
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
# 也可以直接关闭防火墙
# 关闭防火墙：
sudo ufw disable

# 查看防火墙状态：
sudo ufw status
~~~
6. 但是这里有个问题 我使用的是clash / clash verge 但是这里的面板 分享出来的地址却是 V2ary 的 所以需要转换一下 [转换地址：https://acl4ssr-sub.github.io/](https://acl4ssr-sub.github.io/)
7. 搭建节点可以选择 使用域名搭建 也可以直接用IP地址 [域名注册和解析教程：https://youtu.be/dkc1I4WXHOA](https://youtu.be/dkc1I4WXHOA)