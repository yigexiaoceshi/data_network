#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import os
from dataNetworkManagement.utils.get_yaml_datas import GetYamlDatas
from dataNetworkManagement.utils.mysql_execute import MysqlExecute
from dataNetworkManagement.utils.redis_execute import RedisExecute

yaml_path = os.getcwd() + "/datas/data_network.yaml"


@pytest.fixture(scope="function")
def test_account_data_clear():
    """
    处理"用户管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    account_id = MysqlExecute().mysql_execute(
        f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")
    # 清除用户表测试数据
    MysqlExecute().mysql_execute(
        f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.u_account where account = 'account_add_auto_test'")
    if account_id == ():
        pass
    else:
        # 清除用户与角色关联关系测试数据
        MysqlExecute().mysql_execute(
            f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.u_account_role_relation where u_account_id = {account_id[0][0]}")
    print("测试数据清理完毕，当前用例执行完成。")


@pytest.fixture(scope="function")
def test_role_data_clear():
    """
    处理"角色管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    role_id = MysqlExecute().mysql_execute(
        f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name in ('role_name_add_auto_test','role_name_edit_auto_test')")
    # 清除角色表测试数据
    MysqlExecute().mysql_execute(
        f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.u_role where name in ('role_name_add_auto_test','role_name_edit_auto_test')")
    if role_id == ():
        pass
    else:
        # 清除角色与菜单关联关系测试数据
        MysqlExecute().mysql_execute(
            f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.u_role_menu_relation where u_role_id = {role_id[0][0]}")
    print("测试数据清理完毕，当前用例执行完成。")


@pytest.fixture(scope="function")
def test_subject_data_clear():
    """
    处理"学科管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    # 清除学科表测试数据
    MysqlExecute().mysql_execute(
        f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where name in ('subject_name_add_auto_test','subject_name_edit_auto_test')")
    print("测试数据清理完毕，当前用例执行完成。")


@pytest.fixture(scope="function")
def test_tag_data_clear():
    """
    处理"标签管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    # 清除标签表测试数据
    MysqlExecute().mysql_execute(
        f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where name in ('tag_name_add_auto_test','tag_name_edit_auto_test')")
    print("测试数据清理完毕，当前用例执行完成。")


@pytest.fixture(scope="function")
def test_data_node_data_clear():
    """
    处理"数据节点管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    # 清除数据节点表测试数据
    MysqlExecute().mysql_execute(
        f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where name in ('data_node_name_add_auto_test','data_node_name_edit_auto_test')")
    print("测试数据清理完毕，当前用例执行完成。")


@pytest.fixture(scope="function")
def test_api_data_clear():
    """
    处理"数据服务管理"模块的测试用例执行前后的数据清理
    :return:
    """
    print("开始执行")

    yield
    yaml_datas = GetYamlDatas().get_yaml_datas()
    # 获取新增api的id
    api_id = MysqlExecute().mysql_execute(
        f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
    # 获取新增api的dataAddress
    dataAddress = MysqlExecute().mysql_execute(
        f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
    if api_id == ():
        print("无需清理！")
    else:
        # 根据id删除步骤一和步骤二api数据
        MysqlExecute().mysql_execute(
            f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where id = {api_id[0][0]}")
        # 根据id删除步骤三数据
        MysqlExecute().mysql_execute(
            f"delete from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_id[0][0]}")
    if dataAddress == ():
        print('无需清理！')
    else:
        RedisExecute().redis_execute("centralsystem", "delete", dataAddress[0][2])
        RedisExecute().redis_execute("data_network", "delete", f"{yaml_datas['login']['account']}")
    print("测试数据清理完毕，当前用例执行完成。")
