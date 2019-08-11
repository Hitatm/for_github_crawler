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

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from login_github import auth_search,get_userinfo

import concurrent
from concurrent.futures import ThreadPoolExecutor

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
# e_keyword.set("人工智能")



def append_write_to_csvfile(filename,line,append):
	if os.path.exists(filename) and append:
		with open(filename,'a+',encoding='utf-8-sig',newline='') as csvfile:
			output=csv.writer(csvfile,dialect='excel')
			output.writerow(line)
	else:
		with open(filename,'w',encoding='utf-8-sig',newline='') as csvfile:
			output=csv.writer(csvfile,dialect='excel')
			output.writerow(line)
def time_to_nomaltime(time):
	pos_T=time.find("T")
	return str(time[:pos_T]+" "+time[pos_T+1:-1])

def search_fn(url):
	repo_dict=auth_search(url)
	if repo_dict != None and "items" in repo_dict:
		return repo_dict["items"]
	else:
		return None




def search_repositories(url_list):
	global progress_bar
	dict_list = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
		future_to_url = {executor.submit(search_fn, url): url for url in url_list}
		for future in concurrent.futures.as_completed(future_to_url):
			url = future_to_url[future]
			try:
				data = future.result()
				dict_list.append(data)

			except Exception as exc:
				time.sleep(1)
				continue
				# print('%r generated an exception: %s' % (url, exc))
			else:
				print('%r page is %d bytes' % (url, len(data)))
			progress_bar.step(1)
			win.update()
	return dict_list

def concurrent_get_user_info(user_list):
	user_dict_list = {}
	with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
		future_to_user = {executor.submit(get_userinfo, user): user for user in user_list}
		for future in concurrent.futures.as_completed(future_to_user):
			user = future_to_user[future]
			try:
				data = future.result()
				user_dict_list[user] = data
				progress_bar.step(1)
				win.update()
			except Exception as exc:
				time.sleep(1)
				continue
				# print('%r generated an exception: %s' % (user, exc))
			# else:
				# print('%r page is %s bytes' % (user, str(data)))
	return user_dict_list

def get_final_result(dict_list):
	global filename
	user_info_dict = {}
	user_set = set()
	for repo_dict in dict_list:
		if repo_dict != None:
			for item in repo_dict:
				username = str(item["owner"]["login"])
				user_set.add(username)
	progress_bar['maximum'] = progress_bar['value'] + len(user_set)
	user_info_dict = concurrent_get_user_info(user_set)
	# progress_bar['value']=0
	# return True
	for repo_dict in dict_list:
		if repo_dict != None:
			for item in repo_dict:
				username = str(item["owner"]["login"])
				if username not in user_set:
					continue

				user_set.discard(username)
				github_url  =  str(item["owner"]["html_url"])
				description = str(item["description"])
				update_time = str(time_to_nomaltime(item["updated_at"]))
				home_page = str(item["homepage"])
				email,blog,name,location = user_info_dict[username]
				lists = [name,email,location,blog,github_url,update_time,home_page,description]
				append_write_to_csvfile(filename+".csv",lists,True)
				# print(lists)
	return True

def get_repositories_url(keyword,start,end):
	global filename
	print(keyword)
	repo_urls = []
	filename = keyword
	url_keyword=urllib.parse.quote(keyword)
	search_header="https://api.github.com/search/repositories?"+"q="+url_keyword+"+&sort=stars&order=desc&page="
	write_header = ["name","email","location","blog","Github","更新时间","个人主页","项目描述"]
	append_write_to_csvfile(filename+".csv",write_header,False)
	for page in range(int(start),int(end)):
		search_url = search_header+str(page)
		repo_urls.append(search_url)
	return repo_urls

def get_keyword():
	keyword = str(e_keyword.get())
	# print(keyword)
	start=0
	end=15
	pages=end-start
	if len(keyword)==0:
		messagebox.showinfo(title='输入内容为空', message=keyword)
	else:
		progress_bar['value']=0
		progress_bar['maximum'] = pages * 25
		# print(progress_bar['value'])
		repo_urls = get_repositories_url(keyword,start,end)
		repo_dicts = search_repositories(repo_urls)
		get_final_result(repo_dicts)

		print("Done")


if __name__ == '__main__':
	# entry_keyword = ttk.Entry(win,textvariable = e_keyword,show = "@")
	line_search=Frame(win)
	line_search.pack()

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
