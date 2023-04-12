import wx
import wx.lib.buttons as buttons
import time
import ddddocr


# 继承Frame
class Button(wx.Frame):
    ID_Btn = 10000
    ID_ToggleBtn = 10001

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        # 初始化窗口UI
        self.init_ui()
        self.ocr = ddddocr.DdddOcr(beta=True, show_ad=0)

    def init_ui(self):
        # 面板
        self.panel = wx.Panel(self)
        # 截图按钮
        cut_btn = buttons.GenButton(self.panel, id=0, label="截图", size=(50, 30), pos=(20, 0))
        self.Bind(wx.EVT_BUTTON, self.screenshot, cut_btn)
        # 识别按钮
        recognition_btn = buttons.GenButton(self.panel, id=1, label="识别", size=(50, 30), pos=(100, 0))
        self.static_text = wx.StaticText(self.panel, id=wx.ID_ANY, label=f" ", pos=(5, 40))
        self.Bind(wx.EVT_BUTTON, self.recognition, recognition_btn)

        self.SetSize(400, 300)
        self.SetTitle("识别")
        # self.SetTransparent(50)
        self.Centre()
        self.Show(True)

    def screenshot(self, e):
        import screenshot
        import tkinter as tk
        import py_tool

        scale = py_tool.get_screen_scale_rate()
        py_tool.eliminate_scaling_interference()
        top = tk.Tk()
        screenshot.Screenshot(top, scale)
        top.mainloop()
        print("截图")

    def recognition(self, e):
        start = time.time()
        # 图片路径
        image = './img/test00.png'
        # 创建ocr的reader对象，识别中英文
        with open(image, 'rb') as f:
            image = f.read()

        topic = self.ocr.classification(image)
        print("识别")

        new_topic = ""
        counter = 0
        for char in topic:
            # Increment the counter for each character
            counter += 1
            # If the counter is a multiple of 15, print a newline character
            if counter % 15 == 0:
                new_topic += "\n"
            # Print the current character
            new_topic += char
        self.static_text.SetLabel(f"{new_topic}")
        self.static_text.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        # static_text = wx.StaticText(self.panel, id=wx.ID_ANY, label=f"{topic}", pos=(5, 40))
        print(f"程序运行耗时：{time.time() - start:.3f}s")

    def close(self, e):
        self.Close()


def main():
    app = wx.App(False)
    Button(None)
    app.MainLoop()


if __name__ == "__main__":
    main()
