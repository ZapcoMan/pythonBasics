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

        # 绑定鼠标滚轮事件到函数on_mousewheel
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)

        # 创建一个静态位图控件，用于显示图片
        self.image = wx.StaticBitmap(self.panel, -1, self.bmps[0])

        # 将静态位图控件添加到布局管理器中，并设置其在面板中所占的比例以及对齐方式
        vbox.Add(self.image, proportion=3, flag=wx.CENTER)

        # 为面板设置布局管理器
        self.panel.SetSizer(vbox)

    # 鼠标滚轮滚动事件的处理函数
    def on_mousewheel(self, event):
        # 如果是超前移动 显示第一张图片
        if event.GetWheelRotation() > 0:
            print('鼠标滚轮向前移动了')
            self.image.SetBitmap(self.bmps[0])
        # 如果是后退移动 显示第二张图片
        else:
            print('鼠标滚轮向后移动了')
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
