# coding: utf-8

import time
import json
import requests
import webbrowser
import urllib
from lxml import html


questions = []

def open_webbrowser(question):
    # data = {"wd": question}
    data = {"q": question}
    url = urllib.parse.urlencode(data)
    # webbrowser.open('https://baidu.com/s?' + url)
    webbrowser.open('http://www.google.com/search?' + url)


def open_webbrowser_count(question,choices):
    print('-- 方法2： 题目+选项搜索结果计数法 --')
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')

    counts = []
    for i in range(len(choices)):
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
        content = req.text
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
        print(choices[i] + " : " + count)


def count_base(question,choices):
    print('-- 方法3： 题目搜索结果包含选项词频计数法 --')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
    content = req.text
    #print(content)
    counts = []
    print('Question: '+question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        print(choices[i] + " : " + str(counts[i]))


def get_answer():
    resp =‘抓包接口’
    resp_dict = json.loads(resp)
    if resp_dict['msg'] == 'no data':
        return 'Waiting for question...'
    else:
        resp_dict = eval(str(resp))
        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]
        if question not in questions:
            questions.append(question)
            choices = eval(resp_dict['data']['event']['options'])
            open_webbrowser(question)
            # open_webbrowser_count(question, choices)
            # count_base(question, choices)
            time.sleep(5)
        else:
            return 'Waiting for new question...'

def get_general_number(result):
    for item in ("About", ",", "results"):
        result = result.replace(item, "")
    return result


def search_result_number(keyword, timeout=2):
    """
    Search keyword and get search number

    :param keyword:
    :param timeout:
    :return:
    """
    url = "http://www.google.com/search"
    params = {
        "q": keyword
    }


    resp = requests.get(url, params=params, timeout=timeout)
    if not resp.ok:
        print("google search error")
        return 0
    parser = html.fromstring(resp.text)
    result = parser.xpath("//div[@id='resultStats']/text()")
    if not result:
        return 0

    return int(get_general_number(result[0]))

def main():
    while True:
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(get_answer())
        time.sleep(1)


if __name__ == '__main__':
    main()
    # open_webbrowser('歌曲康定情歌 中的康定位于哪个省?')
