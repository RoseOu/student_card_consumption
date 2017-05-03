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

URL: /api/consume/<int:id>/

METHOD:GET

RESPONSE DATA: 
{ 
    "fangsiDate":String,     //最放肆的一顿日期 
    "fangsiCost":Float,      //最放肆的一顿消费 
    "tuhaoMonth":Int,        //最土豪的月份 
    "tuhaoCost":Float,       //最土豪月份的消费 
    "tuhaoMul":Float,        //最土豪月份消费是最低月份的倍数 
    "totalCost":Float,       //近300天内在食堂总共消费 
    "highestCost":Int,       //最高消费是那一餐，1为早餐，2为午餐，3为晚餐 
    "favorite":String,       //最爱的窗口 
    "favorNum":Int,          //在最爱的窗口吃了几顿 
    "favorCost":Float,       //在最爱的窗口总共消费 
    "duoshouDate":String,    //在超市剁手的日期 
    "duoshouCost":Float,     //挥霍了几元 
    "duoshouNum":Int,        //共计在超市刷卡几次 
    "chaoshiCost":Float,     //在超市累计消费 
    "shitangPercent":Float,  //食堂消费占比 
    "chaoshiPercent":Float,  //超市消费占比 
    "qitaPercent":Float,     //其他消费占比 
    "daysNum":300,           //近一年300天内 
    "cost":Float,            //共消费XX元 
    "over":Float,            //超过全校百分之几人 
    "rank":Int,              //全校排名 
} 
