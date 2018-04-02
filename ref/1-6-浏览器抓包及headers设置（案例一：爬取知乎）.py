import requests
import pandas as pd
import time

headers = {
    'authorization': 'Bearer 2|1:0|10:1510242384|4:z_c0|80:MS4xa25qNEFBQUFBQUFtQUFBQVlBSlZUVkRHOFZwb3VKUlhDREpZUlBxV2U1WTYwaUFwdzRHTzJBPT0=|f3bd96d41e73c6e5431b3664a15570b1fb6ebf305cb69f40f997839592533551',
    # 括号中填上你的authorization
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    # 括号中填上你的User-Agent
}

user_data = []  # 用来保存数据的list


def get_user_data(page):
    for i in range(page):
        url = 'https://www.zhihu.com/api/v4/members/wang-jason-wang/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'.format(
            i * 20)
        response = requests.get(url, headers=headers).json()['data']  # 只获取有用的data值
        user_data.extend(response)  # 把数据添加到 user_data 尾部
        print('正在爬取第%s页' % str(i + 1))
        time.sleep(1)


if __name__ == '__main__':
    get_user_data(10)
    df = pd.DataFrame.from_dict(user_data)
    df.to_csv('followers.csv')
