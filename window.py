from tkinter import *
import tkinter as tk
import configparser
from pynput import keyboard
import pyperclip
import tools
import os
from tkinter.filedialog import askdirectory

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
window = Tk()
bg='#FFFFFF'
window.configure(bg=bg)
aa, bb, path = StringVar(), StringVar(), StringVar()
path.set(os.path.join(os.path.expanduser('~'), "Desktop"))

old = None
p_old = None
id, key = '', ''

class LoginPage(Frame):
    def __init__(self):
        super().__init__()
        self.username = StringVar()
        self.password = StringVar()
        if config.has_section('set') and config.has_option('set', 'appid') and config.has_option('set','secret_key'):
            appid = config.get('set', 'appid')
            secret_key = config.get('set', 'secret_key')
            id.set(appid)
            key.set(secret_key)
            self.username.set(appid)
            self.password.set(secret_key)
        self.pack()
        self.createForm()
        window.configure(bg='#EEEEEE')
        # self.configure(bg=bg)


    def createForm(self):

        Label(self).grid(row=0, stick=W, pady=10)
        Button(self, text="结果保存路径", command=selectPath, relief='groove').grid(row=3, column=0)
        Entry(self, textvariable=path, relief='groove', bd=0).grid(row=3, column=1)
        Label(self, text='appid: ', bd=0).grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username, bd=0).grid(row=1, column=1, stick=E)
        Label(self, text='密钥: ', bd=0).grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.password, bd=0).grid(row=2, column=1, stick=E)
        Button(self, text='完成', width=20, bd=0, bg='#ec7259', command=self.data).grid(row=4, columnspan=2, pady=20)


    def data(self):
        if config.has_section('set'):
            config.set("set", 'appid', self.username.get())
            config.set("set", 'secret_key', self.password.get())
        else:
            config.add_section('set')
            config.set("set", 'appid', self.username.get())
            config.set("set", 'secret_key', self.password.get())
        config.write(open('config.ini', 'w', encoding='utf-8'))
        self.destroy()
        window.destroy()

def selectPath():
    path_ = askdirectory()
    if path_:
        mkdir(path_)
        path.set(path_)
        if config.has_section('set'):
            config.set("set", 'path', path_)
        else:
            config.add_section('set')
            config.set("set", 'path', path_)
        config.write(open('config.ini', 'w', encoding='utf-8'))
    print(path_)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def start_settings():
    window.title('参数设置')
    page1 = LoginPage()
    width = 350
    height = 220
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2.5)
    window.geometry(alignstr)
    window.mainloop()
    return 0



def start_translate(s1, s2):
    global id, key
    id, key = s1, s2
    window.geometry("+{}+{}".format(0, 0))

    window.title("TSTK 全局翻译")
    window.wm_attributes('-topmost', 1)
    aa.set('ctrl+shift ➡ 翻译复制内容')
    bb.set('ctrl+  Q   ➡ 保存复制内容')
    f = ('黑体', 15)
    "flat, groove, raised, ridge, solid, or sunken"
    b = Button(window, text="一键复制翻译结果", font=f,  relief='groove', bg=bg, fg='red', command=callback)
    b.pack(side=TOP, padx=10, pady=5)
    lbl = Label(window, textvariable=aa, bg=bg, font=f,justify='left', cursor='cross' )
    lbl.pack(side=TOP, padx=10, pady=10)
    lbl2 = Label(window, textvariable=bb, bg=bg, font=f,justify='left', anchor = "w")
    lbl2.pack(side=TOP, padx=10, pady=5)

    window.mainloop()
    return 1

def callback():
    pyperclip.copy(bb.get()[3:])

def press():
    a = pyperclip.paste()
    a = str(a).strip('\n').replace("\r", " ").replace("\n", " ")

    global p_old, old

    if a is None:
        pass
    else:
        print(a)
        aa.set('原文：{}'.format(tools.show(a, 45)))
        if a != old:
            p_old = tools.extract_result(a, id, key)
            print(a, 1, p_old)
            old = a
        bb.set('参考：{}'.format(tools.ch_show(p_old, 25)))


def download():
    a = pyperclip.paste()
    pa = '{}\zh {}.html'.format(config['set']['path'] if config.has_option('set', 'path') else path.get(), a[:13])
    pa = pa.replace('/', '\\')
    print(pa)
    f = open(pa, 'w', encoding='utf-8')
    a = str(a).strip('\n').replace("\r", " ").replace("\n", " ")
    global p_old, old
    if a is None:
        pass
    else:
        print(a)
        aa.set('原文：{}'.format(tools.show(a, 45)))
        if a != old:
            p_old = tools.extract_result(a, id, key)
            print(a, p_old)
            old = a
        f.write(tools.html.format(a, p_old))
        bb.set('翻译结果保存到了:\n{}\n里面了'.format(pa))
        print(pa)
        os.system("explorer.exe %s" % pa)


def keyboard_listener_start():
    gh = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>': press, })
    gh.start()
    fd = keyboard.GlobalHotKeys({
        '<ctrl>+q': download, })
    fd.start()
    print('键盘监听服务启动完成')
