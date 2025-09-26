import socket
import time

def test_telnet_honeypot():
    """
    测试Telnet蜜罐连接功能
    该函数模拟一个Telnet客户端，连接到本地运行的Telnet蜜罐，
    执行登录流程并发送一些基本命令来测试蜜罐是否正常工作
    """
    try:
        # 创建socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 2323))

        # 接收初始banner
        banner = sock.recv(1024)
        print("Received banner:", banner.decode('utf-8', errors='ignore'))

        # 发送用户名
        sock.send(b"admin\n")

        # 接收密码提示
        prompt = sock.recv(1024)
        print("Received prompt:", prompt.decode('utf-8', errors='ignore'))

        # 发送密码
        sock.send(b"password123\n")

        # 接收登录成功消息
        success_msg = sock.recv(1024)
        print("Login response:", success_msg.decode('utf-8', errors='ignore'))

        # 接收命令提示符
        cmd_prompt = sock.recv(1024)
        print("Command prompt:", cmd_prompt.decode('utf-8', errors='ignore'))

        # 发送命令
        sock.send(b"whoami\n")

        # 接收命令响应
        cmd_response = sock.recv(1024)
        print("Command response:", cmd_response.decode('utf-8', errors='ignore'))

        # 接收新的命令提示符
        new_prompt = sock.recv(1024)
        print("New prompt:", new_prompt.decode('utf-8', errors='ignore'))

        # 发送退出命令
        sock.send(b"exit\n")

        # 接收退出消息
        exit_msg = sock.recv(1024)
        print("Exit response:", exit_msg.decode('utf-8', errors='ignore'))

        sock.close()
        print("Test completed successfully!")

    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    """
    程序主入口，执行Telnet蜜罐测试
    """
    test_telnet_honeypot()
