# 接口来源于iApp后台
import requests
import time
import webbrowser
import random
import sys
import os
from typing import Dict, List, Optional, Union


class QQ信息查询:
    def __init__(self):
        """
        初始化QQ信息查询API - 黑客风格版本
        """
        # 黑客风格颜色代码
        self.黑色 = '\033[30m'
        self.红色 = '\033[31m'
        self.绿色 = '\033[32m'
        self.黄色 = '\033[33m'
        self.蓝色 = '\033[34m'
        self.紫色 = '\033[35m'
        self.青色 = '\033[36m'
        self.白色 = '\033[37m'
        self.亮黑 = '\033[90m'
        self.亮红 = '\033[91m'
        self.亮绿 = '\033[92m'
        self.亮黄 = '\033[93m'
        self.亮蓝 = '\033[94m'
        self.亮紫 = '\033[95m'
        self.亮青 = '\033[96m'
        self.亮白 = '\033[97m'

        self.重置 = '\033[0m'
        self.粗体 = '\033[1m'
        self.下划线 = '\033[4m'
        self.闪烁 = '\033[5m'
        self.反色 = '\033[7m'

        self.基础网址 = "http://iappht.sslqq.cn/api/qqxx/"
        self.会话 = requests.Session()

        # 设置请求头，模拟浏览器行为
        self.会话.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://iappht.sslqq.cn/',
        })

    def _黑客打印(self, 文本: str, 颜色: str = None, 延迟: float = 0.03, 特效: str = None):
        """黑客风格打印 - 逐字符显示"""
        if 颜色 is None:
            颜色 = self.亮绿

        # 添加特效
        if 特效 == "闪烁":
            文本 = f"{self.闪烁}{文本}{self.重置}"
        elif 特效 == "粗体":
            文本 = f"{self.粗体}{文本}{self.重置}"
        elif 特效 == "下划线":
            文本 = f"{self.下划线}{文本}{self.重置}"
        elif 特效 == "反色":
            文本 = f"{self.反色}{文本}{self.重置}"

        # 逐字符打印效果
        for 字符 in 文本:
            print(f"{颜色}{字符}{self.重置}", end='', flush=True)
            time.sleep(延迟)
        print()  # 换行

    def _矩阵效果(self, 行数: int = 5):
        """矩阵数字雨效果"""
        字符集 = "01"
        宽度 = os.get_terminal_size().columns

        for _ in range(行数):
            行 = ''.join(random.choice(字符集) for _ in range(宽度))
            print(f"{self.亮绿}{行}{self.重置}")
            time.sleep(0.1)

    def _黑客头部(self):
        """显示黑客风格头部"""
        os.system('cls' if os.name == 'nt' else 'clear')

        # 矩阵效果
        self._矩阵效果(3)

        头部 = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  ██████  ██████   ██████  ██   ██ ██ ██████  ███████ ██████   ║
║ ██      ██    ██ ██    ██ ██  ██  ██ ██   ██ ██      ██   ██  ║
║ ██      ██    ██ ██    ██ █████   ██ ██████  █████   ██████   ║
║ ██      ██    ██ ██    ██ ██  ██  ██ ██   ██ ██      ██   ██  ║
║  ██████  ██████   ██████  ██   ██ ██ ██   ██ ███████ ██   ██  ║
║                                                                ║
║                QQ 信息查询系统 - [访问已授权]                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """

        print(f"{self.亮绿}{头部}{self.重置}")

        # 系统状态显示
        状态行 = [
            f"{self.亮青}🖥️  系统状态: {self.亮绿}在线{self.重置}",
            f"{self.亮青}🔒 安全等级: {self.亮黄}机密{self.重置}",
            f"{self.亮青}🌐 连接状态: {self.亮绿}已加密{self.重置}",
            f"{self.亮青}🎯 目标API: {self.亮白}http://iappht.sslqq.cn/api/qqxx/{self.重置}",
            f"{self.亮青}⏰ 会话开始: {self.亮白}{time.strftime('%Y-%m-%d %H:%M:%S')}{self.重置}"
        ]

        for 行 in 状态行:
            self._黑客打印(行, 延迟=0.02)

        print()

    def _加载动画(self, 消息: str, 持续时间: float = 2.0):
        """黑客风格加载动画"""
        帧 = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        结束时间 = time.time() + 持续时间

        print(f"{self.亮青}{消息}{self.重置}", end=' ')

        while time.time() < 结束时间:
            for 帧图 in 帧:
                print(f"\r{self.亮青}{消息}{self.重置} {self.亮绿}{帧图}{self.重置}", end='', flush=True)
                time.sleep(0.1)

        print(f"\r{self.亮青}{消息}{self.重置} {self.亮绿}✅{self.重置}")

    def _二进制流效果(self, 文本: str, 持续时间: float = 1.5):
        """二进制流效果显示数据"""
        二进制字符 = "01"
        原始文本 = 文本
        行列表 = 文本.split('\n')

        # 先显示二进制流效果
        开始时间 = time.time()
        while time.time() - 开始时间 < 持续时间:
            显示文本 = ""
            for 行 in 行列表:
                二进制行 = ''.join(random.choice(二进制字符) for _ in range(len(行)))
                显示文本 += 二进制行 + "\n"

            print(f"\r{self.亮绿}{显示文本}{self.重置}", end='')
            time.sleep(0.1)

        # 最后显示真实数据
        print(f"\r{self.亮青}{文本}{self.重置}")

    def _彩色文本(self, 文本: str, 颜色: str) -> str:
        """为文本添加颜色"""
        return f"{颜色}{文本}{self.重置}"

    def _成功文本(self, 文本: str) -> str:
        """成功文本 - 亮绿色"""
        return self._彩色文本(文本, self.亮绿)

    def _错误文本(self, 文本: str) -> str:
        """错误文本 - 亮红色"""
        return self._彩色文本(文本, self.亮红)

    def _警告文本(self, 文本: str) -> str:
        """警告文本 - 亮黄色"""
        return self._彩色文本(文本, self.亮黄)

    def _信息文本(self, 文本: str) -> str:
        """信息文本 - 亮青色"""
        return self._彩色文本(文本, self.亮青)

    def 查询QQ信息(self, QQ号码: Union[str, int]) -> Dict:
        """
        查询QQ号码信息 - 黑客风格版本
        
        Args:
            QQ号码: QQ号码
            
        Returns:
            包含QQ信息的字典
        """
        QQ字符串 = str(QQ号码).strip()

        # 验证QQ号码格式
        if not self._有效QQ(QQ字符串):
            self._黑客打印(f"❌ 目标验证失败: {QQ字符串}", self.亮红)
            return {
                '成功': False,
                '错误': f'无效的QQ号码格式: {QQ字符串}',
                'QQ': QQ字符串,
                'HTTP状态': None,
                '响应成功': False
            }

        # 构建完整的API URL
        API网址 = f"{self.基础网址}?qq={QQ字符串}"

        try:
            self._黑客打印(f"🌐 初始化数据流: {API网址}", self.亮青)

            # 显示连接动画
            self._加载动画("🔗 建立连接中", 1.5)

            # 发送GET请求
            响应 = self.会话.get(API网址, timeout=15)

            # 记录HTTP状态码
            HTTP状态 = 响应.status_code

            # 根据HTTP状态码显示不同颜色
            if HTTP状态 == 200:
                self._黑客打印(f"📡 数据流状态: {HTTP状态} - 连接安全", self.亮绿)
            else:
                self._黑客打印(f"📡 数据流状态: {HTTP状态} - 连接异常", self.亮红)

            # 检查HTTP状态码
            if HTTP状态 != 200:
                return {
                    '成功': False,
                    '错误': f'HTTP错误: {HTTP状态}',
                    'QQ': QQ字符串,
                    'HTTP状态': HTTP状态,
                    '响应成功': False,
                    '网址': API网址
                }

            self._黑客打印("✅ 数据流已建立 - 加密激活", self.亮绿)

            # 显示数据接收动画
            self._加载动画("📥 接收加密数据", 1.0)

            # 直接获取原始响应文本，不进行JSON解析
            原始数据 = 响应.text

            # 构建结果
            结果 = {
                '成功': True,
                'QQ': QQ字符串,
                '原始数据': 原始数据,
                'HTTP状态': HTTP状态,
                '响应成功': True,
                '网址': API网址,
                '消息': '查询成功 - 原始数据已获取'
            }

            # 检查返回的数据是否有效
            if not 原始数据 or 原始数据.strip() == "":
                结果['消息'] = '查询成功但数据流为空'
                self._黑客打印("⚠️ 数据流为空 - 无目标信息", self.亮黄)
            else:
                结果['消息'] = '查询成功 - 原始数据流已获取'
                self._黑客打印(f"📊 原始数据大小: {len(原始数据)} 字节", self.亮绿)

            return 结果

        except requests.exceptions.Timeout:
            错误消息 = '数据流超时 (15秒) - 连接丢失'
            self._黑客打印(f"❌ {错误消息}", self.亮红)
            return {
                '成功': False,
                '错误': 错误消息,
                'QQ': QQ字符串,
                'HTTP状态': None,
                '响应成功': False
            }
        except requests.exceptions.ConnectionError:
            错误消息 = '网络连接失败 - 检查安全协议'
            self._黑客打印(f"❌ {错误消息}", self.亮红)
            return {
                '成功': False,
                '错误': 错误消息,
                'QQ': QQ字符串,
                'HTTP状态': None,
                '响应成功': False
            }
        except requests.exceptions.RequestException as e:
            错误消息 = f'系统错误: {str(e)}'
            self._黑客打印(f"❌ {错误消息}", self.亮红)
            return {
                '成功': False,
                '错误': 错误消息,
                'QQ': QQ字符串,
                'HTTP状态': None,
                '响应成功': False
            }

    def _有效QQ(self, QQ: str) -> bool:
        """
        验证QQ号码格式
        
        Args:
            QQ: QQ号码字符串
            
        Returns:
            bool: 格式是否有效
        """
        # QQ号通常为5-11位数字
        if not QQ.isdigit():
            return False

        长度 = len(QQ)
        if 长度 < 5 or 长度 > 11:
            return False

        # 不能以0开头
        if QQ.startswith('0'):
            return False

        return True

    def 批量查询(self, QQ列表: List[Union[str, int]], 延迟: float = 1.0) -> List[Dict]:
        """
        批量查询多个QQ号码 - 黑客风格版本
        
        Args:
            QQ列表: QQ号码列表
            延迟: 请求间隔时间(秒)
            
        Returns:
            查询结果列表
        """
        结果列表 = []

        self._黑客打印(f"🚀 开始批量扫描: 已识别 {len(QQ列表)} 个目标", self.亮青)

        for i, QQ in enumerate(QQ列表):
            self._黑客打印(f"\n{self.粗体}🎯 扫描进度: {i + 1}/{len(QQ列表)} - 目标: {QQ}{self.重置}", self.亮白)

            结果 = self.查询QQ信息(QQ)
            结果列表.append(结果)

            # 显示本次查询结果摘要
            if 结果.get('成功'):
                状态图标 = "✅" if 结果.get('响应成功') else "⚠️"
                消息 = 结果.get('消息', '扫描完成')
                if 结果.get('响应成功'):
                    self._黑客打印(f"{状态图标} 目标扫描: {消息}", self.亮绿)
                else:
                    self._黑客打印(f"{状态图标} 目标扫描: {消息}", self.亮黄)
            else:
                self._黑客打印(f"❌ 目标扫描失败: {结果.get('错误')}", self.亮红)

            # 添加延迟，避免请求过快
            if i < len(QQ列表) - 1:  # 最后一个不需要延迟
                self._黑客打印(f"⏳ 安全冷却: {延迟}秒", self.亮青)
                time.sleep(延迟)

        return 结果列表

    def 关闭(self):
        """关闭会话"""
        self.会话.close()
        self._黑客打印("🔒 会话已终止 - 所有连接已关闭", self.亮黄)


def 打开QQ群():
    """
    打开QQ群聊 977736763 - 黑客风格版本
    """
    QQ群号 = "977736763"
    QQ群链接 = f"https://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=key&authKey=key&group_code={QQ群号}"

    亮青 = '\033[96m'
    亮黄 = '\033[93m'
    亮绿 = '\033[92m'
    亮红 = '\033[91m'
    重置 = '\033[0m'

    print(f"\n🎯 {亮青}启动通信协议: QQ群 {QQ群号}{重置}")
    print(f"{亮黄}📢 安全通道已建立 - 可手动覆盖{重置}")
    print(f"{亮绿}🔗 {QQ群链接}{重置}")

    try:
        # 尝试用默认浏览器打开QQ群
        webbrowser.open(QQ群链接)
        print(f"{亮绿}✅ 通信门户已激活{重置}")
        print(f"{亮青}👥 访问请求已发送至安全通道{重置}")
    except Exception as e:
        print(f"{亮红}❌ 门户激活失败: {e}{重置}")
        print(f"{亮黄}💡 需要手动访问 - 搜索群号: {QQ群号}{重置}")


def 显示单个结果(结果: Dict):
    """
    显示单个查询结果 - 黑客风格版本，直接显示原始数据
    """
    # 黑客风格颜色代码
    亮红 = '\033[91m'
    亮绿 = '\033[92m'
    亮黄 = '\033[93m'
    亮青 = '\033[96m'
    亮白 = '\033[97m'
    重置 = '\033[0m'
    粗体 = '\033[1m'

    def 黑客打印(文本: str, 颜色: str = 亮绿, 延迟: float = 0.01):
        """黑客风格逐字符打印"""
        for 字符 in 文本:
            print(f"{颜色}{字符}{重置}", end='', flush=True)
            time.sleep(延迟)
        print()

    def 二进制流(文本: str, 持续时间: float = 1.0):
        """二进制流效果"""
        二进制字符 = "01"
        开始时间 = time.time()
        文本长度 = len(文本)

        while time.time() - 开始时间 < 持续时间:
            二进制文本 = ''.join(random.choice(二进制字符) for _ in range(文本长度))
            print(f"\r{亮绿}{二进制文本}{重置}", end='')
            time.sleep(0.1)
        print(f"\r{亮青}{文本}{重置}")

    print("\n" + "=" * 80)
    黑客打印(f"📱 目标分析报告 - ID: {结果.get('QQ', '未知')}", 亮青, 0.005)
    print("=" * 80)

    # 显示响应状态
    黑客打印("📊 系统状态:", 亮白, 0.005)

    # HTTP状态码颜色
    HTTP状态 = 结果.get('HTTP状态', 'N/A')
    if HTTP状态 == 200:
        print(f"{亮绿}  • 数据流: {HTTP状态} - 安全{重置}")
    else:
        print(f"{亮红}  • 数据流: {HTTP状态} - 异常{重置}")

    # 响应成功状态颜色
    响应成功 = 结果.get('响应成功')
    if 响应成功:
        print(f"{亮绿}  • 解密状态: ✅ 成功{重置}")
    else:
        print(f"{亮红}  • 解密状态: ❌ 失败{重置}")

    # 查询状态颜色
    成功 = 结果.get('成功')
    if 成功:
        print(f"{亮绿}  • 任务状态: ✅ 已完成{重置}")
    else:
        print(f"{亮红}  • 任务状态: ❌ 已中止{重置}")

    if 结果.get('成功'):
        # 消息颜色
        消息 = 结果.get('消息', 'N/A')
        if '成功' in 消息:
            print(f"{亮绿}  • 情报: {消息}{重置}")
        else:
            print(f"{亮黄}  • 情报: {消息}{重置}")

        print(f"  • 访问点: {结果.get('网址')}")

        黑客打印("\n📄 原始数据流分析:", 亮白, 0.005)
        print("-" * 50)

        原始数据 = 结果.get('原始数据', '')

        if 原始数据 and 原始数据.strip():
            # 显示二进制流效果
            print(f"{亮黄}[启动数据解密序列]{重置}")
            time.sleep(1)

            # 显示原始数据，带二进制流效果
            print(f"{亮青}=== 开始加密数据流 ==={重置}")

            # 对每行数据应用二进制流效果
            行列表 = 原始数据.split('\n')
            for i, 行 in enumerate(行列表):
                if 行.strip():  # 只处理非空行
                    二进制流(f"{行}", 持续时间=0.5)
                else:
                    print()  # 空行

            print(f"{亮青}=== 结束加密数据流 ==={重置}")

            # 显示数据统计
            print(f"\n{亮绿}📊 数据流分析完成:{重置}")
            print(f"  {亮青}• 总字节数: {len(原始数据)}{重置}")
            print(f"  {亮青}• 行数: {len(行列表)}{重置}")
            print(f"  {亮青}• 数据哈希: {hash(原始数据) & 0xFFFFFFFF}{重置}")
        else:
            print(f"{亮黄}  ⚠️ 数据流为空 - 未获取到情报{重置}")

    else:
        错误消息 = 结果.get('错误', '未知系统故障')
        print(f"{亮红}\n❌ 系统警报: {错误消息}{重置}")

        # 显示原始响应（如果有）
        原始响应 = 结果.get('原始响应')
        if 原始响应:
            黑客打印("\n📝 原始数据流 (前500字节):", 亮白, 0.005)
            print(f"  {亮黄}{原始响应}{重置}")

    print("=" * 80)


def 显示批量摘要(结果列表: List[Dict]):
    """
    显示批量查询摘要 - 黑客风格版本
    """
    # 黑客风格颜色代码
    亮红 = '\033[91m'
    亮绿 = '\033[92m'
    亮黄 = '\033[93m'
    亮青 = '\033[96m'
    亮白 = '\033[97m'
    重置 = '\033[0m'
    粗体 = '\033[1m'

    def 黑客打印(文本: str, 颜色: str = 亮绿, 延迟: float = 0.01):
        """黑客风格逐字符打印"""
        for 字符 in 文本:
            print(f"{颜色}{字符}{重置}", end='', flush=True)
            time.sleep(延迟)
        print()

    print("\n" + "📊" * 30)
    黑客打印("批量扫描任务报告", 亮青, 0.005)
    print("📊" * 30)

    总数 = len(结果列表)
    成功数 = sum(1 for r in 结果列表 if r.get('成功'))
    HTTP成功数 = sum(1 for r in 结果列表 if r.get('HTTP状态') == 200)
    响应成功数 = sum(1 for r in 结果列表 if r.get('响应成功'))
    失败数 = 总数 - 成功数

    黑客打印("📈 任务统计:", 亮白, 0.005)
    print(f"  • 总目标数: {亮白}{总数}{重置}")

    # 成功查询颜色
    if 成功数 > 0:
        print(f"  • {亮绿}✅ 成功获取: {成功数}{重置}")
    else:
        print(f"  • ✅ 成功获取: {成功数}")

    print(f"  • {亮青}🌐 安全连接: {HTTP成功数}{重置}")
    print(f"  • {亮青}📡 数据流: {响应成功数}{重置}")

    # 失败查询颜色
    if 失败数 > 0:
        print(f"  • {亮红}❌ 丢失目标: {失败数}{重置}")
    else:
        print(f"  • ❌ 丢失目标: {失败数}")

    # 显示成功率
    if 总数 > 0:
        成功率 = (成功数 / 总数) * 100
        # 成功率颜色
        if 成功率 >= 80:
            print(f"  • {亮绿}📊 任务成功率: {成功率:.1f}%{重置}")
        elif 成功率 >= 50:
            print(f"  • {亮黄}📊 任务成功率: {成功率:.1f}%{重置}")
        else:
            print(f"  • {亮红}📊 任务成功率: {成功率:.1f}%{重置}")

    # 显示失败的QQ号
    if 失败数 > 0:
        黑客打印("\n❌ 失败目标:", 亮红, 0.005)
        for 结果 in 结果列表:
            if not 结果.get('成功'):
                print(f"  • {亮红}目标 {结果.get('QQ')}: {结果.get('错误')}{重置}")

    # 显示成功的QQ号
    if 成功数 > 0:
        黑客打印("\n✅ 成功目标:", 亮绿, 0.005)
        for 结果 in 结果列表:
            if 结果.get('成功'):
                状态图标 = "✅" if 结果.get('响应成功') else "⚠️"
                消息 = 结果.get('消息')
                if 结果.get('响应成功'):
                    print(f"  • {亮绿}{状态图标} 目标 {结果.get('QQ')}: {消息}{重置}")
                else:
                    print(f"  • {亮黄}{状态图标} 目标 {结果.get('QQ')}: {消息}{重置}")


def 保存结果(结果: Union[Dict, List[Dict]], 文件名: str = None):
    """
    保存结果到文件 - 黑客风格版本
    """
    亮绿 = '\033[92m'
    重置 = '\033[0m'

    if 文件名 is None:
        时间戳 = time.strftime("%Y%m%d_%H%M%S")
        文件名 = f"QQ情报数据_{时间戳}.txt"

    with open(文件名, 'w', encoding='utf-8') as 文件:
        if isinstance(结果, dict):
            # 单个结果
            文件.write(f"=== QQ情报数据 - 目标: {结果.get('QQ', '未知')} ===\n")
            文件.write(f"时间戳: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            文件.write(f"状态: {结果.get('消息', '未知')}\n")
            文件.write(f"HTTP状态: {结果.get('HTTP状态', 'N/A')}\n")
            文件.write("\n--- 原始数据流 ---\n")
            文件.write(结果.get('原始数据', '无数据'))
            文件.write("\n--- 数据流结束 ---\n")
        else:
            # 批量结果
            文件.write(f"=== 批量QQ情报报告 ===\n")
            文件.write(f"时间戳: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            文件.write(f"总目标数: {len(结果)}\n")
            文件.write(f"成功: {sum(1 for r in 结果 if r.get('成功'))}\n")
            文件.write(f"失败: {sum(1 for r in 结果 if not r.get('成功'))}\n\n")

            for i, 单个结果 in enumerate(结果):
                文件.write(f"\n--- 目标 {i + 1}: {单个结果.get('QQ', '未知')} ---\n")
                文件.write(f"状态: {单个结果.get('消息', '未知')}\n")
                文件.write(f"HTTP状态: {单个结果.get('HTTP状态', 'N/A')}\n")
                文件.write("\n原始数据:\n")
                文件.write(单个结果.get('原始数据', '无数据'))
                文件.write("\n" + "-" * 50 + "\n")

    print(f"{亮绿}💾 情报数据已存档: {文件名}{重置}")
    return 文件名


def 获取QQ输入():
    """
    获取用户输入的QQ号码 - 黑客风格版本
    """
    亮红 = '\033[91m'
    亮绿 = '\033[92m'
    亮青 = '\033[96m'
    重置 = '\033[0m'
    亮白 = '\033[97m'

    def 黑客打印(文本: str, 颜色: str = 亮绿, 延迟: float = 0.03):
        """黑客风格逐字符打印"""
        for 字符 in 文本:
            print(f"{颜色}{字符}{重置}", end='', flush=True)
            time.sleep(延迟)
        print()

    while True:
        try:
            黑客打印("\n🎯 选择操作模式:", 亮青, 0.02)
            print(f"{亮绿}1. 单目标获取{重置}")
            print(f"{亮绿}2. 多目标扫描协议{重置}")
            print(f"{亮青}3. 启动通信通道 (QQ群 977736763){重置}")
            print(f"{亮红}4. 终止会话{重置}")

            选择 = input(f"{亮白}输入命令 (1/2/3/4): {重置}").strip()

            if 选择 == '1':
                QQ输入 = input(f"{亮青}输入目标ID: {重置}").strip()
                if QQ输入:
                    return [QQ输入], 'single'
                else:
                    黑客打印("❌ 需要目标ID", 亮红, 0.02)

            elif 选择 == '2':
                QQ输入 = input(f"{亮青}输入目标列表 (逗号/空格分隔): {重置}").strip()
                if QQ输入:
                    # 分割输入
                    QQ列表 = []
                    for 项目 in QQ输入.replace(',', ' ').split():
                        QQ = 项目.strip()
                        if QQ:
                            QQ列表.append(QQ)

                    if QQ列表:
                        return QQ列表, 'batch'
                    else:
                        黑客打印("❌ 无效的目标标识符", 亮红, 0.02)
                else:
                    黑客打印("❌ 输入不能为空", 亮红, 0.02)

            elif 选择 == '3':
                打开QQ群()
                return None, 'group'

            elif 选择 == '4' or 选择.lower() in ['exit', 'quit', 'q']:
                return None, 'exit'

            else:
                黑客打印("❌ 无效命令 - 授权被拒绝", 亮红, 0.02)

        except KeyboardInterrupt:
            黑客打印("\n\n⚡ 会话被用户终止", 亮红, 0.02)
            return None, 'exit'
        except Exception as e:
            黑客打印(f"❌ 系统错误: {e}", 亮红, 0.02)


def 主程序():
    """
    主程序 - 黑客风格版本
    """
    global 亮绿, 亮青, 亮红, 亮黄, 亮白, 重置, 粗体

    # 定义全局颜色变量
    亮绿 = '\033[92m'
    亮青 = '\033[96m'
    亮红 = '\033[91m'
    亮黄 = '\033[93m'
    亮白 = '\033[97m'
    重置 = '\033[0m'
    粗体 = '\033[1m'

    查询工具 = QQ信息查询()

    try:
        # 显示黑客风格头部
        查询工具._黑客头部()

        while True:
            QQ列表, 模式 = 获取QQ输入()

            if 模式 == 'exit':
                查询工具._黑客打印("🔒 会话已终止 - 所有系统安全", 亮黄, 0.03)
                break
            elif 模式 == 'group':
                # 已经处理了QQ群跳转，继续循环
                continue

            if not QQ列表:
                continue

            if 模式 == 'single':
                # 单个查询
                QQ号码 = QQ列表[0]
                查询工具._黑客打印(f"\n🔍 启动目标获取: {QQ号码}", 亮青, 0.02)

                结果 = 查询工具.查询QQ信息(QQ号码)
                显示单个结果(结果)

                # 询问是否保存
                保存选择 = input(f"\n{亮青}💾 存档情报数据? (y/n): {重置}").strip().lower()
                if 保存选择 in ['y', 'yes', '是']:
                    保存结果(结果)

            elif 模式 == 'batch':
                # 批量查询
                查询工具._黑客打印(f"\n🔍 启动多目标扫描: {len(QQ列表)} 个目标", 亮青, 0.02)

                结果列表 = 查询工具.批量查询(QQ列表, 延迟=0.5)

                print("\n" + "=" * 60)
                显示批量摘要(结果列表)

                # 保存批量结果
                保存选择 = input(f"\n{亮青}💾 存档批量情报? (y/n): {重置}").strip().lower()
                if 保存选择 in ['y', 'yes', '是']:
                    保存结果(结果列表)

            # 询问是否继续
            继续选择 = input(f"\n{亮青}🔄 继续操作? (y/n): {重置}").strip().lower()
            if 继续选择 not in ['y', 'yes', '是', '继续']:
                查询工具._黑客打印("🔒 任务完成 - 系统正在关闭", 亮黄, 0.03)
                break

            print("\n" + "-" * 70)

    except Exception as e:
        查询工具._黑客打印(f"❌ 严重系统故障: {e}", 亮红, 0.02)
    finally:
        查询工具.关闭()


# 直接查询函数（供其他程序调用）
def 快速查询(QQ号码: Union[str, int]) -> Dict:
    """
    快速查询单个QQ号 - 黑客风格版本
    
    Args:
        QQ号码: QQ号码
        
    Returns:
        查询结果字典
    """
    查询工具 = QQ信息查询()
    try:
        return 查询工具.查询QQ信息(QQ号码)
    finally:
        查询工具.关闭()


if __name__ == "__main__":
    主程序()
