from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import csv

z=int(input('slow[with obtrusive ads, may encounter errors](1) / fast[without obtrusive ads](2): '))
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

# listToStr = ' '.join(map(str, s))

with open('{} links.csv'.format(' '.join(map(str,y.split('/')[-1].split('-')))),'w') as f:
    write=csv.writer(f)
    for j,i in enumerate(l):
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
        write.writerow([l[j][-1:-11:-1],b])

print('\nOMEDETO !!')
