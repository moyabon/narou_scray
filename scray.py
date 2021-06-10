from sys import warnoptions
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
	if judge18():
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
	for tag in soup.findAll(["rt","rp"]):
		tag.decompose()
	whonbun=soup.find('div',id='novel_honbun').get_text()

	if judge18():
		wtitle=soup.find('a',class_='margin_l10r20').get_text()
	else:
		wtitle=soup.find('a',class_='margin_r20').get_text()
		
	wno=soup.find('div',id='novel_no').get_text()
	wst=soup.find('p',class_='novel_subtitle').get_text()
	if soup.find('p',class_='chapter_title'):
		wct=soup.find('p',class_='chapter_title').get_text()
		tlabel["text"]=wtitle+" "+wct+" "+wno+" "+wst
	else:
		tlabel["text"]=wtitle+" "+wno+" "+wst

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

def shortcut_des():
	app = tk.Tk()
	flabel=tk.Label(app,text='ショートカット一覧')
	flabel.pack()
	frame_content=tk.Frame(app,pady=5,padx=5,relief=tk.GROOVE,bd=2)
	clabel=tk.Label(frame_content,text='<Control-0>:フォントサイズ1増加\n<Control-9>:フォントサイズ1減少\n<Control-e>:選択範囲をwebで検索\n<Control-d>前話をスクレイピング:\n<Control-f>:次話をスクレイピング\n')
	frame_content.pack()
	clabel.pack()
	app.mainloop()



def increase_size_font():
	tfontStyle.configure(size=tfontStyle['size']+1)
	

def decrease_size_font():
	tfontStyle.configure(size=tfontStyle['size']-1)


# ウィンドウを作成 --- (*2)
win = tk.Tk()
#win.tk.call('tk', 'scaling', 1.5) 
win.title("小説")
win.geometry("800x540")


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

setting_menu.add_command(label='ショートカットキー',command=shortcut_des)


# テキストボックスを作成

text = tk.Entry(win,width=60)
text.pack()
text.insert(tk.END, 'https://ncode.syosetu.com/n0632db/15/')

#ボタンを作成
frame_top = tk.Frame(win,pady=5)
Button = tk.Button(frame_top, text=u'scray',width=10)
Button["command"] = text_set


nButton = tk.Button(frame_top, text=u'previous',width=10)
nButton["command"] = text_set_previous


tButton = tk.Button(frame_top, text=u'next',width=10)
tButton["command"] = text_set_next

frame_top.pack(fill=tk.X)

Button.pack(side = tk.LEFT,padx=5)
nButton.pack(side = tk.LEFT,padx=5)
tButton.pack(side = tk.LEFT,padx=5)



tlabel = tk.Label(frame_top, text='')
tlabel.pack()

tfontStyle = tkFont.Font(family="メイリオ", size=10)
hontext = ScrolledText(win, width=200, height=100,font=tfontStyle)
hontext.pack(side='bottom')

#key-bind setting
def increase_fontsize(event):
    increase_size_font()

def decrease_fontsize(event):
    decrease_size_font()

def explore_word(event):
	ew=text.selection_get()
	webbrowser.open("https://www.bing.com/search?q="+ew)

def textSet_next(event):
	text_set_next()

def textSet_previous(event):
	text_set_previous()

def textSet(event):
	text_set()

#key-bind
win.bind('<Control-0>',increase_fontsize)
win.bind('<Control-9>',decrease_fontsize)
win.bind('<Control-e>',explore_word)
win.bind('<Control-d>',textSet_previous)
win.bind('<Control-f>',textSet_next)
win.bind('<Return>',textSet)


# ウィンドウを動かす
win.mainloop()
