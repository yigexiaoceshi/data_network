#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
from data_network.dataNetworkManagement.apis.data_management import DataManagement


@allure.feature("数据服务管理")
class TestDataManagement():

    # @pytest.mark.api_test
    @allure.story("数据服务列表")
    def test_data_management_list(self, test_api_data_clear):
        """
        数据服务列表
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().get_data_list()
        print(result)
        assert result['success'] == True
        assert result['code'] == 200

    # @pytest.mark.api_test
    @allure.story("新增http类型数据服务")
    def test_data_add_http(self, test_api_data_clear):
        """
        新增http类型数据服务
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().data_add_http()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后的服务总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        # 必填字段正确入库，d_data_manager_info表
        assert result[3][0][1] == 1
        assert result[3][0][4] == 'http'
        assert result[3][0][7] == 'Data_name_http_add_auto_test'
        assert result[3][0][8] == 'V1.0.0'
        assert result[3][0][9] == 'description_add_auto_test'
        assert result[3][0][37] == 0
        assert result[3][0][42] == 'api.oioweb.cn'
        assert result[3][0][43] == 'No'
        assert result[3][0][44] == 'description_test_data_add_second'
        # 必填字段正确入库，d_data_manager_api表
        assert result[4][0][1] == 'http'
        assert result[4][0][2] == 'get'
        assert result[4][0][3] == '/api/common/history'
        assert result[4][0][22] == 0
        assert result[4][0][23] == 'application/json'
        # 中枢Redis
        assert result[5]['serviceManage']['apiName'] == 'Data_name_http_add_auto_test'
        assert result[5]['serviceManage']['apiDesc'] == 'description_add_auto_test'
        assert result[5]['serviceManage']['apiVersion'] == 'V1.0.0'
        assert result[5]['serviceManage']['connectorType'] == 'http'
        assert result[5]['serviceManage']['connectorCode'] == 'a56d81b86eb847be8d68757c49252f21'
        assert result[5]['serviceManage']['dataSystem'][0] == 'api.oioweb.cn'
        assert result[5]['serviceManage']['accessProtocol'] == 'http'
        assert result[5]['serviceManage']['requestMethod'] == 'get'
        assert result[5]['serviceManage']['status'] == 1
        assert result[5]['serviceManage'][
                   'route'] == '{"path":"/api/common/history","method":"get","contentType":"application/json"}'
        assert result[5]['serviceManage']['requestPath'] == '/api/common/history'
        # 数据网络Redis，firstKey
        assert result[6][0]['authorizationType'] == 'Public'
        assert result[6][0]['name'] == 'Data_name_http_add_auto_test'
        assert result[6][0]['version'] == 'V1.0.0'
        assert result[6][0]['description'] == 'description_add_auto_test'
        # 数据网络Redis，secondKey
        assert result[7][0]['type'] == 'http'
        assert result[7][0]['endpoint'] == 'api.oioweb.cn'
        assert result[7][0]['tls'] == 'No'
        assert result[7][0]['description'] == 'description_test_data_add_second'
        # 数据网络Redis，thirdKey
        assert result[8][0]['type'] == 'http'
        assert result[8][0]['protocol'] == 'http'
        assert result[8][0]['method'] == 'get'
        assert result[8][0]['path'] == '/api/common/history'
        assert result[8][0]['contentType'] == 'application/json'
        assert result[8][0]['mockData'] == 'MockData'
        assert result[8][0]['transferProtocol'] == 'HTTP->HTTP'
        assert result[8][0]['requestGroovy'] == 'request_groovy_test'
        assert result[8][0]['responseGroovy'] == 'response_groovy_test'

    # @pytest.mark.api_test
    @allure.story("新增database类型数据服务")
    def test_data_add_database(self,test_api_data_clear):
        """
        新增database类型数据服务
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().data_add_database()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后的服务总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 1
        assert result[3][0][4] == 'database'
        assert result[3][0][7] == 'Data_name_database_add_auto_test'
        assert result[3][0][8] == 'V1.0.0'
        assert result[3][0][9] == 'description_add_auto_test'
        assert result[3][0][37] == 0
        assert result[3][0][42] == 'rm-3ns1r51utqk2nfjp0uo.mysql.rds.aliyuncs.com:3306'
        assert result[3][0][43] == 'No'
        assert result[3][0][44] == 'description_test_data_add_second'
        assert result[4][0][1] == 'http'
        assert result[4][0][2] == 'post'
        assert result[4][0][3] == '/database/mysql/test'
        assert result[4][0][22] == 0
        assert result[4][0][23] == 'application/json'
        # 中枢Redis
        assert result[5]['serviceManage']['apiName'] == 'Data_name_database_add_auto_test'
        assert result[5]['serviceManage']['apiDesc'] == 'description_add_auto_test'
        assert result[5]['serviceManage']['apiVersion'] == 'V1.0.0'
        assert result[5]['serviceManage']['connectorType'] == 'mysql'
        assert result[5]['serviceManage']['connectorCode'] == '016d8036b81046259895330b2285b10f'
        assert result[5]['serviceManage']['dataSystem'][0] == 'rm-3ns1r51utqk2nfjp0uo.mysql.rds.aliyuncs.com:3306'
        assert result[5]['serviceManage']['accessProtocol'] == ''
        assert result[5]['serviceManage']['requestMethod'] == 'post'
        assert result[5]['serviceManage']['status'] == 1
        assert result[5]['serviceManage'][
                   'route'] == '{"password":"*Rj7a8T%9Bp6s42","databaseName":"dde_manager","options":"serverTimezone=GMT%2B8&useSSL=false","version":"5.7","databaseKind":"mysql","username":"root"}'
        assert result[5]['serviceManage']['requestPath'] == '/database/mysql/test'
        # 数据网络Redis，firstKey
        assert result[6][0]['authorizationType'] == 'Public'
        assert result[6][0]['name'] == 'Data_name_database_add_auto_test'
        assert result[6][0]['version'] == 'V1.0.0'
        assert result[6][0]['description'] == 'description_add_auto_test'
        # 数据网络Redis，secondKey
        assert result[7][0]['type'] == 'database'
        assert result[7][0]['endpoint'] == 'rm-3ns1r51utqk2nfjp0uo.mysql.rds.aliyuncs.com:3306'
        assert result[7][0]['tls'] == 'No'
        assert result[7][0]['description'] == 'description_test_data_add_second'
        # 数据网络Redis，thirdKey
        assert result[8][0]['type'] == 'database'
        assert result[8][0]['protocol'] == 'http'
        assert result[8][0]['method'] == 'post'
        assert result[8][0]['path'] == '/database/mysql/test'
        assert result[8][0]['contentType'] == 'application/json'
        assert result[8][0]['transferProtocol'] == 'Database->HTTP'
        assert result[8][0]['requestGroovy'] == 'request_groovy_test'
        assert result[8][0]['responseGroovy'] == 'response_groovy_test'

    # @pytest.mark.api_test
    @allure.story("新增map类型数据服务")
    def test_data_add_map(self,test_api_data_clear):
        """
        新增map类型数据服务
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().data_add_map()
        print(result)
        assert result[0]["success"] == True
        assert result[0]['code'] == 200
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 1
        assert result[3][0][4] == 'map'
        assert result[3][0][7] == 'Data_name_map_add_auto_test'
        assert result[3][0][8] == 'V1.0.0'
        assert result[3][0][9] == 'description_add_auto_test'
        assert result[3][0][37] == 0
        assert result[3][0][42] == '192.168.1.1:8080'
        assert result[3][0][43] == 'No'
        assert result[3][0][44] == 'description_test_data_add_second'
        # 中枢Redis
        assert result[5]['serviceManage']['apiName'] == 'Data_name_map_add_auto_test'
        assert result[5]['serviceManage']['apiDesc'] == 'description_add_auto_test'
        assert result[5]['serviceManage']['apiVersion'] == 'V1.0.0'
        assert result[5]['serviceManage']['connectorType'] == 'http'
        assert result[5]['serviceManage']['connectorCode'] == 'a56d81b86eb847be8d68757c49252f21'
        assert result[5]['serviceManage']['dataSystem'][0] == '192.168.1.1:8080'
        assert result[5]['serviceManage']['accessProtocol'] == 'http'
        assert result[5]['serviceManage']['requestMethod'] == 'post'
        assert result[5]['serviceManage']['status'] == 1
        assert result[5]['serviceManage']['route'] == '{"path":"/api/map/test","method":"post","contentType":"application/json"}'
        assert result[5]['serviceManage']['requestPath'] == '/api/map/test'
        # 数据网络Redis，firstKey
        assert result[6][0]['authorizationType'] == 'Public'
        assert result[6][0]['name'] == 'Data_name_map_add_auto_test'
        assert result[6][0]['version'] == 'V1.0.0'
        assert result[6][0]['description'] == 'description_add_auto_test'
        # 数据网络Redis，secondKey
        assert result[7][0]['type'] == 'map'
        assert result[7][0]['endpoint'] == '192.168.1.1:8080'
        assert result[7][0]['tls'] == 'No'
        assert result[7][0]['description'] == 'description_test_data_add_second'

    # @pytest.mark.api_test
    @allure.story("新增图片类型数据服务")
    def test_data_add_imagery(self,test_api_data_clear):
        """
        新增图片类型数据服务
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().data_add_imagery()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 断言新增前后服务总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 1
        assert result[3][0][4] == 'imageBase'
        assert result[3][0][7] == 'Data_name_imagery_add_auto_test'
        assert result[3][0][8] == 'V1.0.0'
        assert result[3][0][9] == 'description_add_auto_test'
        assert result[3][0][37] == 0
        assert result[3][0][42] == 'hbimg.huabanimg.com'
        assert result[3][0][43] == 'No'
        assert result[3][0][44] == 'description_test_data_add_second'
        assert result[4][0][1] == 'http'
        assert result[4][0][2] == 'get'
        assert result[4][0][3] == '/api/imagery/test'
        assert result[4][0][22] == 0
        assert result[4][0][23] == 'application/x-www-form-urlencoded'
        # 中枢Redis
        assert result[5]['serviceManage']['apiName'] == 'Data_name_imagery_add_auto_test'
        assert result[5]['serviceManage']['apiDesc'] == 'description_add_auto_test'
        assert result[5]['serviceManage']['apiVersion'] == 'V1.0.0'
        assert result[5]['serviceManage']['connectorType'] == 'http'
        assert result[5]['serviceManage']['connectorCode'] == 'a56d81b86eb847be8d68757c49252f21'
        assert result[5]['serviceManage']['dataSystem'][0] == 'hbimg.huabanimg.com'
        assert result[5]['serviceManage']['accessProtocol'] == 'http'
        assert result[5]['serviceManage']['requestMethod'] == 'get'
        assert result[5]['serviceManage']['status'] == 1
        assert result[5]['serviceManage'][
                   'route'] == '{"path":"/api/imagery/test","method":"get","contentType":"application/x-www-form-urlencoded"}'
        assert result[5]['serviceManage']['requestPath'] == '/api/imagery/test'
        # 数据网络Redis，firstKey
        assert result[6][0]['authorizationType'] == 'Public'
        assert result[6][0]['name'] == 'Data_name_imagery_add_auto_test'
        assert result[6][0]['version'] == 'V1.0.0'
        assert result[6][0]['description'] == 'description_add_auto_test'
        # 数据网络Redis，secondKey
        assert result[7][0]['type'] == 'imageBase'
        assert result[7][0]['endpoint'] == 'hbimg.huabanimg.com'
        assert result[7][0]['tls'] == 'No'
        assert result[7][0]['description'] == 'description_test_data_add_second'
        # 数据网络Redis，thirdKey
        assert result[8][0]['type'] == 'http'
        assert result[8][0]['protocol'] == 'http'
        assert result[8][0]['method'] == 'get'
        assert result[8][0]['path'] == '/api/imagery/test'
        assert result[8][0]['contentType'] == 'application/x-www-form-urlencoded'
        assert result[8][0]['transferProtocol'] == 'HTTP->HTTP'
        assert result[8][0]['requestGroovy'] == 'request_groovy_test'
        assert result[8][0]['responseGroovy'] == 'response_groovy_test'

    # @pytest.mark.api_test
    @allure.story("新增linkdata类型数据服务")
    def test_data_add_linkdata(self,test_api_data_clear):
        """
        新增linkdata类型数据服务
        :return:
        """
        # 调用户列表接口获取返回值
        result = DataManagement().data_add_linkdata()
        print(result)
        assert result[0]['success'] == True
        assert result[0]['code'] == 200
        # 短信新增前后服务总数量相差1
        assert result[2][0][0] - result[1][0][0] == 1
        assert result[3][0][1] == 1
        assert result[3][0][4] == 'linkData'
        assert result[3][0][7] == 'Data_name_linkdata_add_auto_test'
        assert result[3][0][8] == 'V1.0.0'
        assert result[3][0][9] == 'description_add_auto_test'
        assert result[3][0][37] == 0
        assert result[3][0][42] == '192.168.0.1:8080'
        assert result[3][0][43] == 'No'
        assert result[3][0][44] == 'description_test_data_add_second'
        assert result[4][0][1] == 'http'
        assert result[4][0][2] == 'get'
        assert result[4][0][3] == '/api/linkdata/test'
        assert result[4][0][22] == 0
        assert result[4][0][23] == 'application/json'
        # 中枢Redis
        assert result[5]['serviceManage']['apiName'] == 'Data_name_linkdata_add_auto_test'
        assert result[5]['serviceManage']['apiDesc'] == 'description_add_auto_test'
        assert result[5]['serviceManage']['apiVersion'] == 'V1.0.0'
        assert result[5]['serviceManage']['connectorType'] == 'http'
        assert result[5]['serviceManage']['connectorCode'] == 'a56d81b86eb847be8d68757c49252f21'
        assert result[5]['serviceManage']['dataSystem'][0] == '192.168.0.1:8080'
        assert result[5]['serviceManage']['accessProtocol'] == 'http'
        assert result[5]['serviceManage']['requestMethod'] == 'get'
        assert result[5]['serviceManage']['status'] == 1
        assert result[5]['serviceManage']['route'] == '{"path":"/api/linkdata/test","method":"get","contentType":"application/json"}'
        assert result[5]['serviceManage']['requestPath'] == '/api/linkdata/test'
        # 数据网络Redis，firstKey
        assert result[6][0]['authorizationType'] == 'Public'
        assert result[6][0]['name'] == 'Data_name_linkdata_add_auto_test'
        assert result[6][0]['version'] == 'V1.0.0'
        assert result[6][0]['description'] == 'description_add_auto_test'
        # 数据网络Redis，secondKey
        assert result[7][0]['type'] == 'linkData'
        assert result[7][0]['endpoint'] == '192.168.0.1:8080'
        assert result[7][0]['tls'] == 'No'
        assert result[7][0]['description'] == 'description_test_data_add_second'
        # 数据网络Redis，thirdKey
        assert result[8][0]['type'] == 'http'
        assert result[8][0]['protocol'] == 'http'
        assert result[8][0]['method'] == 'get'
        assert result[8][0]['path'] == '/api/linkdata/test'
        assert result[8][0]['contentType'] == 'application/json'
        assert result[8][0]['transferProtocol'] == 'HTTP->HTTP'
        assert result[8][0]['requestGroovy'] == 'request_groovy_test'
        assert result[8][0]['responseGroovy'] == 'response_groovy_test'