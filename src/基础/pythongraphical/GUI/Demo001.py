import wx

# 创建一个wx.App实例，初始化应用程序
app = wx.App()

# 创建一个框架窗口
# 参数说明：
# - None: 表示该窗口没有父窗口
# - title: 设置窗口标题为'第一个窗口程序'
# - size: 设置窗口大小为400x200像素
# - pos: 设置窗口左上角在屏幕上的位置为(100, 100)像素
frm = wx.Frame(None, title='第一个窗口程序', size=(400, 200), pos=(100, 100))

# 显示框架窗口
frm.Show()

# 进入应用程序主循环，等待事件处理
app.MainLoop()
