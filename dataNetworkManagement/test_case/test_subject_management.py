#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from dataNetworkManagement.apis.subjects_management import SubjectsManagement


@allure.feature("学科管理")
class TestSubjectManagement():

    # @pytest.mark.api_test
    @allure.story("学科列表")
    def test_subject_list(self, test_subject_data_clear):
        """
        学科列表
        :return:
        """
        # 调用户列表接口获取返回值
        result = SubjectsManagement().get_subject_list()
        assert result['success'] == True
        assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("新增学科")
    def test_subject_add(self, test_subject_data_clear):
        """
        新增学科
        :return:
        """
        # 调用户列表接口获取返回值
        result = SubjectsManagement().subject_add()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后的学科总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 'subject_name_add_auto_test'
        assert result[3][0][2] == 'description_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("编辑学科")
    def test_subject_edit(self, test_subject_data_clear):
        """
        编辑学科
        :return:
        """
        # 调用户列表接口获取返回值
        result = SubjectsManagement().subject_edit()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言编辑前后的学科id相同
        assert result[1][0][0] == result[2][0][0]
        # 断言编辑前后学科名称不相同
        assert result[1][0][1] != result[2][0][1]
        assert result[1][0][1] == 'subject_name_add_auto_test'
        assert result[2][0][1] == 'subject_name_edit_auto_test'
        assert result[1][0][2] != result[2][0][2]
        assert result[1][0][2] == 'description_add_auto_test'
        assert result[2][0][2] == 'description_edit_auto_test'

    # @pytest.mark.api_test
    @allure.story("删除学科")
    def test_subject_delete(self, test_subject_data_clear):
        """
        删除学科
        :return:
        """
        # 调用户列表接口获取返回值
        result = SubjectsManagement().subject_delete()
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言被删除学科id不包含在所有未删除学科id中
        assert result[1] not in result[2]
