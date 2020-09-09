#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/7 11:22
# @Author : ZhangXiaobo
# @Software: PyCharm
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options  # 用于实现无窗
from selenium.webdriver import ChromeOptions  # 用于实现规避检测

start_time = time.time()
# 无窗访问
options = Options()
options.add_argument('--headless')
options.add_argument('--disable_gpu')
# 设置下载路径
chrome_options = ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': './doi_pdf/'}
chrome_options.add_experimental_option('prefs', prefs)
# 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 打开一个无窗浏览器
chrome = webdriver.Chrome(options=options, chrome_options=chrome_options)
