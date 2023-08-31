#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from dataNetworkManagement.basic.get_login_token import GetLoginToken
from dataNetworkManagement.utils.mysql_execute import MysqlExecute


# 定义一个学科管理的类，包含学科的增删改查等方法
class SubjectsManagement(GetLoginToken):

    def get_subject_list(self):
        """
        获取学科：/manager-system-webapi/subject/display
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['获取学科']
        # 定义请求体
        requests_payload = {}
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 返回JSON格式的response，用作断言
        return res.json()

    def subject_add(self):
        """
        新增学科：/manager-system-webapi/subject/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['新增学科']
        # 定义请求体
        requests_payload = {
            "name": yaml_datas['subject_add']['name'],
            "description": yaml_datas['subject_add']['description']
        }
        # 获取请求之前所有未被删除的学科的数量
        subjects_count_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0")
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取请求之后所有未被删除的学科的数量
        subjects_count_after = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0")
        # 获取新增学科信息，用作断言
        new_subject = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where name = 'subject_name_add_auto_test'")
        # 返回JSON格式的response，发起请求前后的学科的总数量
        return res.json(), subjects_count_before, subjects_count_after, new_subject

    def subject_edit(self):
        """
        编辑学科：/manager-system-webapi/subject/edit
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用学科新增接口新增一个学科
        SubjectsManagement().subject_add()
        # 获取该新增学科信息
        new_subject_detail_before = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where name = 'subject_name_add_auto_test'")
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['编辑学科']
        # 定义请求体，更改name和description
        requests_payload = {
            "parent": new_subject_detail_before[0][4],
            "name": yaml_datas['subject_edit']['name'],
            "description": yaml_datas['subject_edit']['description'],
            "id": new_subject_detail_before[0][0]
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取编辑之后的学科
        new_subject_detail_after = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject order by create_time desc limit 1")
        # 返回JSON格式的response，以及编辑前后的学科信息，可在断言里用作比较
        return res.json(), new_subject_detail_before, new_subject_detail_after

    def subject_delete(self):
        """
        删除学科：/manager-system-webapi/subject/delete
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用学科新增方法新增一个学科
        SubjectsManagement().subject_add()
        # 获取该新增学科信息
        new_subject_detail = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where name = 'subject_name_add_auto_test'")
        # 获取该新增学科的id，作为删除的入参
        new_subject_id = new_subject_detail[0][0]
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['删除学科']
        # 定义请求体
        requests_payload = {
            "subjectId": new_subject_id
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 查询所有学科的id，得到元组嵌套元组
        subjects_id_select = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0")
        # 定义空列表，遍历元组嵌套元组之后，该列表得到所有学科id
        subjects_id = []
        for i in subjects_id_select:
            subjects_id.append(i[0])
        # 返回JSON格式的response，新增的学科id，以及删除之后所有未删除的学科id，用作断言
        return res.json(), new_subject_id, subjects_id
