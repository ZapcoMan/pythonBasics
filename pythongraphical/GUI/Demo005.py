import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Hello World", size=(300, 180),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.Centre()
        # 取消最大化按钮
        self.Maximize(False)
        #喇叭蜂鸣

        panel = wx.Panel(parent=self)
        self.statictext = wx.StaticText(parent=panel, pos=(110, 20))
        b1 = wx.Button(parent=panel, id=1, label="按钮1", pos=(100, 45))
        self.Bind(wx.EVT_BUTTON, self.on_click, b1)
        b2 = wx.Button(parent=panel, id=2, label="按钮2", pos=(100, 85))
        self.Bind(wx.EVT_BUTTON,self.on_click, b2)

    def on_click(self, event):

        if event.GetId() == 1:
            self.statictext.SetLabel("按钮1被点击")
            wx.MessageBox("这是一个消息框", "消息提示", wx.OK | wx.ICON_INFORMATION)
        elif event.GetId() == 2:
            self.statictext.SetLabel("按钮2被点击")
            wx.MessageBox("这是一个消息框", "消息提示", wx.OK | wx.ICON_INFORMATION)

class APP(wx.App):
    def OnExit(self):
        print("退出程序")
        return 0
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == '__main__':
    app = APP()
    app.MainLoop()
