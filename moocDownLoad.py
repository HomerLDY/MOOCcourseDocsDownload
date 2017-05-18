# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:10:00 2017

@author: SiqiCai
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import requests

driver = webdriver.Chrome(executable_path=r"C:\Program Files\Chrome\chromedriver.exe")
driver.implicitly_wait(10)

def loginMooc():
    driver.maximize_window()
    driver.get('http://www.icourse163.org/')
    driver.find_element_by_xpath("//span[starts-with(@class, 'm-index-person-loginBtn')]").click()
    driver.switch_to.frame(0)
    driver.find_element_by_xpath("//input[starts-with(@data-placeholder, '常用邮箱')]").clear()
    driver.find_element_by_xpath("//input[starts-with(@data-placeholder, '常用邮箱')]").send_keys("xxx@163.com")
    driver.find_element_by_xpath("//input[starts-with(@data-placeholder, '密码')]").clear()
    driver.find_element_by_xpath("//input[starts-with(@data-placeholder, '密码')]").send_keys("xxx")
    driver.find_element_by_id("dologin").click()
    driver.switch_to.default_content()
    return ""
def getUnit():
#    time.sleep(5)
    driver.find_element_by_xpath("//span[text()='我的课程']").click()
#    time.sleep(5)
    driver.find_element_by_xpath("//img[@alt='Python语言程序设计']").click()
    driver.switch_to_window(driver.window_handles[-1])
#    time.sleep(5)
    driver.find_element_by_xpath("//a[text()='课件']").click()
    driver.find_element_by_css_selector("div[class='u-learnLesson normal f-cb f-pr']>h4").click()
    
def getCourseUrl():
    inputs = driver.find_elements_by_xpath("//li[starts-with(@class, 'f-fl')]")
    titleLst = []
    titleUrl = []
    titleLsts = []
    n = 1
    for i in inputs:
        ititle = '07-0' + str(n) + i.get_attribute('title').split('：')[-1]
        titleLsts.append(ititle)
        titleLst.append(i.get_attribute('title'))
        n = n + 1
        print(ititle)
    for titleName in titleLst:
        titleNames = "//li[@title='" + titleName + "']"
        print(titleNames)
        driver.find_element_by_xpath(titleNames).click()
        time.sleep(4)
        try:
            print(driver.find_element_by_xpath("//video/source").get_attribute('src'))
            titleUrl.append(driver.find_element_by_xpath("//video/source").get_attribute('src'))
        except:
            driver.find_element_by_xpath("//a[text()='文档下载']").click()
    titleLstUrl = [titleLst, titleUrl, titleLsts]
    return titleLstUrl
    
def downloadUrl(url, fileName):
    #url = "http://v.stu.126.net/mooc-video/nos/mp4/2017/04/24/1006133412_b9b827b168dd43d69c37976e27fbd0ff_shd.mp4"
    root = "D://New folder//"
    path = root + fileName + '.mp4'#'ab.mp4'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("打印成功")
        else:
            print(" ")
    except:
        print("爬去失败")

def clickHighRP():
    actions = ActionChains(driver)
    toElement = driver.find_element_by_class_name('bbg')
    actions.move_to_element(toElement).perform()
    toElement = driver.find_element_by_xpath("//span[starts-with(@class, 'qualitybtn_text')]")
    actions.move_to_element(toElement).perform()
    driver.find_element_by_xpath("//li[text()='超高清']").click()
    
def getAllUrl():
    #killn = 1
    chapter = 0
    currentChapter = driver.find_element_by_css_selector("div[class='f-fl j-chapter'] div[class='up j-up f-thide']")
    currentChapter.click()
    ichapters = driver.find_elements_by_css_selector("div[class='f-fl j-chapter'] div[class='f-thide list']")
    for ichapter in ichapters:
        iichapters = driver.find_elements_by_css_selector("div[class='f-fl j-chapter'] div[class='f-thide list']")
        iichapters[chapter].click()
        chapter = chapter + 1
        lesson = 0
        currentLesson = driver.find_element_by_css_selector("div[class='f-fl j-lesson'] div[class='up j-up f-thide']")
        currentLesson.click()
        ilessons = driver.find_elements_by_css_selector("div[class='f-fl j-lesson'] div[class='f-thide list']")
        for ilesson in ilessons:
            iilessons = driver.find_elements_by_css_selector("div[class='f-fl j-lesson'] div[class='f-thide list']")
            iilessons[lesson].click()
            lesson = lesson + 1
            ivideos = driver.find_elements_by_css_selector("li[class^='f-fl']")#li[class^='f-fl'][title^='视频']
            video = 0
            for ivideo in ivideos:                   
                iivideos = driver.find_elements_by_css_selector("li[class^='f-fl']")
                iivideoTitle = iivideos[video].get_attribute('title')
                if video != 0:
                    iivideos[video].click()
                if iivideoTitle[:2] == '视频':
                    source = driver.find_element_by_css_selector("video>source")
                    printcontent = iivideoTitle + '===' + source.get_attribute('src')
                    print(printcontent)
                    #killn = killn + 1
                if iivideoTitle[:2] == '文档':
                    print('文档下载')
                    driver.find_element_by_css_selector("a[class^='j-downpdf downpdf']").click()
                    '''
                if iivideoTitle[:3] == '富文本':
                    RichText = driver.find_element_by_css_selector("div[class^='m-learnunitUI']>div")
                    print(RichText.text)
                    '''
                video = video + 1
                '''
                if killn > 10:
                    return
                    '''
            currentLesson = driver.find_element_by_css_selector("div[class='f-fl j-lesson'] div[class='up j-up f-thide']")
            currentLesson.click()
            
        currentChapter = driver.find_element_by_css_selector("div[class='f-fl j-chapter'] div[class='up j-up f-thide']")
        currentChapter.click()
        
    
def main():
    loginMooc()
    time.sleep(5)
    getUnit()
    clickHighRP()
    getAllUrl()
    '''
    dloadLstUrl = getCourseUrl()
    j = 0
    for i in dloadLstUrl[2]:
        downloadUrl(dloadLstUrl[1][j], i)
        j = j + 1
#    downloadUrl()
'''    
main()
