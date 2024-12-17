import time

import wx


class MyFrame(wx.Frame):
    def __init__(self):
        # 任务栏图标
        super().__init__(parent=None, title='鼠标事件处理', size=(300, 300),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        # 图标的路径
        # 加载图标
        icon = wx.Icon("powershell.ico", wx.BITMAP_TYPE_ICO)

        # 设置框架的图标
        self.SetIcon(icon)

        # 等待一段时间，让操作系统加载图标
        time.sleep(1)
        self.Centre()

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_click_up)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)

        # 监听键盘
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def on_click_down(self, event):
        print('鼠标左键按下')

    def on_click_up(self, event):
        print('鼠标左键抬起')

    def on_right_click_down(self, event):
        print('鼠标右键按下')

    def on_mouse_move(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = event.GetPosition()
            print(pos)
    def on_key_down(self,event):
        print('键盘按下')
        # 获取键盘按键
        key = event.GetKeyCode()
        if key == wx.WXK_SPACE:
            print('空格键')
            wx.MessageBox('空格键', '提示', wx.OK | wx.ICON_INFORMATION)
        # Fn 键监听
        if key == wx.WXK_F1:
            print('Fn键')

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
