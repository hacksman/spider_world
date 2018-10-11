# spider_world

自己实现的爬虫记录，现已实现的爬虫有

1. scrapy 电影天堂爬虫
2. scrapy 站酷爬虫
3. scrapy 通用爬虫
4. 抖音视频爬虫


其中，Aburame 文件夹下实现的是通用爬虫，如果是不需要登录的全站爬虫，用它实现可以说非常简单，只需要进行简单的配置即可。实现全站爬虫的逻辑主要在页面解析和分析，非常方便

有什么问题，小伙伴们欢迎在我issues提，一起进步

该爬虫模块长期有效，后续会增加更多有趣的爬虫，如果对小伙伴们有帮助的话，请给我star鼓励，先谢过了



> python3下运行这个项目

### 如何使用抖音爬虫

```angular2html
$ git clone https://github.com/hacksman/spider_world.git
$ cd spider_world/www_douyin_com/spiders/
$ python douyin_crawl.py 
```
程序会稍等几秒，你会得到如下提示
```angular2html
$ 请输入用户的id（11为纯数字）：
```
此时，键入用户的id，即可爬取该用户所有已经发布过的视频，爬取下来的视频存储在videos目录下

你可以通过以下方式获取用户的id

<p align="center">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_1.jpeg" width="160">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_2.jpeg" width="160">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_3.jpeg" width="160">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_4.jpeg" width="160">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_5.jpeg" width="160">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_6.jpeg" width="160">
</p>
