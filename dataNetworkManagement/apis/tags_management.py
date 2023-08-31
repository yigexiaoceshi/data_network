#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from dataNetworkManagement.utils.get_yaml_datas import GetYamlDatas
from dataNetworkManagement.basic.get_login_token import GetLoginToken
from dataNetworkManagement.utils.get_four_randoms import GetFourRandoms
from dataNetworkManagement.utils.mysql_execute import MysqlExecute


#  定义一个标签管理的类，包含标签增删改查等方法
class TagsManagement(GetLoginToken):

    def get_tags_list(self):
        """
        获取标签列表: /manager-system-webapi/tag/display
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['获取标签列表']
        # 定义请求体
        requests_payload = {
            "pageIdx": 1,
            "pageSize": 2
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 返回JSON格式的response，用作断言
        return res.json()

    def tags_add(self):
        """
        新增标签: /manager-system-webapi/tag/add
        :return:
        """
        # 获取类属性：yaml_data
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['新增标签']
        # 定义请求体
        requests_payload = {
            "name": yaml_datas['tag_add']['name'],
            "description": yaml_datas['tag_add']['description']
        }
        # 获取新增之前的所有未被删除的标签的总数量
        tags_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0")
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取新增之后的所有未被删除的标签的总数量
        tags_number_after = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0")
        # 获取新增标签信息
        new_tag = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where name = 'tag_name_add_auto_test'")
        # 返回JSON格式的response，操作新增前后的标签的总数量，用作断言
        return res.json(), tags_number_before, tags_number_after, new_tag

    def tags_edit(self):
        """
        编辑标签: /manager-system-webapi/tag/edit
        :return:
        """
        # 获取类属性：yaml_data
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用标签新增接口新增一个标签
        TagsManagement().tags_add()
        # 查数据库获取该新增标签的数据，用来拼接编辑接口的入参，以及和编辑过后的对比
        new_tag = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where name = 'tag_name_add_auto_test'")
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['编辑标签']
        # 定义请求体
        requests_payload = {
            "name": yaml_datas['tag_edit']['name'],
            "description": yaml_datas['tag_edit']['description'],
            "id": new_tag[0][0]
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 查数据库获取该标签编辑过后的数据
        edit_tag = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where id = {new_tag[0][0]}")
        # 返回JSON格式的response，标签编辑前后的数据，用作断言
        return res.json(), new_tag, edit_tag

    def tags_delete(self):
        """
        删除标签: /manager-system-webapi/tag/delete
        :return:
        """
        # 获取类属性：yaml_data
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用标签新增接口新增一个标签
        TagsManagement().tags_add()
        # 查询数据库获取该标签的数据
        new_tag = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where name = 'tag_name_add_auto_test'")
        # 从查出的数据中得到删除接口的入参
        idList = list(new_tag[0])
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['删除标签']
        # 定义请求体
        requests_payload = {
            "idList": idList
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 查数据库，获取执行删除之后所有未被删除的标签id，得到元组嵌套元组
        idLists_select = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0")
        # 定义空列表，遍历该元组嵌套元组后，列表里得到所有为别删除的标签id
        idLists = []
        for i in idLists_select:
            idLists.append(i[0])
        # 返回JSON格式的response，删除之前的标签信息，以及删除之后所有未被删除的标签id，用作断言
        return res.json(), new_tag, idLists
