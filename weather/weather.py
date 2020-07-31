"""
 @Description: 用于爬取天气网近日天气信息，并发送给指定邮箱
 @Date: 2020-07-31
"""

import requests
from bs4 import BeautifulSoup
import prettytable as pt
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def get_weather_data(url):
    """
    :param url: 天气网地址
    :return:
    """
    data_list = []
    response = requests.get(url)
    html_doc = response.text
    # soup = BeautifulSoup(html_doc, 'lxml')  # 自动补全html代码，并按html代码格式返回(lxml需要c语言支持)
    soup = BeautifulSoup(html_doc, 'html.parser')  # 使用python自带的html解析器
    temperature = soup.find('div', class_='temperature').get_text()  # 获取温度信息
    current_weather = soup.find('div', class_='weather-icon-wrap').get_text()  # 当前天气情况
    data_list.append("现在的温度：%s\n现在天气情况：%s" % (temperature, current_weather))
    weather_list = soup.find_all('ul', class_='weather-columns')  # 获取近日天气情况列表
    for item in weather_list:
        data_list.append(item.get_text())
    table_data = pt.PrettyTable()  # 创建 PrettyTable 对象
    table_data.field_names = ["日期", "天气", "详情"]  # 表头数据
    for i, item in enumerate(data_list, 1):
        if i != 1:
            table_data.add_row(
                [
                    item.strip().split()[0] + item.strip().split()[1],  # 星期和日期拼接
                    item.strip().split()[2],  # 天气情况
                    item.strip().split()[3] + item.strip().split()[4]  # 详情列数据
                ]
            )
    print(table_data)
    return table_data


def send_mail(msg, receiver):
    """
    :param msg: 邮件正文
    :param receiver: 收件人邮箱
    :return:
    """
    receiver = receiver  # 收件人
    mail_title = '请查收今天以及往后15天的天气预报，愿你三冬暖，春不寒'
    mail_body = str(msg)
    # 创建一个 message 实例
    # 邮件正文 (plain表示mail_body的内容直接显示，也可以用text，则mail_body的内容在正文中以文本的形式显示，需要下载）
    message = MIMEText(mail_body, 'plain', 'utf-8')
    message['From'] = sender  # 邮件的发件人(用于显示名称，可自定义任意名称)
    message['To'] = receiver  # 邮件的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 创建发送邮件连接
    smtp.connect(smtpserver)  # 连接发送邮件的服务器
    smtp.login(username, password)  # 登录服务器
    smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
    smtp.quit()  # 退出


# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
if __name__ == '__main__':
    sender = 'xxx@qq.com'  # 发件人邮箱
    smtpserver = 'smtp.qq.com'  # 发件人邮箱的SMTP服务器（即sender的SMTP服务器，平台有提供）
    username = 'xxx@qq.com'  # 发件人邮箱的用户名
    password = 'lvsuziegrytfbddc'  # 邮箱授权码（不是登陆邮箱的密码）
    url = 'https://tianqi.so.com/weather/101230201'  # 101230201 是福建省厦门市的编码
    receiver = 'xxx@qq.com'
    tb = get_weather_data(url)  # 获得每一个用户的数据
    send_mail(tb, receiver)  # 发送邮件
