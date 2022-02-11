import os
import time
import base64
import sys

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

import download
from multiprocessing import Process, Queue

from icon import img
from utils.log import log

try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen

log('主程序包引入完成')


class WIN(object):
    def __init__(self):

        self.loop = True

        with open("./temp.ico", "wb+") as temp:
            temp.write(base64.b64decode(img))
        log('创建临时icon文件')

        self.queue = Queue(5)
        self.root = tk.Tk()
        self.root.iconbitmap("./temp.ico")
        # os.remove("temp.ico")
        self.root.title('股市信息抓取')
        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 300
        height = 150
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        log('主窗口初始化完毕')

        lb = tk.Label(self.root, text='请输入要抓取的股票信息页数（<250)')
        lb.place(x=20, y=20)

        # 要进行爬取的页数
        self.page = tk.StringVar(value=10)

        page_enter = tk.Entry(self.root, textvariable=self.page, bd=2, justify='center', width=4)
        page_enter.place(x=235, y=20)

        self.is_save_html = tk.StringVar(value=0)

        save_html = tk.Radiobutton(self.root, text='生成HTML文件', variable=self.is_save_html, value=1)
        save_html.place(x=50, y=60)
        not_save_html = tk.Radiobutton(self.root, text='不生成HTML文件', variable=self.is_save_html, value=0)
        not_save_html.place(x=130, y=60)

        btn_quit = tk.Button(self.root, text='退出', command=self.sign_out)
        btn_quit.place(x=50, y=100)

        btn_start = tk.Button(self.root, text='开始收集数据', command=self.get)
        btn_start.place(x=200, y=100)

        log('主窗口开始运行')

        self.root.protocol("WM_DELETE_WINDOW", self.sign_out)

        self.root.mainloop()

    def sign_out(self):
        try:
            os.remove("temp.ico")
            log('删除临时icon文件')
        except Exception as e:
            print(e)
        self.root.destroy()
        self.loop = False
        log('退出 关闭主窗口')

    def get(self):
        # 获取参数值
        page_num = int(self.page.get())
        is_save = int(self.is_save_html.get())

        log('设置多进程')
        get_data = Process(target=download.master, args=(is_save, page_num, self.queue,))
        display = Process(target=get_process, args=(self.queue, page_num,))

        log('开始下载')
        get_data.start()
        log('开始更新')
        display.start()

        self.root.destroy()
        log('关闭主窗口')

        log('阻塞主程序')
        get_data.join()
        display.join()

        log('主程序继续')


def get_process(q: Queue, pages):
    log('创建进度窗口')
    root = tk.Tk()
    root.iconbitmap("./temp.ico")
    # os.remove("temp.ico")
    root.title('执行进度')
    screenwidth = root.winfo_screenwidth()  # 屏幕宽度
    screenheight = root.winfo_screenheight()  # 屏幕高度
    width = 300
    height = 100
    x = int((screenwidth - width) / 2)
    y = int((screenheight - height) / 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

    tk.Label(root, text='下载进度:', ).place(x=20, y=50)

    process = tk.StringVar(value='当前进度:')
    tk.Label(root, textvariable=process).place(x=20, y=20)
    progressbar = ttk.Progressbar(root, length=200)
    progressbar['maximum'] = pages
    progressbar.place(x=85, y=50)

    log('开始更新进度信息')
    while True:
        try:
            page = int(q.get(timeout=2))
            # print('当前进度{}/{}'.format(page, pages))
            progressbar['value'] = page
            process.set('当前进度{}/{}'.format(page, pages))
            root.update()
            time.sleep(0.02)
        except Exception as e:
            print(e)
            # print('全部保存完毕')
            break
    root.destroy()
    log('关闭进度窗口')


def main():
    loop = True
    while loop:
        log('进入主程序')
        win = WIN()
        loop = win.loop


if __name__ == '__main__':
    main()
