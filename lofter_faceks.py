# -*- coding: utf-8 -*-  
""" 
Crawling pictures by selenium and urllib 
url: http://pic.yxdown.com/list/0_0_1.html 
Created on 2015-10-02 @author: Eastmount CSDN  
"""    
    
import time            
import re            
import os    
import sys  
import urllib  
import shutil  
import datetime  
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains    
    
#Open PhantomJS    
driver = webdriver.PhantomJS(executable_path="C:\Python27\Scripts\phantomjs.exe")    
#driver = webdriver.Firefox()  
wait = ui.WebDriverWait(driver,10)    
  
#Download one Picture  
def loadPicture(pic_url, pic_path):  
    pic_name = os.path.basename(pic_url) #delete path, get the filename  
    urllib.urlretrieve(pic_url, pic_path + pic_name)  
  
#Visit the picture page and get <script>(.*?)</script>  original  
def getScript(elem_url,path):  
    print elem_url  
    print path  
    ''''' 
    #Error: Message: Error Message => 'Element does not exist in cache' 
    driver.get(elem_url) 
    pic_url = driver.find_element_by_xpath("//div[@id='wrap']/div/div[2]/a") 
    print pic_url.text 
    '''  
    #By urllib to download the original pics  
    count = 1  
    html_content = urllib.urlopen(elem_url).read()  
    html_script = r'bigimgsrc="(.*?\.jpg)'
    m_script = re.findall(html_script,html_content,re.S|re.M) 
    """ 
    for script in m_script:  
        res_original = r'"original":"(.*?)"' #原图  
        m_original = re.findall(res_original,script)  
        for pic_url in m_original:  
            loadPicture(pic_url, path)  
            count = count + 1  
    else:  
        print 'Download ' + str(count) + ' Pictures'  
    """
    for pic_url in m_script:
        loadPicture(pic_url,path)
        count = count + 1
    else:
        print 'Download ' + str(count) + ' Pictures'
      
#Get the Title of the URL  
def getTitle(url,path):
    try:  
        #print key,type(key)  
        count = 0  
        print 'Function getTitle(key,url)'  
        driver.get(url)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='m-postlst box masonry']/div/div/div/div/a"))
        elem_title = driver.find_elements_by_xpath("//div[@class='m-postlst box masonry']/div/div/div/div/a")
        for title in elem_title:  
            #title.text-unicode  key-str=>unicode  
            #print key,title.text  
            elem_url = title.get_attribute("href")
            #weibu = re.findall(r'/post/.*',elem_url,re.S)
            #true_url = r'http://sexy.faceks.com' + weibu
            #true_url = "http://sexy.faceks.com" + elem_url

            count = count + 1
                #print elem_url
            getScript(elem_url,path)  #visit pages
            """
            if key in title.text:  
                #print key,title.text  
                path="E:\\Picture_DM\\"+title.text+"\\"  
                if os.path.isfile(path):  #Delete file  
                    os.remove(path)  
                elif os.path.isdir(path): #Delete dir  
                    shutil.rmtree(path,True)  
                os.makedirs(path)         #create the file directory
            """  

                  
    except Exception,e:  
        print 'Error:',e  
    finally:  
        print 'Find ' + str(count) + ' pages with key\n'  
      
#Enter Function  
def main():  
    #Create Folder  
    basePathDirectory = "E:\\Picture_PLMM"
    if not os.path.exists(basePathDirectory):  
        os.makedirs(basePathDirectory)
    path="E:\\Picture_PLMM\\"
    if os.path.isfile(path):  #Delete file
        os.remove(path)
    elif os.path.isdir(path): #Delete dir
        shutil.rmtree(path,True)
    os.makedirs(path)         #create the file directory
  
    #Input the Key for search  str=>unicode=>utf-8  
    #key = raw_input("Please input a key: ").decode(sys.stdin.encoding)  
    #print 'The key is : ' + key  
  
    #Set URL List  Sum:1-73 Pages  
    print 'Ready to start the Download!!!\n\n'  
    starttime = datetime.datetime.now() 

    num=1  
    while num<=58:
        url = 'http://sexy.faceks.com/?page='+str(num)
        print '第'+str(num)+'页','url:'+url  
        #Determine whether the title contains key  
        getTitle(url,path)
        time.sleep(2)  
        num = num + 1  
    else:  
        print 'Download Over!!!'  

    #url = r'D:\ptest/mnt.html'
    #Determine whether the title contains key  
    #getTitle(url)
    #time.sleep(2)
    #get the runtime  
    endtime = datetime.datetime.now()  
    print 'The Running time : ',(endtime - starttime).seconds  
          
main()  
