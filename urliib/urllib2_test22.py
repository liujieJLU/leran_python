    # -*-coding:utf-8-*-

import urllib2
import urllib
import re
import thread
import time
# http://blog.csdn.net/wyf86/article/details/52608857

#-----------加载处理糗事百科--------
class Spider_Model:

    def __init__(self):
        self.page=1
        self.pages=[]
        self.enable = False
    #-------将所有段子都抠出来，添加到列表中并返回列表
    def GetPage(self,page):
        myUrl = "http://m.qiushibaike.com/hot/page/"+page
        user_agent = 'Mozilla/4.0 (compatible; MISE 5.5; Windows NT'
        headers = { 'User-Agent': user_agent}
        req = urllib2.Request(myUrl,headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        #encode作用是将unicode编码转换成其他编码的字符串
        #dencode作用是讲其他格式编码的字符串转行unicode的编码
        unicodePage = myPage.decode("utf-8")

        #----找出class="content"的div标记
        #re.S是任意匹配模式，也就是.可以匹配换行符
        # myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>',unicodePage,re.S)    
        # myItems = re.findall('<div.*?class="content">\n+<span>(.*?)</sapn>\n+</div>',unicodePage,re.S)    
        myItems = re.findall('<div.*?class="content">\n\n+<span>(.*?)</span>\n\n+</div>',unicodePage,re.S)
        # print u""+myItems
        items =[]

        # for item in myItems:
        #     #item 中第一个是div的标题，也就是时间
        #     #item 中第二个是div的内容，也就是内容 
        #     print "---------"+item+"***********"
        #     # items.append([item[0].replace("\n","")])
        return myItems

    #用于加载新段子
    def LoadPage(self):
        #如果用户未输入quit则一直运行
        while self.enable:
            #如果pages数组中的内容小于两个
            if len(self.pages)<2:
                try:
                    #获取新的页面中的段子
                    myPage = self.GetPage(str(self.page))
                    self.page +=1
                    self.pages.append(myPage)
                except :
                    print u"无法链接糗事百科！"
            else:
                time.sleep(1)
    # def ShowPgae(self,nowPage,page):
    #     for items in nowPage:
    #         print u'第%d页' % page, items[0]
    #         myInput  = raw_input()
    #         if myInput == "quit":
    #             self.enable = False
    #             break
    
    def ShowPage(self,nowPage,page):  
        i = 0  
        # print len(nowPage)  
        for i in range(0,len(nowPage)):  
            if i < len(nowPage):  
                oneStory="\n\n"+nowPage[i].replace("\n\n","").replace("<br/>","\n")+"\n\n"  
                print u'第%d页,第%d个故事' %(page,i) ,oneStory  
                i += 1  
            else:  
                break  
  
        myInput = raw_input() 
        if myInput == "quit":  
            self.enable = False

    def Start(self):
        self.enable = True
        page = self.page
        print u"正在加载中请稍后"

        #新建线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage,())

        #--------加载糗事百科---------
        while self.enable:
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage,page)
                page +=1


                #----------- 程序的入口处 -----------    
print u"""  
---------------------------------------  
   程序：糗百爬虫  
   版本：0.3  
   作者：why  
   日期：2014-06-03  
   语言：Python 2.7  
   操作：输入quit退出阅读糗事百科  
   功能：按下回车依次浏览今日的糗百热点  
---------------------------------------  
"""  
    
    
print u'请按下回车浏览今日的糗百内容：'    
raw_input(' ')
myModel = Spider_Model()    
myModel.Start()