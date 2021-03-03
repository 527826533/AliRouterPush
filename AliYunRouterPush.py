import datetime
import json
import re
import time

import requests
import os

# API
three_url = "https://domainapi.aliyun.com/preDelete/search.jsonp?keyWord=&excludeKeyWord=&keywordAsPrefix=false" \
              "&keywordAsSuffix=false&exKeywordAsPrefix=false&exKeywordAsSuffix=false&constitute=1204&suffix=cn%2Ccom%2Cvip" \
              "&domainType=&endDate=&regDate=&pageSize=20000&currentPage=1&bookStatus=false&reserveRmb=&sortBy" \
              "=&partnerTypes=&sortType=&_t=self&minLength=&maxLength=&minPrice=&maxPrice=&token=tdomain-aliyun-com" \
              "%3AYa5ec76ce58a362a6766e2bf031726f94&callback=jsonp "


def three(headers):
    res = requests.get(three_url, headers=headers)
    if res.status_code == 200:
        res_text = res.text.replace("jsonp(","").replace(");","")
        res_json = json.loads(res_text)
        data = res_json["data"]
        pageResult = data["pageResult"]
        datas = pageResult["data"]
        dataX = []
        for dataOne in datas:
            if None != re.match("(\\w)(\\1)(\\1)\\w", dataOne["short_name"], flags=0) or \
               None != re.match("(\\w)(\\1)(\\w)(\\3)", dataOne["short_name"], flags=0) or \
               None != re.match("(\\w)(\\1)\\w(\\1)", dataOne["short_name"], flags=0) or \
               None != re.match("(\\w)(\\w)(\\1|\\2)(\\1|\\2)", dataOne["short_name"], flags=0):
                dataX.append(dataOne)
    else:
        print("Request todayPointIncome failed!")
    return dataX



def getContent(dataXT, dataXF):
    content=""
    for dataXTOne in dataXT:
        domain_name = dataXTOne["domain_name"]
        price = dataXTOne["price"]
        content = content + "\n *  域名:" + domain_name + "\t\t\t\t\t\t\t" + "     价格:" + str(price)
    return content


# 推送通知
def sendNotification(SERVERPUSHKEY, text, desp):
    # server推送
    server_push_url = "https://sc.ftqq.com/" + SERVERPUSHKEY + ".send"
    data = time.strftime("%Y-%m-%d");
    params = {
        "text": data+" 域名情况",
        "desp": desp
    }
    res = requests.get(url=server_push_url, params=params)
    if res.status_code == 200:
        print("推送成功!")
    else:
        print("推送失败!")
    print("标题->", text)
    print("内容->\n", desp)


# 主操作
def main(SERVERPUSHKEY):
    headers = {
        "Referer": "https://wanwang.aliyun.com/domain/reserve"
    }
    dataXT = three(headers)
    con=getContent(dataXT,"")
    sendNotification(SERVERPUSHKEY, "测试测试测试", con)


# 读取配置文件
if __name__ == '__main__':
    SERVERPUSHKEY = "SCU82722T9f1c22c29fc4505b93a0ecdec1f56d745e441faa0579f"
    main(SERVERPUSHKEY)
