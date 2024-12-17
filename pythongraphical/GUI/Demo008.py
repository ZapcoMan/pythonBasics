import wx
import pyautogui
import time


# 创建窗口
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, id=wx.ID_ANY, title='MyFrame',
                         pos=wx.DefaultPosition, size=(300, 120),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.Centre()

        # 图标的路径
        # 加载图标
        icon = wx.Icon("powershell.ico", wx.BITMAP_TYPE_ICO)

        # 设置框架的图标
        self.SetIcon(icon)

        # 等待一段时间，让操作系统加载图标
        time.sleep(1)

        panel = wx.Panel(parent=self)
        # 创建垂直方向的  Box 布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='Button 1 单击')
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)

        b1 = wx.Button(parent=panel, label='Button 1', id=10)

        self.Bind(wx.EVT_BUTTON, self.on_click, id=10, id2=20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, 5)

        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    def on_click(self, event):
        # 模拟 按下 printScreen 键
        if event.GetId() == 10:
            pyautogui.press('printscreen')
            print('已点击 printscreen 键')


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
