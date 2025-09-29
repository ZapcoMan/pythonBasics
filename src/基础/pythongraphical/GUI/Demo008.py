import wx
import pyautogui

# 定义图标路径常量
ICON_PATH = "powershell.ico"

# 创建窗口
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, id=wx.ID_ANY, title='MyFrame',
                         pos=wx.DefaultPosition, size=(300, 120),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.Centre()

        # 加载图标
        try:
            icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
        except Exception as e:
            print(f"加载图标失败: {e}")

        panel = wx.Panel(parent=self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='Button TG 短信轰炸接口 单击')
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)

        b1 = wx.Button(parent=panel, label='Button TG 短信轰炸接口', id=10)

        # 绑定按钮事件
        self.Bind(wx.EVT_BUTTON, self.on_click, b1)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, 5)

        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    # 按钮点击事件处理函数
    def on_click(self, event):
        try:
            if event.GetId() == 10:
                pyautogui.press('printscreen')
                print('已点击 printscreen 键')
        except Exception as e:
            print(f"模拟按键失败: {e}")


# 自定义应用程序类
class APP(wx.App):
    # 应用程序退出时调用
    def OnExit(self):
        print('程序退出')
        return 0

    # 应用程序初始化时调用
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = APP()
    app.MainLoop()
