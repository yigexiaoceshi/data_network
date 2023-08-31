#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import requests
from dataNetworkManagement.utils.mysql_execute import MysqlExecute
from dataNetworkManagement.basic.get_login_token import GetLoginToken


# 定义一个用户管理的类，包含用户增删改查、启用/停用等方法
class AccountManagement(GetLoginToken):

    def get_account_list(self):
        """
        用户列表：/manager-system-webapi/account/display
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml_datas里获取URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['用户列表']
        # 定义请求体
        requests_payload = {
            "pageIdx": 1,
            "pageSize": 10
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 返回JSON格式的response，用作断言
        return res.json()

    def account_add(self):
        """
        新增用户：/manager-system-webapi/account/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 查询所有角色id
        role_id_select = \
            MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = '自定义管理员角色'")[0]
        # 转换成列表，得到角色新增、角色编辑的通用参数
        role_id_list = list(role_id_select)
        # 从yaml_datas里获取请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['新增用户']
        # 定义请求体
        requests_paylyad = {
            "account": yaml_datas['account_add']['account'],
            "nickName": yaml_datas['account_add']['nickName'],
            "roleIdList": role_id_list,
            "phone": str(yaml_datas['account_add']['phone']) + four_randoms[1],
            "email": str(yaml_datas['account_add']['email']) + four_randoms[1],
            "description": yaml_datas['account_add']['description']
        }
        try:
            # 发起请求
            res = requests.post(requests_url, json=requests_paylyad, headers=requests_header)
            if res.json()['code'] == 500 and res.json()['msg'] == 'account repeat':
                return '新增用户失败，用户名重复！'
            else:
                new_user = MysqlExecute().mysql_execute(
                    f"select * from data_network_prod.u_account where account = 'account_add_auto_test'")
                # 返回JSON格式的response，用作断言
                return res.json(), new_user
        except:
            return "新增用户报错！"

    def account_edit(self):
        """
        编辑用户：/manager-system-webapi/account/edit
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 查询所有角色id
        role_id_select = \
            MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name = '自定义管理员角色'")[0]
        # 转换成列表，得到角色新增、角色编辑的通用参数
        role_id_list = list(role_id_select)
        # 调用新增方法，先新增一个用户
        AccountManagement().account_add()
        # 获取该新增用户的nickName
        nickName_before = \
            MysqlExecute().mysql_execute(
                f"select nick_name from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")[
                0][0]
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['编辑用户']
        # 定义请求体
        requests_payload = {
            "account": yaml_datas['account_edit']['account'],
            "nickName": yaml_datas['account_edit']['nickName'],
            "roleIdList": role_id_list,
            "phone": str(yaml_datas['account_add']['phone']) + four_randoms[1],
            "email": str(yaml_datas['account_add']['email']) + four_randoms[1],
            "description": yaml_datas['account_edit']['description'],
            "id":
                MysqlExecute().mysql_execute(
                    f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")[
                    0][0]
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 获取编辑之后该用户的nickName
        nickName_after = \
            MysqlExecute().mysql_execute(
                f"select nick_name from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")[
                0][0]
        # 返回json格式的response，操作编辑之前的nickName和编辑之后的nickName，用作断言
        return res.json(), nickName_before, nickName_after

    def account_detail(self):
        """
        用户详情：/manager-system-webapi/account/detail
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['用户详情']
        # 新增一个用户
        AccountManagement().account_add()
        # 定义请求体
        requests_payload = {
            "accountId":
                MysqlExecute().mysql_execute(
                    f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")[
                    0][0]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 返回JSON格式的response，用作断言
        return res.json()

    def account_disable(self):
        """
        停用用户：/manager-system-webapi/account/disable
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['停用用户']
        # 新增一个用户
        AccountManagement().account_add()
        # 获取该新增用户的id
        account_id = \
            MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")
        # 如果查询结果为空
        if account_id == ():
            # 没有启用状态的用户
            print("创建新用户失败！")
        # 查询结果不为空
        else:
            # 定义请求体
            requests_payload = {
                "accountId": account_id[0][0]
            }
            # 发起请求
            res = requests.get(requests_url, params=requests_payload, headers=requests_header)
            # 由account_id得到实际的用户id
            id = account_id[0][0]
            # 获取停用之后的该用户的状态
            account_status = \
                MysqlExecute().mysql_execute(
                    f"select active from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where id = {id}")[0][
                    0]
            # 返回JSON格式的response，以及停用之后的用户状态，用作断言
            return res.json(), account_status,id

    def account_enable(self):
        """
        启用用户：/manager-system-webapi/account/enable
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['启用用户']
        # 调用禁用用户方法，获得新增用户并操作禁用
        disable_account = AccountManagement().account_disable()
        # 定义请求体
        requests_payload = {
            "accountId": disable_account[2]
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 查询启用之后的用户状态
        account_status = \
            MysqlExecute().mysql_execute(
                f"select active from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where id = {disable_account[2]}")[0][
                0]
        # 返回JSON格式的response，启用之后的该用户的状态，用作断言
        return res.json(), account_status

    def account_delete(self):
        """
        删除用户：/manager-system-webapi/account/delete
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类Basic中获取类属性：four_randoms
        four_randoms = self.four_randoms
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 调用新增方法先新增一个用户
        AccountManagement().account_add()
        # 获取该新增用户的用户id
        account_id = \
            MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account order by create_time desc limit 1")[
                0][0]
        # 从yaml文件里获取host和path，拼接成请求URL
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['删除用户']
        # 定义请求体
        requests_payload = {
            "accountId": account_id
        }
        # 发起请求
        res = requests.get(requests_url, params=requests_payload, headers=requests_header)
        # 查询操作删除之后的所有的用户id，返回元组嵌套元组
        accounts_select = MysqlExecute().mysql_execute(
            f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where deleted = 0")
        # 定义空列表，用来接收遍历查询结果之后的所有元素，得到用户id的列表
        accounts_id = []
        for i in accounts_select:
            accounts_id.append(i[0])
        # 返回JSON格式的response，新增并被删除的用户id，以及删除之后的所有用户id列表，用作断言
        return res.json(), account_id, accounts_id