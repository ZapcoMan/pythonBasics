import sys

import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World', size=(300, 300), )
        self.Centre()
        panel = wx.Panel(parent=self)
        self.statictext = wx.StaticText(parent=panel, pos=(110, 20))
        b = wx.Button(parent=panel, label='第一个按钮', pos=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.on_click, b)

    def on_click(self, event):
        print(type(event))
        self.statictext.SetLabelText('Hello,world')
        self.statictext.SetForegroundColour('red')
        self.statictext.SetBackgroundColour('yellow')
class App(wx.App):
    def OnExit(self):
        print('程序退出')
        return 0

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
