#### 环境

- 语言：Python3
- 数据库：MongoDB

### 运行方式
1. 抓包获得 token(对应于access_token)、user_id(对应于uid)、secret_key 字段
2. 关注公众号：鸡仔说，后台回复cp，获取唯一的 check_code 校验码
3. 启动mongo数据库 ```mongod```
4. 启动
```
# 这里仅为演示数据，实际参数请以你实际的账户参数为准
python lanuch_cp_spider.py --secrite_key 423dabf849172d8a15342710cc3211220 --token 1576511283920896_6364131_1573704298_86dbaf32dc852651de5c8a5bfcac7bc7 --user_id 7314332 --check_code odyvBt5OiGhR72FBF2AnMnCa_Dt3
```
### 运行结果示例
```
2019-03-01 09:16:07,680 INFO yizhoucp_crawl.py get_moment_list:80 开始采集动态页
2019-03-01 09:16:08,712 INFO yizhoucp_crawl.py like_sex:141 给用户(不甜。)发布的【今天杭州有太阳！！】点赞成功
2019-03-01 09:16:10,920 INFO yizhoucp_crawl.py like_sex:141 给用户(会是你好友吗)发布的【早上好啊啊啊！！！】点赞成功
2019-03-01 09:16:15,170 INFO yizhoucp_crawl.py like_sex:141 给用户(九九)发布的【💔 
男人的嘴骗人的鬼💔 
我现在很崩溃💔 
我现在只想大哭一场💔】点赞成功
2019-03-01 09:16:16,547 INFO yizhoucp_crawl.py like_sex:141 给用户(好难)发布的【  我对你就算再好，在你眼里都认为并不重要。回首去看你以往的感情经历，反而那些玩弄你感情的人，你在以后的岁月里遇到好狗，继续吃你喜欢的东西。】点赞成功
2019-03-01 09:16:17,885 INFO yizhoucp_crawl.py like_sex:141 给用户(哈娜)发布的【☀️晴天        
                      ————周杰伦】点赞成功
2019-03-01 09:16:19,071 INFO yizhoucp_crawl.py like_sex:141 给用户(无言)发布的【哼╭(╯^╰)╮
都没有一个真心谈恋爱的小哥哥
我要沉迷学习无法自拔了……】点赞成功
2019-03-01 09:16:23,329 INFO yizhoucp_crawl.py like_sex:141 给用户(你会剥石榴么)发布的【早🤭】点赞成功
2019-03-01 09:16:25,586 INFO yizhoucp_crawl.py like_sex:141 给用户(X)发布的【奔现成功🏃
正式官宣❤】点赞成功
2019-03-01 09:16:26,587 INFO yizhoucp_crawl.py like_sex:107 过滤掉cp组
2019-03-01 09:16:29,820 INFO yizhoucp_crawl.py like_sex:141 给用户(Charon)发布的【反正你没女朋友 叫我声宝贝怎么了】点赞成功
```
