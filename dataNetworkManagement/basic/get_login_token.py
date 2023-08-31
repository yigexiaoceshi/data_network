#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from dataNetworkManagement.basic.Basic import Basic


class GetLoginToken(Basic):

    def get_login_token(self):
        """
        登录数据网络管理系统，并从返回值里获取登录token
        :return:
        """
        # 从继承类Basic里获取yaml_datas
        yaml_datas = self.yaml_datas
        # 从yaml文件里读取host和url，通过字符串拼接成requests_url
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['登录']
        # 定义请求体
        requests_payload = {
            "account": yaml_datas['login']['account'],
            "password": yaml_datas['login']['password']
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload)
        try:
            if res.json()['success'] == True and res.json()['code'] == 200:
                # 将response的JSON序列化数据返回
                return res.json()
            else:
                return "登录失败！"
        except:
            return "登录报错！"
