import os
from subprocess import call



def main():
    owl = os.path.abspath('scrape')
    myOwl = '/pythonwork/bbbscrap2/scrape'
    # print(myOwl)
    # print(os.path.abspath(cwd))

    ourPath = ['scrapy','crawl', 'yellow']
    name = "yellow"
    call(["scrapy", "crawl", "{0}".format(name)], cwd=myOwl)

if __name__ == "__main__" :
    main()
