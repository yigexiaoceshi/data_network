#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from dataNetworkManagement.apis.tags_management import TagsManagement


@allure.feature("标签管理")
class TestTagsManagement():

    # @pytest.mark.api_test
    @allure.story("标签列表")
    def test_get_tags_list(self, test_tag_data_clear):
        """
        标签列表
        :return:
        """
        with allure.step("步骤一：d调用用户列表获取返回值"):
            # 调用户列表接口获取返回值
            result = TagsManagement().get_tags_list()
            print(result)
        with allure.step("步骤二：获取返回结果的success做断言"):
            assert result['success'] == True
        with allure.step("步骤三：获取返回结果的code做断言"):
            assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("标签新增")
    def test_tags_add(self, test_tag_data_clear):
        """
        标签新增
        :return:
        """  # 调用户列表接口获取返回值
        result = TagsManagement().tags_add()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后的标签总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 'tag_name_add_auto_test'
        assert result[3][0][2] == 'description_add_auto_test'

    # @pytest.mark.api_test
    @allure.story("标签编辑")
    def test_tags_edit(self, test_tag_data_clear):
        """
        标签编辑
        :return:
        """
        # 调用户列表接口获取返回值
        result = TagsManagement().tags_edit()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言编辑前后标签id相同
        assert result[1][0][0] == result[2][0][0]
        # 断言编辑前后标签名称不相同
        assert result[1][0][1] != result[2][0][1]
        assert result[1][0][2] != result[2][0][2]

    # @pytest.mark.api_test
    @allure.story("标签删除")
    def test_tags_delete(self, test_tag_data_clear):
        """
        标签删除
        :return:
        """
        # 调用户列表接口获取返回值
        result = TagsManagement().tags_delete()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言被删除标签id不包含在所有未删除标签id中
        assert result[1][0] not in result[2]
