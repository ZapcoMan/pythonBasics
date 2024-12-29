import wx

# 自定义框架类，继承自wx.Frame
class MyFrame(wx.Frame):
    # 初始化方法
    def __init__(self):
        # 调用父类的初始化方法，设置窗口的父级为None，标题为"第一个 GUI 程序"，大小为400x300，位置为(100, 100)
        super().__init__(parent=None, title=" 第一个 GUI 程序", size=(400, 300), pos=(100, 100))

# 自定义应用程序类，继承自wx.App
class App(wx.App):
    # 初始化方法
    def OnInit(self):
        # 创建框架实例
        frame = MyFrame()
        # 显示框架
        frame.Show()
        # 初始化成功，返回True
        return True

    # 退出方法
    def OnExit(self):
        # 打印退出程序的消息
        print("退出程序")
        # 返回0表示正常退出
        return 0

# 主程序入口
if __name__ == '__main__':
    # 创建应用程序实例
    app = App()
    # 运行主循环
    app.MainLoop()
