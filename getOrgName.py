#-*- coding:utf-8 -*-
#抓取所有的orgname名
from urllib.request import urlopen
import json
start = 2016211081
end = 2016211500
def getResponse(url):
    try:
        response = urlopen(url)
    except HTTPError as e:
        return None
    if response == 'null':
        return None
    else: 
        return response.read().decode('utf-8')

orgNames = set()
for i in range(start, end):
    url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='+str(i)+'&days=365&startNum=0&num=100'
    response = getResponse(url)
    responseJson = json.loads(response)
    print(str(i))
    try:
        for each in responseJson:
            orgNames.add(each['orgName'])
    except TypeError as e:
        print("An error occured")
        continue

with open('./orgName.txt', 'w') as f:
    for each in list(orgNames):
        f.write(each+'\n')