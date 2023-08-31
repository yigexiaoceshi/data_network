#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from dataNetworkManagement.utils.mysql_execute import MysqlExecute
from dataNetworkManagement.basic.Basic import Basic


class GetCentralsystemToken(Basic):

    def get_centralsystem_token(self):
        """
        获取中枢token：/api/central/token
        :return:
        """
        # 从继承类basis里获取yaml_datas
        yaml_datas = self.yaml_datas
        # 查询数据库得出AK/SK
        payload_data = MysqlExecute().mysql_execute(
            f"select access_key,secret_key from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'liyong'")
        # 从yaml_datas里获取请求url
        requests_url = yaml_datas['api_interface'] + yaml_datas['api_url']['获取中枢token']
        # 构造请求体
        requests_payload = {
            "accessKey": payload_data[0][0],
            "secretKey": payload_data[0][1]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload)
        # 返回response的json序列化数据
        return res.json()
