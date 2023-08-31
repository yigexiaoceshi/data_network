#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from dataNetworkManagement.basic.get_login_token import GetLoginToken
from dataNetworkManagement.utils.mysql_execute import MysqlExecute


# 定义一个数据节点管理的类，包含数据节点的增删改查等方法
class DataNodeManagement(GetLoginToken):

    def get_data_node_list(self):
        """
        获取数据节点: /manager-system-webapi/data/manager/data/node/count
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['获取数据节点']
        # 发起请求
        res = requests.get(requests_url, headers=requests_header)
        # 返回JSON格式的response，用作断言
        return res.json()

    def data_node_add(self):
        """
        新增数据节点: /manager-system-webapi/data/node/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['新增数据节点']
        # 定义请求体
        requests_payload = {
            "name": yaml_datas['data_node_add']['name'],
            "description": yaml_datas['data_node_add']['description']
        }
        # 获取发起请求之前的数据节点的总数量
        data_node_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0")
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取发起请求之后的数据节点的总数量
        data_node_number_after = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0")
        # 获取新增数据节点数据
        new_data_node = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where name = 'data_node_name_add_auto_test'")
        # 返回JSON格式的response，请求前和请求后的数据节点的总数量
        return res.json(), data_node_number_before, data_node_number_after, new_data_node

    def data_node_edit(self):
        """
        编辑数据节点: /manager-system-webapi/data/node/edit
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用数据节点新增接口新增一个数据节点
        DataNodeManagement().data_node_add()
        # 按照create_time倒序，查出该新增数据节点
        new_data_node = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where name = 'data_node_name_add_auto_test'")
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['编辑数据节点']
        # 定义请求体
        requests_payload = {
            "parent": new_data_node[0][4],
            "name": yaml_datas['data_node_edit']['name'],
            "description": yaml_datas['data_node_edit']['description'],
            "id": new_data_node[0][0]
        }
        # 发起编辑请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 按照create_time倒序，查找出该节点编辑过后更新的数据
        edit_data_node_select = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0 order by create_time desc limit 1")
        # 返回JSON格式的response以及新增的数据节点在编辑前后的数据，用作断言
        return res.json(), new_data_node, edit_data_node_select

    def data_node_delete(self):
        """
        删除数据节点: /manager-system-webapi/data/node/delete
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用数据节点新增接口，新增一个数据节点
        DataNodeManagement().data_node_add()
        # 按照create_time倒序，查出该新增数据节点
        new_data_node = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where name = 'data_node_name_add_auto_test'")
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['删除数据节点']
        # 定义请求体
        requests_payload = {
            "dataNodeId": new_data_node[0][0]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 获取请求后所有未被删除的数据节点的id，返回元组嵌套元组
        data_nodes = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0")
        data_node_list = []
        # 遍历该元组嵌套元组，得到每个元组的第一个元素，添加到列表，最终列表里得到所有未被删除的数据节点id
        for i in data_nodes:
            data_node_list.append(i[0])
        # 返回JSON格式的response，操作删除之前的数据，以及删除之后所有未被删除的数据节点的id，用作断言
        return res.json(), new_data_node, data_node_list
