#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class WechatRobotSender(object):
    def __init__(self, robot_key: str):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robot_key
        self.headers = {
            'ContentType': 'application/json'
        }

    def send_markdown_msg(self, markdown_text: str):
        session = requests.session()
        body = {
            'msgtype': 'markdown',
            'markdown': {
                'content': markdown_text
            }
        }
        try:
            response = session.post(url=self.url, headers=self.headers, json=body)
            assert response.status_code == 200, print(response.text)
        except Exception as e:
            print(e)
        finally:
            session.close()


if __name__ == '__main__':
    print('This wechat robot sender')
