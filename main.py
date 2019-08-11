# -*- coding: utf-8 -*-
# @Author: Gxn
# @Date:   2018-04-22 15:24:09
# @Last Modified by:   Gxn
# @Last Modified time: 2019-08-04 23:17:09
from PIL import ImageTk
filename = ""

import csv
import os,sys
import requests
import json
import urllib
# from urllib import parse
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from login_github import auth_search,get_userinfo

# os.reload(sys);
# sys.setdefaultencoding("utf8")

# 创建一个主窗口
win = Tk()
# 设置标题
win.title("猎头搜索引擎")
# 设置窗口大小和位置
# 500x500 表示窗口大小
# +200+50 表示窗口距离电脑屏幕的左边缘和上边缘的距离
# win.geometry("700x500+200+50")

e_keyword = StringVar()
e_keyword.set("人工智能")
global progress_bar


def append_write_to_csvfile(filename,line,append):
	if os.path.exists(filename) and append:
		with open(filename,'a',encoding='utf-8-sig') as csvfile:
			output=csv.writer(csvfile,dialect='excel')
			output.writerow(line)
	else:
		with open(filename,'w',encoding='utf-8-sig') as csvfile:
			output=csv.writer(csvfile,dialect='excel')
			output.writerow(line)
def time_to_nomaltime(time):
	pos_T=time.find("T")
	return str(time[:pos_T]+" "+time[pos_T+1:-1])

def search_fn(search_content):
	status = True
	while status:
		try:
			# reponse=requests.get(search_content)
			# print("asdasfa",requests.utils.get_encodings_from_content(reponse))
			# reponse.encode("latin1").decode("GBK")
			repo_dict = reponse.json()
			auth_search
			return repo_dict
		except Exception as e:
			status = False
			print(e)
			continue

def search_repositories(keyword,start,end):
	global progress_bar
	print(keyword)
	filename = keyword
	url_keyword=urllib.parse.quote(keyword)
	search_header="https://api.github.com/search/repositories?"+"q="+url_keyword+"+&sort=stars&order=desc&page="
	# write_header = ["Username","Github","更新时间".encode('gbk'),"个人主页".encode('gbk'),"项目描述".encode('gbk')]
	write_header = ["name","email","location","blog","Github","更新时间".encode("utf-8"),"个人主页".encode("utf-8"),"项目描述".encode("utf-8")]
	append_write_to_csvfile(filename+".csv",write_header,False)
	count=0
	total_count=(int(end)-int(start))*30
	for page in range(int(start),int(end)):
		search_content = search_header+str(page)
		repo_dict = auth_search(search_content)

		if repo_dict != None and "items" in repo_dict:
			items = repo_dict["items"]
			for item in items:
				github_url  =  str(item["owner"]["html_url"])
				description = str(item["description"])
				update_time = str(time_to_nomaltime(item["updated_at"]))
				home_page = str(item["homepage"])
				username = str(item["owner"]["login"])
				email,blog,name,location = get_userinfo(username)
				lists = [name,email,location,blog,github_url,update_time,home_page,description]
				# print(count)
				append_write_to_csvfile(filename+".csv",lists,True)
				count += 1
				progress_bar.step(1)
				win.update()

			# print("asdfsa")

		else:
			print(repo_dict)
	return True

# def get_file():
#     global filename
#     #创建文件对话框
#     filename = tkFileDialog.askopenfilename(filetypes=[("text file", "*")])
#     var.set(filename)

def get_keyword():
	keyword = str(e_keyword.get())
	# print(keyword)
	start=0
	end=2
	pages=end-start
	if len(keyword)==0:
		messagebox.showinfo(title='输入内容为空', message=keyword)
	else:
		progress_bar['value']=pages*30
		progress_bar['maximum']=pages*30
		print(progress_bar['value'])
		search_repositories(keyword,start,end)
		print("Done")
		# filename = keyword.encode('gbk')
		# print(filename.decode('gbk'))


if __name__ == '__main__':
	# entry_keyword = ttk.Entry(win,textvariable = e_keyword,show = "@")
	line_search=Frame(win)
	line_search.pack()
	# s1=Label(line_search,text="用户名：",font=('StSong', 25))
	# s1.pack(side='left', expand=False)

	entry_keyword = Entry(line_search,textvariable = e_keyword,foreground='green',width = 40,font=('StSong', 14))
	entry_keyword.pack(side=LEFT, expand=YES,fill=BOTH)

	button1 = Button(line_search,text = "查找" ,width = 15,height = 1,command = get_keyword)
	button1.pack(side=LEFT, expand=YES,fill=BOTH)


	progress_bar=ttk.Progressbar(win, orient = 'horizontal',mode='determinate',value=0)
	progress_bar.pack(side=LEFT,expand=YES,fill=BOTH)

	#创建文本框
	# scroll = ttk.Scrollbar()
	# text = ttk.Text(win,width = 100,height = 40)
	# scroll.pack(side = ttk.RIGHT,fill = ttk.Y)
	# text.pack(side = ttk.LEFT,fill = ttk.Y)

	# 启动主窗口
	win.mainloop()
