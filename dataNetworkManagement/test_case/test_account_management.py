#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from dataNetworkManagement.apis.account_management import AccountManagement


@allure.feature('用户管理')
class TestAccountManagement():

    # @pytest.mark.api_test
    @allure.title("获取用户列表")
    @allure.story("获取用户列表")
    def test_account_list(self, test_account_data_clear):
        """
        获取用户列表1
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().get_account_list()
        assert result['success'] == True
        assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("新增用户")
    def test_account_add(self, test_account_data_clear):
        """
        新增用户
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_add()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        assert result[1][0][1] == 'account_add_auto_test'
        assert result[1][0][4] == 'nick_name_add_auto_test'
        assert result[1][0][10] == 'description_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("编辑用户")
    def test_account_edit(self, test_account_data_clear):
        """
        编辑用户
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_edit()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        assert result[1] == 'nick_name_add_auto_test'
        assert result[2] == 'nick_name_edit_auto_test'

    # @pytest.mark.api_test
    @allure.story("用户详情")
    def test_account_detail(self,test_account_data_clear):
        """
        用户详情
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_detail()
        assert result['success'] == True
        assert result['code'] == 200
        assert result['data']['account'] == 'account_add_auto_test'
        assert result['data']['nickName'] == 'nick_name_add_auto_test'
        assert result['data']['description'] == 'description_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("停用用户")
    def test_account_disable(self,test_account_data_clear):
        """
        停用用户
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_disable()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言当前用户的启用状态为禁用
        assert result[1] == 0

    # @pytest.mark.api_test
    @allure.story("启用用户")
    def test_account_enable(self,test_account_data_clear):
        """
        启用用户
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_enable()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言当前用户的启用状态为启用
        assert result[1] == 1

    # @pytest.mark.api_test
    @allure.story("删除用户")
    def test_account_delete(self,test_account_data_clear):
        """
        删除用户
        :return:
        """
        # 调用户列表接口获取返回值
        result = AccountManagement().account_delete()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言当前用户id不包含在所有未删除的用户id
        assert result[1] not in result[2]
