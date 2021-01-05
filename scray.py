from bs4 import BeautifulSoup
from urllib import request
import requests

import tkinter as tk
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import os
import subprocess
import lxml
import re
import webbrowser
import tkinter.font as tkFont
import tkinter.messagebox

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def judge18():
	return 'novel18' in text.get()

def make_bs_object():
	if judge18:
		url=text.get()
		cookie={'over18':'yes'}
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"}
		response = requests.get(url=url, headers=headers, cookies=cookie)
		html=response.content
		#logger.debug('access {} ...'.format(url))
		return BeautifulSoup(html,"lxml")
	else:
		url=text.get()
		html = request.urlopen(url=url)
		#logger.debug('access {} ...'.format(url))
		return BeautifulSoup(html,"lxml")

def get_no():
	soup=make_bs_object()
	novel_no=soup.find('div',id='novel_no').get_text()
	nn=novel_no.split("/")
	return int(nn[0])

def get_max_no():
	soup=make_bs_object()
	novel_no=soup.find('div',id='novel_no').get_text()
	nn=novel_no.split("/")
	return int(nn[1])

def url_form():
	uuu=text.get().split("/")
	uuu[4]="{}"
	surl='/'.join(uuu)
	return surl

def text_set():
	soup=make_bs_object()
	whonbun=soup.find('div',id='novel_honbun').get_text()
	if hontext:
		hontext.delete(1.0,tk.END)
		hontext.insert(tk.END, whonbun)
	else:
		hontext.insert(tk.END, whonbun)

def text_set_next():
	if get_no()!=get_max_no():
		surl=url_form().format(get_no()+1)
		text.delete(0,tk.END)
		text.insert(tk.END,surl)
	text_set()
	

def text_set_previous():
	if get_no()!=1:
		surl=url_form().format(get_no()-1)
		text.delete(0,tk.END)
		text.insert(tk.END,surl)
	text_set()

def get_main_text(bs_obj):
   whonbun=bs_obj.find('div',class_='novel_view').get_text()
   return whonbun

def file_open():
	f_type = [('Text', '*.txt'), ('Markdown', '*.md')]
	ret = tk.filedialog.askopenfilename(defaultextension='txt' , filetypes=f_type )
	if ret:
		subprocess.Popen(['start',ret], shell=True)		

def file_write():
	f_type = [('Text', '*.txt'), ('Markdown', '*.md')]
	ret = tk.filedialog.asksaveasfile(defaultextension='txt' , filetypes=f_type )
	if ret :
		thonbun=get_main_text(make_bs_object())
        # ファイルを開いてdataを書き込み
		f = open(ret, "w")
		f.write(thonbun)
		f.close()

def browser_default():
	webbrowser.open(text.get())

def browser_search_narou():
	webbrowser.open("https://yomou.syosetu.com/search.php")

def browser_search_noc():
	webbrowser.open('https://noc.syosetu.com/search/search/')

def browser_search_mn():
	webbrowser.open('https://mnlt.syosetu.com/search/search/')

def fontsize_setting():
	app = tk.Tk()
	fontStyle = tkFont.Font(family="メイリオ", size=tfontStyle['size'])
	labelExample = tk.Label(app, text=tfontStyle['size'], font=fontStyle)

	def increase_label_font():
		fontsize = tfontStyle['size']
		labelExample['text'] = fontsize+1
		tfontStyle.configure(size=fontsize+1)
		fontStyle.configure(size=fontsize+1)

	def decrease_label_font():
		fontsize = tfontStyle['size']
		labelExample['text'] = fontsize-1
		tfontStyle.configure(size=fontsize-1)
		fontStyle.configure(size=fontsize-1)
    
	buttonExample2 = tk.Button(app, text="Increase", width=30,command=increase_label_font)
	buttonExample1 = tk.Button(app, text="Decrease", width=30,command=decrease_label_font)

	buttonExample1.pack(side=tk.LEFT)
	buttonExample2.pack(side=tk.LEFT)
	labelExample.pack(side=tk.RIGHT)
	app.mainloop()




# ウィンドウを作成 --- (*2)
win = tk.Tk()
win.title("小説")
win.geometry("750x325")



# 部品を作成 --- (*3)
# ラベルを作成
label = tk.Label(win, text='urlを入力してください')
label.pack()

#メニューバーを作成
menubar = tk.Menu(win)
win.config(menu=menubar)

# menubarを親としてメニューを作成と表示
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='ファイル', menu=file_menu)

file_menu.add_command(label='ファイルを開く',command=file_open)
file_menu.add_command(label='ファイルに保存',command=file_write)

browser = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='ブラウザ', menu=browser)

browser.add_command(label='ブラウザ',command=browser_default)
browser.add_command(label='なろう',command=browser_search_narou)
browser.add_command(label='ノクターン',command=browser_search_noc)
browser.add_command(label='ムーンライト',command=browser_search_mn)

setting_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='設定', menu=setting_menu)

setting_menu.add_command(label='フォントサイズ',command=fontsize_setting)

# テキストボックスを作成
text = tk.Entry(win,width=60)
text.pack()
text.insert(tk.END, 'https://novel18.syosetu.com/n1896br/1/')

Button = tk.Button(win, text=u'scray',width=10)
Button["command"] = text_set
Button.pack(padx=20, side = 'top')

nButton = tk.Button(win, text=u'previous',width=10)
nButton["command"] = text_set_previous
nButton.pack(padx=20, side = 'top')

tButton = tk.Button(win, text=u'next',width=10)
tButton["command"] = text_set_next
tButton.pack(padx=20, side = 'top')

tfontStyle = tkFont.Font(family="メイリオ", size=10)
hontext = ScrolledText(win, width=200, height=100,font=tfontStyle)
hontext.pack(side='bottom')

# ウィンドウを動かす
win.mainloop()