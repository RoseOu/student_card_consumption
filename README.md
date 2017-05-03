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
    "CanteenWantonDate":String,     //9月1日到现在在食堂最放肆的一顿的日期 
    "CanteenWantonCost":Float,      //9月1日到现在在食堂最放肆的一顿的消费 
    "CanteenWantonMonth":Int,        //9月1日到现在在食堂最土豪的月份 
    "CanteenWantonMonthCost":Float,       //9月1日到现在在食堂最土豪月份的消费 
    "CanteenWantonMul":Float,        //9月1日到现在在食堂最土豪月份消费是最低月份的倍数 
    
    "CanteenTotalCost":Float,       //9月1日到现在在食堂总共消费 
    "CanteenWhatMan":Int,       //9月1日到现在最高消费是什么餐，1为早餐，2为午餐，3为晚餐 
    "CanteenFavorite":String,       //9月1日到现在在食堂消费最高的窗口（最爱的窗口）
    "CanteenFavorNum":Int,          //9月1日到现在在最爱的窗口吃了几顿 
    "CanteenfavorCost":Float,       //9月1日到现在在最爱的窗口总共消费 
    
    "MarketWantonDate":String,    //9月1日到现在在超市消费最高（剁手）的日期
    "MarketWantonCost":Float,     //9月1日到现在在超市消费最高那天挥霍了几元 
    "MarketTotalNum":Int,        //9月1日到现在共计在超市刷卡几次 
    "MarketTotalCost":Float,     //9月1日到现在在超市的累计消费 
    
    "CanteenPercent":Float,  //9月1日到现在食堂消费占比 
    "MarketPercent":Float,  //9月1日到现在超市消费占比 
    "OtherPercent":Float,     //9月1日到现在其他消费占比 
    
    "DaysNum":Int,           //9月1日到现在共有多少天 
    "TotalCost":Float,            //9月1日到现在共消费XX元 
    "Over":Float,            //9月1日到现在的消费超过全校百分之几人 
    "Rank":Int,              //9月1日到现在的消费在全校排名 
} 
```
