import requests
import re
import csv
import os

if os.path.exists('yhq.csv') != True:  # 判断同目录下是否有上次导出表格，有则删除后运行
    print('------数据开始导出------')
else:
    os.remove('yhq.csv')
    print('------数据开始导出------')
url = 'http://www.airchina.com.cn/cn/lp/pcc/pcc.shtml'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.airchina.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}


r = requests.get(url, headers=headers)

html = r.text.replace('&nbsp', '')  # 清除返回数据多余字符

tr = re.findall(r'<TR[\s\S]*?\/TR>', html)  # 正则定位所有优惠券相关信息
fieldnames = ['起始地', '到达地', '舱位', '优惠力度', '优惠码', '有效期', '旅行时间']
with open('yhq.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for td in tr:
        data = re.findall(r'width=.*?>(.*?)<', td.replace('<BR>', ''))  # 清除返回数据多余字符，并遍历单条数据
        for end_city in data[1].split('、'):  # 到达城市以'、'分割后生成list遍历
            if data[2] == '全舱':  # 国际航班舱位为全舱无法与正则匹配
                f_code = [data[2]]
            else:
                f_code = re.search(r'（(.*?)）', data[2]).group(1).split('/')
            day_pass = data[6].split('；')  # 旅行时间以'；'分割生成list遍历
            for n in day_pass:
                if day_pass[-1][-1] == '）':  # 为每个限制在某周几的优惠线路旅行时间上加备注
                    if re.search(r'（(.*?)）', day_pass[-1]).group() in n:
                        n = n
                    else:
                        n = n + re.search(r'（(.*?)）', day_pass[-1]).group()
                for s in f_code:  # 遍历舱位后以CSV导出
                    print('出发：' + data[0] + '\n' +
                          '到达：' + str(end_city) + '\n' +
                          '舱位：' + s + '\n' +
                          '优惠力度:' + data[3][2:] + '\n' +
                          '优惠码:' + data[4] + '\n' +
                          '有效期:' + data[5] + '\n' +
                          '旅行时间:' + str(n) + '\n'
                          )
                    writer.writerow({'起飞城市': data[0],
                                     '到达城市': str(end_city),
                                     '舱位': s,
                                     '优惠力度': data[3][2:],
                                     '优惠码': data[4],
                                     '有效期': data[5],
                                     '旅行时间': str(n)
                                     })

print('------数据导出完成------')
