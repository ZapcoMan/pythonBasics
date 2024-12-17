import wx

# 创建一个继承自wx.Frame的类，用于实现自定义的窗口功能
class MyFrame(wx.Frame):
    # 初始化函数，设置窗口的基本属性
    def __init__(self):
        # 调用父类的初始化方法，创建一个没有父窗口，标题为'Chao009'，大小为600x500的窗口
        super().__init__(parent=None, title='静态位图展示', size=(600, 500), pos=wx.DefaultPosition)
        # 加载图片资源，创建一个包含三张图片的位图列表
        self.bmps = [wx.Bitmap('./images/1.jpg'), wx.Bitmap('./images/2.jpg'), wx.Bitmap('./images/3.jpg')]
        # 将窗口居中显示
        self.Centre()
        # 创建一个面板，作为窗口的内容区域
        self.panel = wx.Panel(parent=self)
        # 创建一个垂直方向的Box布局管理器，用于管理面板中的控件布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 创建两个按钮，并添加到面板上
        button1 = wx.Button(parent=self.panel, label='第一张图片', id=1)
        button2 = wx.Button(self.panel, label='第二张图片', id=2)

        # 绑定按钮事件处理函数，为id为1和2的按钮绑定同一个事件处理函数on_click
        self.Bind(wx.EVT_BUTTON, self.on_click, id=1, id2=2)

        # 创建一个静态位图控件，用于显示图片
        self.image = wx.StaticBitmap(self.panel, -1, self.bmps[0])

        # 将按钮和图片控件添加到布局管理器中，并设置它们的布局属性
        vbox.Add(button1, proportion=1, flag=wx.CENTER | wx.EXPAND)
        vbox.Add(button2, proportion=1, flag=wx.CENTER | wx.EXPAND)
        vbox.Add(self.image, proportion=3, flag=wx.CENTER)

        # 为面板设置布局管理器
        self.panel.SetSizer(vbox)

    # 按钮点击事件处理函数
    def on_click(self, event):
        """
        根据点击事件的ID更改图像。

        该方法通过事件对象获取事件ID，然后根据ID的不同选择相应的位图资源
        设置到图像控件中。目前支持两个ID（1和2），分别对应两个不同的位图。

        参数:
        - event: 触发的事件对象，包含事件的相关信息。

        返回值:
        无
        """
        # 当事件ID为1时，设置图像控件的位图为第一个位图
        if event.GetId() == 1:
            self.image.SetBitmap(self.bmps[0])
        # 当事件ID为2时，设置图像控件的位图为第二个位图
        if event.GetId() == 2:
            self.image.SetBitmap(self.bmps[1])



# 创建一个继承自wx.App的类，用于实现自定义的应用程序
class App(wx.App):
    # 应用程序退出时的回调函数，这里简单打印一条消息
    def OnExit(self):
        print('程序退出')
        return 0

    # 应用程序初始化时的回调函数，创建并显示窗口
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

# 程序入口点，创建应用程序实例，并运行主循环
if __name__ == '__main__':
    app = App()
    app.MainLoop()
