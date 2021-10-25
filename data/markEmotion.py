import pandas as pd
import pymysql
from aip import AipNlp
# from snownlp import SnowNLP
import json
import time

def baiduAI_login():
    # 使用百度api评分
    """ 你的 APPID AK SK """
    APP_ID = '25007483'
    API_KEY = 'yyl8uyWXHBjBFox0cUZMKSXk'
    SECRET_KEY = 'vk5jxmmRd2HHCXNHDkGBbHU9I0Xo1KPP'

    baidu_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    return baidu_client


def markEmotion(data):
    emotion_sentiment = []
    emotion_positive_prob = []
    emotion_confidence = []
    emotion_negative_prob = []
    print('---------------------')
    news = data['标题']
    print('调用百度AI进行情感分析开始........')
    for i in range(0, len(news)):

        try:
            time.sleep(1)# 百度接口qps为2，防止访问过快，失败
            emotion = client.sentimentClassify(news[i])

            sentiment = emotion['items'][0]['sentiment']
            positive_prob = emotion['items'][0]['positive_prob']
            confidence = emotion['items'][0]['confidence']
            negative_prob = emotion['items'][0]['negative_prob']

            print('No {},调用百度AI进行情感分析成功！')
        except Exception as e:
            sentiment = 100
            positive_prob = 100
            confidence = 100
            negative_prob = 100
            print('No {},调用百度AI进行情感分析失败！')
            print(e)

        emotion_sentiment.append(sentiment)
        emotion_positive_prob.append(positive_prob)
        emotion_confidence.append(confidence)
        emotion_negative_prob.append(negative_prob)

    # print(emotion_sentiment)
    # print(emotion_positive_prob)

    data['emotion_sentiment'] = emotion_sentiment
    data['emotion_positive_prob'] = emotion_positive_prob
    data['emotion_confidence'] = emotion_confidence
    data['emotion_negative_prob'] = emotion_negative_prob
    print('调用百度AI进行情感分析结束!!!')
    print(data.head())
    data.to_csv('xxx.csv', encoding='utf-8')
    return data


if __name__ == '__main__':
    filename = '688001.csv'
    client = baiduAI_login()
    data = pd.read_csv(filename, encoding='utf-8')
    marked_data = markEmotion(data)
    marked_data.to_csv('mark_'+filename, encoding='utf-8')