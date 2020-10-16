from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import csv
import wget
import os
import sys

z=int(input('slow[without obtrusive ads, may encounter errors](1) / fast[with obtrusive ads](2): '))
y=input('Give link: ')
w=input("geek mode? y/n: ")
g=['(HDP - mp4)','(360P - mp4)','(720P - mp4)','(1080P - mp4)']
print(g)
x=int(input('which do you want?(enter list index): '))

source=requests.get(y).text
soup=bs(source,'lxml')
'''https://animekisa.tv/enen-no-shouboutai-ni-no-shou-episode-11'''
l=list()

for i in list(soup.find('div',class_="infoepbox").find_all('a',class_="infovan")):
    if len(i['href'].split('.'))==1:
        l.append(i['href'])

start=int(input("enter starting"))-1
end=int(input("enter ending"))-1
episode_list=l[::-1][start:end+1]
if w=='y':
    print(episode_list)
# listToStr = ' '.join(map(str, s))

final_links=list()
name='{}'.format(' '.join(map(str,y.split('/')[-1].split('-'))))
with open('{} links.csv'.format(name),'w') as f:
    write=csv.writer(f)
    for j,i in enumerate(episode_list):
        src='https://animekisa.tv/'+i
        chop = webdriver.ChromeOptions()
        chop.add_extension('./Open link in same tab, pop-up as tab.crx')
        if z==1:
            chop.add_extension('./uBlock Origin.crx')
        # create new Chrome driver object with Chrome extension
        driver = webdriver.Chrome(options=chop)
        if z==1:
            driver.implicitly_wait(10)
        driver.get(src)
        if z==1:
            driver.implicitly_wait(10)
        if z==1:
            search_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div[7]/div")
        else:
            search_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div[8]/div")
        search_button.click()
        if z==1:
            driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[1])       
        a=driver.current_url       
        driver.close()
        if z==1:
            driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        
        sou=requests.get(a).text
        souper=bs(sou,'lxml')
        for k in souper.find_all('div', class_="dowload"):
            #get all available formats from here
            try:
                if g[x]==k.text.split('\n')[1].strip():
                    if w=='y':
                        print(k.text.split('\n')[1].strip())
                        print(k.a['href'])
                    b=k.a['href']
            except:
                pass
        write.writerow([episode_list[j][-1:-10:-1][::-1],b])
        final_links.append(b)

print('\nOMEDETO !!')

def downloader(c):
    if not os.path.exists('{}'.format(name)):
        os.makedirs('{}'.format(name))
    os.chdir('./{}'.format(name))
    for i in c:
        wget.download(i, os.getcwd())

def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  # Don't use print() as it will print in new line every time.
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

if input('download now?'):
    downloader(final_links)
