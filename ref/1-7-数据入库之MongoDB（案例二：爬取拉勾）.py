import requests
from pymongo import MongoClient
import time
from fake_useragent import UserAgent

client = MongoClient()
db = client.lagou
lagou = db.bigdata  # 创建名为java集合

headers = {
    'Cookie': 'user_trace_token=20171210195058-6356f9ff-dda0-11e7-8dc4-525400f775ce; LGUID=20171210195058-6356fe14-dda0-11e7-8dc4-525400f775ce; _ga=GA1.2.2037944954.1512906660; _gid=GA1.2.1585272669.1513682022; ab_test_random_num=0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; index_location_city=%E4%B8%8A%E6%B5%B7; hasDeliver=36; LGSID=20171222112023-0c1efd07-e6c7-11e7-a4eb-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; JSESSIONID=ABAAABAAADEAAFIA9E31557E7F70602314FF28DC7D6139A; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1513830884,1513831709,1513912821,1513913767; _putrc=BB71D504DD84954D; login=true; unick=%E5%94%90%E5%BF%A0%E7%BB%B4; TG-TRACK-CODE=search_code; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1513913857; LGRID=20171222113739-759436ab-e6c9-11e7-a4f0-525400f775ce; SEARCH_ID=802b2fecfe27437582eb70c78d4d10f0',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
    # 拉勾此时要验证这个参数
}  # 填入你抓包的headers信息


def get_job_info(page, kd):  # 获取数据
    for i in range(page):
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=上海&needAddtionalResult=false&isSchoolJob=0'  # 直接请求的json
        payload = {  # 要随post发送的查询数据
            'first': 'false',
            'pn': i,
            'kd': kd,
        }

        ua = UserAgent()
        headers['User-Agent'] = ua.random  # 使用fake-Agent随机生成User-Agent，添加到headers
        response = requests.post(url, data=payload, headers=headers)  # 直接请求的json数据

        if response.status_code == 200:
            job_json = response.json()['content']['positionResult']['result']  # 解析json字典中想要的键
            lagou.insert(job_json)  # 保存数据，入mongodb
        else:
            print('Something Wrong!')

        print('正在爬取' + str(i + 1) + '页的数据...')
        time.sleep(3)


if __name__ == '__main__':
    get_job_info(31, '大数据')  # 爬取前3页的PHP职位信息
