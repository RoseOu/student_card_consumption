#校园卡消费

1.先写个但脚本测试一下
     + 搭建数据库，用pymysql库
     > describe student_card
     +-------------------+------------------+------+-----+---------+----------------+
     | Field             | Type             | Null | Key | Default | Extra          |
     +-------------------+------------------+------+-----+---------+----------------+
     | id                | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
     | userId            | int(10) unsigned | NO   |     | NULL    |                |
     | dealDate          | date             | NO   |     | NULL    |                |
     | orgName           | varchar(100)     | NO   |     | NULL    |                |
     | dealDateTimestamp | timestamp        | YES  |     | NULL    |                |
     | dealTime          | time(6)          | YES  |     | NULL    |                |
     | outMoney          | float unsigned   | NO   |     | NULL    |                |
     | userName          | varchar(45)      | NO   |     | NULL    |                |
     +-------------------+------------------+------+-----+---------+----------------
     搭建结果
     + 抓取所有学生的数据（这要花很长时间，处于只是测试的目的就先抓取小部分数据）
        > 抓取orgName数据并存放在orgName.txt内
        > 总结规律orgName以’华中师范大学/后勤集团/饮食中心‘和’华中师范大学/后勤集团‘
     + 存储在数据库内