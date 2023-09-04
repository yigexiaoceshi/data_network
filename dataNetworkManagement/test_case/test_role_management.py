#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from data_network.dataNetworkManagement.apis.role_management import RoleManagement


@allure.feature("角色管理")
class TestRoleManagement():

    # @pytest.mark.api_test
    @allure.story("角色列表")
    def test_role_list(self):
        """
        角色列表
        :return:
        """
        # 调用户列表接口获取返回值
        result = RoleManagement().get_role_list()
        print(result)
        assert result['success'] == True
        assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("新增角色")
    def test_role_add(self, test_role_data_clear):
        """
        新增角色
        :return:
        """
        # 调用户列表接口获取返回值
        result = RoleManagement().role_add()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后的角色总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 1
        assert result[3][0][2] == 'role_name_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("编辑角色")
    def test_role_edit(self, test_role_data_clear):
        """
        编辑角色
        :return:
        """
        # 调用户列表接口获取返回值
        result = RoleManagement().role_edit()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言编辑前后的角色名称（name）不相同
        assert result[1][2] != result[2][2]

    # @pytest.mark.api_test
    @allure.story("角色详情")
    def test_role_detail(self, test_role_data_clear):
        """
        角色详情
        :return:
        """
        # 调用户列表接口获取返回值
        result = RoleManagement().role_detail()
        print(result)
        assert result['success'] == True
        assert result['code'] == 200
        assert result['data']['name'] == 'role_name_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("删除角色")
    def test_role_delete(self, test_role_data_clear):
        """
        删除角色
        :return:
        """
        # 调用户列表接口获取返回值
        result = RoleManagement().role_delete()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言被删除的角色id不包含在所有未删除的角色id中
        assert result[1][0][0] not in result[2]
