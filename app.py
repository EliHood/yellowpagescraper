import os
import subprocess 

cw = os.getcwd()
path = '/scrape'
ourPath = cw + os.path.join(path)

if(ourPath):
    os.chdir(ourPath)
    os.system('scrapy crawl yellow')

