# spider_world

自己实现的爬虫记录，现已实现的爬虫有

1. scrapy 电影天堂爬虫
2. scrapy 站酷爬虫
3. scrapy 通用爬虫
4. 抖音视频爬虫


其中，Aburame 文件夹下实现的是通用爬虫，如果是不需要登录的全站爬虫，用它实现可以说非常简单，只需要进行简单的配置即可。实现全站爬虫的逻辑主要在页面解析和分析，非常方便

有什么问题，小伙伴们欢迎在我issues提，一起进步

该爬虫模块长期有效，后续会增加更多有趣的爬虫，如果对小伙伴们有帮助的话，请给我star鼓励，先谢过了


### 如何使用抖音爬虫

> python3下运行这个项目

##### step 1: 拷贝项目到本地
```angular2html
$ git clone https://github.com/hacksman/spider_world.git
$ cd spider_world/www_douyin_com/
```

##### step 2: 运行项目

**你需要关注微信公众号：鸡仔说，回复抖音，将 config.py 目录下的 token 值替换成你的 token 值**

你有两种方式运行这个项目：
①. 找到 spiders/douyin_crawl.py 文件，修改对应参数运行，然后直接运行即可
②. 找到 examples/fetch_video_test.py 文件，修改对应的 user_id，然后直接运行项目即可

__你可以通过以下方式获取用户id__

<p align="center">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_1.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_2.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_3.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_4.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_5.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_step_6.jpeg" width="140">
</p>

用户id就是图中最后一步链接user后的数字，比如此处url为```https://www.douyin.com/share/user/93515402600```，用户id就是```93515402600```

__你可以通过以下方式获取视频id__

<p align="center">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_1.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_2.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_3.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_4.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_5.jpeg" width="140">
<img src="https://raw.githubusercontent.com/hacksman/spider_world/master/pictures/douyin_video_id_6.jpeg" width="140">
</p>

视频id就是就是图中最后一步链接video后的数字，比如此处url为

```https://www.iesdouyin.com/share/video/6610679501925911815/?u_code=hjdm8k44&region=CN&mid=6610679524466101005&schema_type=1&object_id=6610679501925911815&utm_campaign=client_scan_share&app=aweme&utm_medium=ios&tt_from=scan_share&iid=45561030398&utm_source=scan_share```

视频id就是```6610679501925911815```


正常运行命令， 将会得到类似如下的log日志

```angular2html
2018-10-11 20:11:21,039 - douyin_crawl.py[line:147] INFO - download_favorite_video 正在下载视频 Gaiamount_93515402600_#8k #hdr 论现场灯光的重要性～ 
2018-10-11 20:11:27,817 - douyin_crawl.py[line:147] INFO - download_favorite_video 正在下载视频 Gaiamount_93515402600_#8k #hdr 片场那些好玩儿的事儿～比如轮椅直线加速⏩ 
2018-10-11 20:11:34,690 - douyin_crawl.py[line:147] INFO - download_favorite_video 正在下载视频 Gaiamount_93515402600_#8k #hdr 关于现场的那些事儿 
2018-10-11 20:11:40,793 - douyin_crawl.py[line:147] INFO - download_favorite_video 正在下载视频 Gaiamount_93515402600_#8k#HDR 中国首部8K HDR 影片！敬请期待～ 
``` 



### TODO LIST

* [X] 下载该用户所有视频

* [X] 下载该用户所有视频和音频

* [X] 下载单个视频

* [ ] 下载单个视频的音频

* [X] 用户的评论信息
