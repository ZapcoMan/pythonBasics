import wx
import pyautogui


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, id=wx.ID_ANY, title='Frame',
                         pos=wx.DefaultPosition, size=(300, 120))
        self.Centre()

        panel = wx.Panel(parent=self)
        # 创建垂直方向的  Box 布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='Button TG 短信轰炸接口 单击')
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)

        b1 = wx.Button(parent=panel, label='Button TG 短信轰炸接口', id=10)
        b2 = wx.Button(parent=panel, label='Button 2', id=11)
        b3 = wx.Button(parent=panel, label='printscreen', id=12)

        self.Bind(wx.EVT_BUTTON, self.on_click, id=10, id2=20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, 5)
        hbox.Add(b2, 0, wx.EXPAND | wx.BOTTOM, 5)
        hbox.Add(b3, 0, wx.EXPAND | wx.BOTTOM, 5)

        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    def on_click(self, event):
        # 模拟 按下 printScreen 键
        if event.GetId() == 12:
            pyautogui.press('printscreen')
            print('已点击 printscreen 键')

        if event.GetId() == 10:
            self.statictext.SetLabelText('按钮一单击')
        else:
            self.statictext.SetLabelText('按钮二单击')


class APP(wx.App):
    def OnExit(self):
        print('程序退出')
        return 0

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = APP()
    app.MainLoop()
