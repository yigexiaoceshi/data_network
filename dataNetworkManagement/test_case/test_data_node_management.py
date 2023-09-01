#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from dataNetworkManagement.apis.data_node_management import DataNodeManagement


@allure.feature("数据节点管理")
class TestDataNodeManagement():

    # @pytest.mark.api_test
    @allure.story("获取数据节点")
    def test_data_node_list(self, test_data_node_data_clear):
        """
        获取数据节点
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataNodeManagement().get_data_node_list()
        print(result)
        assert result['success'] == True
        assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("新增数据节点")
    def test_data_node_add(self, test_data_node_data_clear):
        """
        新增数据节点
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataNodeManagement().data_node_add()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后服务总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 'data_node_name_add_auto_test'
        assert result[3][0][2] == 'description_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("编辑数据节点")
    def test_data_node_edit(self, test_data_node_data_clear):
        """
        编辑数据节点
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataNodeManagement().data_node_edit()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言编辑前后的id相同
        assert result[1][0][0] == result[2][0][0]
        # 断言编辑前后的name不相同
        assert result[1][0][1] != result[2][0][1]
        assert result[1][0][1] != result[2][0][1]

    # @pytest.mark.api_test
    @allure.story("删除数据节点")
    def test_data_node_delete(self, test_data_node_data_clear):
        """
        删除数据节点
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataNodeManagement().data_node_delete()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言当前已删除的id不包含在所有未删除的数据节点id中
        assert result[1][0][0] not in result[2]
