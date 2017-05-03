# 学生卡消费账单-后端（STDCC）

### 消费账单接口
http://console.ccnu.edu.cn/ecard/getTrans?userId=Int&days=Int&startNum=Int&num=Int 

+ userid:学生学号
+ days:查询的最近天数
+ starNum:开始查询的条数
+ num:结束查询的条数

### 学生卡号的范围
+ 13级:2013210001~2013214857
+ 14级:2014210001~2014214840
+ 15级:2015210001~2015214594
+ 16级:2016210001~2016214642

### API文档

URL: /api/consume/\<int:id\>/

METHOD:GET

RESPONSE DATA: 
```
{ 
    "fangsiDate":String,     //9月1日到现在最放肆的一顿的日期 
    "fangsiCost":Float,      //9月1日到现在最放肆的一顿消费 
    "tuhaoMonth":Int,        //9月1日到现在最土豪的月份 
    "tuhaoCost":Float,       //9月1日到现在最土豪月份的消费 
    "tuhaoMul":Float,        //9月1日到现在最土豪月份消费是最低月份的倍数 
    "totalCost":Float,       //9月1日到现在在食堂总共消费 
    "highestCost":Int,       //9月1日到现在最高消费是什么餐，1为早餐，2为午餐，3为晚餐 
    "favorite":String,       //9月1日到现在消费最高的窗口（最爱的窗口）
    "favorNum":Int,          //9月1日到现在在最爱的窗口吃了几顿 
    "favorCost":Float,       //9月1日到现在在最爱的窗口总共消费 
    "duoshouDate":String,    //9月1日到现在在超市消费最高（剁手）的日期
    "duoshouCost":Float,     //9月1日到现在在超市消费最高那天挥霍了几元 
    "duoshouNum":Int,        //9月1日到现在共计在超市刷卡几次 
    "chaoshiCost":Float,     //9月1日到现在在超市的累计消费 
    "shitangPercent":Float,  //9月1日到现在食堂消费占比 
    "chaoshiPercent":Float,  //9月1日到现在超市消费占比 
    "qitaPercent":Float,     //9月1日到现在其他消费占比 
    "daysNum":300,           //9月1日到现在共有多少天 
    "cost":Float,            //9月1日到现在共消费XX元 
    "over":Float,            //9月1日到现在的消费超过全校百分之几人 
    "rank":Int,              //9月1日到现在的消费在全校排名 
} 
```
