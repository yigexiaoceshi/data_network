#!/usr/bin/python3
# -*- coding:utf-8 -*-
import json
import requests
from dataNetworkManagement.basic.get_login_token import GetLoginToken
from dataNetworkManagement.utils.mysql_execute import MysqlExecute


# 定义一个角色管理的类，包含角色的增删改查等测试方法
class RoleManagement(GetLoginToken):

    def get_role_list(self):
        """
        角色列表：/manager-system-webapi/role/display
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求url
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['角色列表']
        """
        从Excel中提取参数：
        将读取到的string转换为字典方法一：读取Excel第二行第六列数据，通过json.loads(json_string)转换为dict
        requests_payload = json.loads(GetExcelDatas().get_excel_datas()[2][6])
        将读取到的string转换为字典方法二：先创建JSON解析器
        decoder = json.JSONDecoder()
        使用解析器解析json字符串，得到JSON的dict格式，第二种方法具有更强的自定义性和灵活性
        requests_payload = decoder.decode(GetExcelDatas().get_excel_datas()[2][6])
        """
        requests_payload = {
            "pageIdx": 1,
            "pageSize": 10
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 返回JSON格式的response
        return res.json()

    def role_add(self):
        """
        新增角色：/manager-system-webapi/role/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 将菜单id组装成列表，作为新增或编辑角色的入参
        menu_select = MysqlExecute().mysql_execute(
            f"select code from {yaml_datas['mysql_hz_prod']['database_name']}.u_menu")
        menu_list = []
        for i in menu_select:
            menu_list.append(i[0])
        # 从yaml里读取host和path拼接成url
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['新增角色']
        # 定义请求参数
        requests_payload = {
            "name": yaml_datas['role_add']['name'],
            "menuList": menu_list
        }
        # 获取请求之前的角色数量
        role_count_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.u_role")
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取请求之后的角色数量
        role_count_after = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.u_role")
        # 获取新增角色信息，用作断言
        role_new = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = 'role_name_add_auto_test'")
        # 返回JSON格式的response，以及请求前后的角色总数，用作断言
        return res.json(), role_count_before, role_count_after, role_new

    def role_edit(self):
        """
        编辑角色：/manager-system-webapi/role/edit
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用新增方法新增一个角色
        RoleManagement().role_add()
        # 获取该新增角色的角色信息
        role_before = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = 'role_name_add_auto_test'")
        # 将菜单id组装成列表，作为新增或编辑角色的入参
        menu_select = MysqlExecute().mysql_execute(
            f"select code from {yaml_datas['mysql_hz_prod']['database_name']}.u_menu")
        menu_list = []
        for i in menu_select:
            menu_list.append(i[0])
        # 从yaml文件读取host和path，拼接成URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['编辑角色']
        # 定义请求体
        requests_payload = {
            "name": yaml_datas['role_edit']['name'],
            "menuList": menu_list,
            "id": role_before[0][0]
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取请求之后的角色信息
        role_after = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = 'role_name_edit_auto_test'")
        # 返回JSON的response，编辑之前的角色信息，编辑之后的角色信息，用作断言
        return res.json(), role_before[0], role_after[0]

    def role_detail(self):
        """
        角色详情：/manager-system-webapi/role/detail
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['角色详情']
        # 新增一个角色
        RoleManagement().role_add()
        new_role_id = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = 'role_name_add_auto_test'")
        # 定义请求体，查询任意一个roleId查询其详情
        requests_payload = {
            "roleId": new_role_id[0][0]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 返回JSON格式的response
        return res.json()

    def role_delete(self):
        """
        删除角色：/manager-system-webapi/role/delete
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用新增方法先新增一个角色
        RoleManagement().role_add()
        # 获取该新增角色的roleId
        new_role_id = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = 'role_name_add_auto_test'")
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['删除角色']
        # 定义请求体
        requests_payload = {
            "roleId": new_role_id[0][0]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 查询表里所有角色id，返回元组嵌套元组
        roles_select = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where deleted = 0")
        # 定义一个空列表，用来接收遍历后的roleId
        roles_id = []
        for i in roles_select:
            roles_id.append(i[0])
        # 返回JSON格式的response，被删除的roleId和操作删除之后的所有roles_id（roles_id）为列表，用作断言
        return res.json(), new_role_id, roles_id
