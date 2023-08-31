#!/usr/bin/python3
# -*- coding:utf-8 -*-
import random
import requests
from dataNetworkManagement.basic.get_login_token import GetLoginToken
from dataNetworkManagement.utils.mysql_execute import MysqlExecute
from dataNetworkManagement.utils.redis_execute import RedisExecute


class DataManagement(GetLoginToken):

    def get_data_list(self):
        """
        数据服务列表: /manager-system-webapi/data/manager/page
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 从yaml文件里获取请求url
        requests_url = yaml_datas['host'] + yaml_datas['api_url']['数据服务列表']
        # 定义请求体
        requests_payload = {
            "pageIdx": 1,
            "pageSize": 10
        }
        # 发起请求
        res = requests.post(requests_url, json=requests_payload, headers=requests_header)
        # 返回response的JSON序列化数据
        return res.json()

    def data_add_http(self):
        """
        数据服务新增_first: /manager-system-webapi/data/manager/first
        数据服务新增_second: /manager-system-webapi/data/manager/second
        数据服务新增_third: /manager-system-webapi/data/manager/third
        数据服务新增_submit: /manager-system-webapi/data/manager/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 获取步骤一的请求URL
        requests_url_first = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_first']
        # 获取任意一个未删除的学科，用作步骤一的入参
        subjects = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0 order by create_time desc limit 1")
        if subjects == ():
            subjects = []
        else:
            subjects = [
                {
                    "id": subjects[0][0],
                    "level": subjects[0][5],
                    "parent": subjects[0][4],
                    "name": subjects[0][1],
                    "icon": subjects[0][6],
                    "description": subjects[0][2],
                    "count": ""
                }
            ]
        # 获取任意一个未删除的标签，用作步骤一的入参
        tags = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0 order by create_time desc limit 1")
        # 获取未删除的数据节点id
        if tags == ():
            tags = []
        else:
            tags = [
                {
                    "id": tags[0][0],
                    "name": tags[0][1],
                    "description": tags[0][2],
                    "label": tags[0][1],
                    "value": tags[0][0]
                }
            ]
        data_node_id_list = []
        for i in MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0"):
            data_node_id_list.append(i[0])
        # 从所有未删除的数据节点id的列表中随机取两位元素，生成新的列表，作为步骤一的入参
        dataNodeIdList = random.sample(data_node_id_list, 0)
        # 定义步骤一的请求体
        requests_payload_first = {
            "name": yaml_datas['data_add_first']['name_http'],
            "version": yaml_datas['data_add_first']['version'],
            "description": yaml_datas['data_add_first']['description'],
            "subjects": subjects,
            "tags": tags,
            "dataNodeIdList": dataNodeIdList,
            "credence": yaml_datas['data_add_first']['credence'],
            "authorizationType": yaml_datas['data_add_first']['authorizationType'],
            "browseGraph": yaml_datas['data_add_first']['browseGraph'],
            "license": yaml_datas['data_add_first']['license'],
            "intellectualProp": yaml_datas['data_add_first']['intellectualProp'],
            "source": yaml_datas['data_add_first']['source'],
            "authorName": yaml_datas['data_add_first']['authorName'],
            "authorMail": yaml_datas['data_add_first']['authorMail'],
            "associatedResource": yaml_datas['data_add_first']['associatedResource'],
            "associatedResourceUrl": yaml_datas['data_add_first']['associatedResourceUrl'],
            "intellectualGraph": yaml_datas['data_add_first']['intellectualGraph'],
            "minX": yaml_datas['data_add_first']['minX'],
            "maxX": yaml_datas['data_add_first']['maxX'],
            "minY": yaml_datas['data_add_first']['minY'],
            "maxY": yaml_datas['data_add_first']['maxY'],
            "resolution": yaml_datas['data_add_first']['resolution'],
            "coordinateReferenceSystem": yaml_datas['data_add_first']['coordinateReferenceSystem'],
            "elevation": yaml_datas['data_add_first']['elevation'],
            "geologicTime": yaml_datas['data_add_first']['geologicTime'],
            "geologicAge": yaml_datas['data_add_first']['geologicAge'],
            "geologicalBase": yaml_datas['data_add_first']['geologicalBase'],
            "geologicalTop": yaml_datas['data_add_first']['geologicalTop'],
            "gtsVersion": yaml_datas['data_add_first']['gtsVersion'],
            "baseInfoStatus": yaml_datas['data_add_first']['baseInfoStatus'],
            "spatialInfoStatus": yaml_datas['data_add_first']['spatialInfoStatus'],
            "temporalInfoStatus": yaml_datas['data_add_first']['temporalInfoStatus']
        }
        # 从yaml文件里获取步骤二的请求url
        requests_url_second = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_second']
        # 定义步骤二的请求体
        requests_payload_second = {
            "endpoint": yaml_datas['data_add_second_http']['endpoint'],
            "tls": yaml_datas['data_add_second_http']['tls'],
            "description": yaml_datas['data_add_second_http']['description'],
            "type": yaml_datas['data_add_second_http']['type']
        }
        # 从yaml文件里获取步骤三的请求url
        requests_url_third = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_third']
        # 定义步骤三的请求体
        requests_payload_third = {
            "protocol": yaml_datas['data_add_third_http']['protocol'],
            "method": yaml_datas['data_add_third_http']['method_get'],
            "contentType": yaml_datas['data_add_third_http']['contentType'],
            "path": yaml_datas['data_add_third_http']['path_http'],
            "mockType": yaml_datas['data_add_third_http']['mockType'],
            "mockData": yaml_datas['data_add_third_http']['mockData'],
            "transferProtocol": yaml_datas['data_add_third_http']['transferProtocol'],
            "requestGroovy": yaml_datas['data_add_third_http']['requestGroovy'],
            "responseGroovy": yaml_datas['data_add_third_http']['responseGroovy'],
            "paramOutType": yaml_datas['data_add_third_http']['paramOutType'],
            "paramPath": [
                {
                    "keyword": yaml_datas['data_add_third_http']['paramPath'][0]['keyword'],
                    "must": yaml_datas['data_add_third_http']['paramPath'][0]['must'],
                    "name": yaml_datas['data_add_third_http']['paramPath'][0]['name'],
                    "Description": yaml_datas['data_add_third_http']['paramPath'][0]['Description'],
                    "description": yaml_datas['data_add_third_http']['paramPath'][0]['description']
                }
            ],
            "paramQuery": [
                {
                    "id": yaml_datas['data_add_third_http']['paramQuery'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramQuery'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramQuery'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramQuery'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramQuery'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramQuery'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramQuery'][0]['keyword'],
                }
            ],
            "paramHeader": [
                {
                    "id": yaml_datas['data_add_third_http']['paramHeader'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramHeader'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramHeader'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramHeader'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramHeader'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramHeader'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramHeader'][0]['keyword'],
                }
            ],
            "paramForm": yaml_datas['data_add_third_http']['paramForm'],
            "paramBody": {
                "keyword": yaml_datas['data_add_third_http']['paramBody']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramBody']['name'],
                "type": yaml_datas['data_add_third_http']['paramBody']['type'],
                "must": yaml_datas['data_add_third_http']['paramBody']['must'],
                "description": yaml_datas['data_add_third_http']['paramBody']['description'],
                "children": yaml_datas['data_add_third_http']['paramBody']['children'],
            },
            "paramOut": {
                "keyword": yaml_datas['data_add_third_http']['paramOut']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramOut']['name'],
                "type": yaml_datas['data_add_third_http']['paramOut']['type'],
                "must": yaml_datas['data_add_third_http']['paramOut']['must'],
                "description": yaml_datas['data_add_third_http']['paramOut']['description'],
                "children": yaml_datas['data_add_third_http']['paramOut']['children'],
            },
            "paramBodyType": yaml_datas['data_add_third_http']['paramBodyType'],
            "type": yaml_datas['data_add_third_http']['type']
        }
        # 步骤一发起请求
        res_first = requests.post(requests_url_first, json=requests_payload_first, headers=requests_header)
        # 获取步骤一的firstKey，用作最后一步submit的入参
        firstKey = res_first.json()['data']
        # 步骤二发起请求
        res_second = requests.post(requests_url_second, json=requests_payload_second, headers=requests_header)
        # 获取步骤二的secondKey，用作最后一步submit的入参
        secondKey = res_second.json()['data']
        # 步骤三发起请求
        res_third = requests.post(requests_url_third, json=requests_payload_third, headers=requests_header)
        # 获取步骤三的thirdKey，用作最后一步submit的入参
        thirdKey = res_third.json()['data']
        # 从yaml文件获取submit的请求url
        requests_url_submit = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_submit']
        # 定义submit的入参
        requests_payload_submit = {
            "firstKey": firstKey,
            "secondKey": secondKey,
            "thirdKey": thirdKey
        }
        # 获取发起新增请求前的服务总数量
        datas_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
        # 发起请求
        res_submit = requests.get(requests_url_submit, params=requests_payload_submit, headers=requests_header)
        if res_submit.status_code == 500:
            print("调用内核注册数据服务失败！")
            return "调用内核注册数据服务失败！"
        else:
            # 获取发起新增请求后的服务总数量
            datas_number_after = MysqlExecute().mysql_execute(
                f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
            # 获取新增服务的步骤一、二数据
            api_http_first_and_second = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
            # 获取新增服务步骤三数据
            api_http_third = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_http_first_and_second[0][0]}")
            # 获取新增服务中枢内核Redis中数据
            dataAddress = api_http_first_and_second[0][2]
            api_http_redis_centralsystem = RedisExecute().redis_execute("centralsystem", "select", dataAddress)
            # 获取新增服务数据网络Redis中数据
            api_http_first_redis_data_network = RedisExecute().redis_execute("data_network", "select", firstKey)
            api_http_second_redis_data_network = RedisExecute().redis_execute("data_network", "select", secondKey)
            api_http_third_redis_data_network = RedisExecute().redis_execute("data_network", "select", thirdKey)
            # 返回response的JSON序列化数据，请求前后的服务总数量，用作断言
            return res_submit.json(), datas_number_before, datas_number_after, api_http_first_and_second, api_http_third, api_http_redis_centralsystem, api_http_first_redis_data_network, api_http_second_redis_data_network, api_http_third_redis_data_network

    def data_add_database(self):
        """
        数据服务新增_first: /manager-system-webapi/data/manager/first
        数据服务新增_second: /manager-system-webapi/data/manager/second
        数据服务新增_third: /manager-system-webapi/data/manager/third
        数据服务新增_submit: /manager-system-webapi/data/manager/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 获取步骤一的请求URL
        requests_url_first = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_first']
        # 获取任意一个未删除的学科，用作步骤一的入参
        subjects = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0 order by create_time desc limit 1")
        if subjects == ():
            subjects = []
        else:
            subjects = [
                {
                    "id": subjects[0][0],
                    "level": subjects[0][5],
                    "parent": subjects[0][4],
                    "name": subjects[0][1],
                    "icon": subjects[0][6],
                    "description": subjects[0][2],
                    "count": ""
                }
            ]
        # 获取任意一个未删除的标签，用作步骤一的入参
        tags = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0 order by create_time desc limit 1")
        # 获取未删除的数据节点id
        if tags == ():
            tags = []
        else:
            tags = [
                {
                    "id": tags[0][0],
                    "name": tags[0][1],
                    "description": tags[0][2],
                    "label": tags[0][1],
                    "value": tags[0][0]
                }
            ]
        data_node_id_list = []
        for i in MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0"):
            data_node_id_list.append(i[0])
        # 从所有未删除的数据节点id的列表中随机取两位元素，生成新的列表，作为步骤一的入参
        dataNodeIdList = random.sample(data_node_id_list, 0)
        # 定义步骤一的请求体
        requests_payload_first = {
            "name": yaml_datas['data_add_first']['name_database'],
            "version": yaml_datas['data_add_first']['version'],
            "description": yaml_datas['data_add_first']['description'],
            "subjects": subjects,
            "tags": tags,
            "dataNodeIdList": dataNodeIdList,
            "credence": yaml_datas['data_add_first']['credence'],
            "authorizationType": yaml_datas['data_add_first']['authorizationType'],
            "browseGraph": yaml_datas['data_add_first']['browseGraph'],
            "license": yaml_datas['data_add_first']['license'],
            "intellectualProp": yaml_datas['data_add_first']['intellectualProp'],
            "source": yaml_datas['data_add_first']['source'],
            "authorName": yaml_datas['data_add_first']['authorName'],
            "authorMail": yaml_datas['data_add_first']['authorMail'],
            "associatedResource": yaml_datas['data_add_first']['associatedResource'],
            "associatedResourceUrl": yaml_datas['data_add_first']['associatedResourceUrl'],
            "intellectualGraph": yaml_datas['data_add_first']['intellectualGraph'],
            "minX": yaml_datas['data_add_first']['minX'],
            "maxX": yaml_datas['data_add_first']['maxX'],
            "minY": yaml_datas['data_add_first']['minY'],
            "maxY": yaml_datas['data_add_first']['maxY'],
            "resolution": yaml_datas['data_add_first']['resolution'],
            "coordinateReferenceSystem": yaml_datas['data_add_first']['coordinateReferenceSystem'],
            "elevation": yaml_datas['data_add_first']['elevation'],
            "geologicTime": yaml_datas['data_add_first']['geologicTime'],
            "geologicAge": yaml_datas['data_add_first']['geologicAge'],
            "geologicalBase": yaml_datas['data_add_first']['geologicalBase'],
            "geologicalTop": yaml_datas['data_add_first']['geologicalTop'],
            "gtsVersion": yaml_datas['data_add_first']['gtsVersion'],
            "baseInfoStatus": yaml_datas['data_add_first']['baseInfoStatus'],
            "spatialInfoStatus": yaml_datas['data_add_first']['spatialInfoStatus'],
            "temporalInfoStatus": yaml_datas['data_add_first']['temporalInfoStatus']
        }
        # 从yaml文件里获取请求url
        requests_url_get_connectors = yaml_datas['host'] + yaml_datas['api_url']['获取内核connector']
        # 请求获取中枢内核的connectors
        connectors = requests.post(requests_url_get_connectors, json={}, headers=requests_header)
        if connectors.status_code == 500:
            print("调用内核获取中枢connectors失败！")
        else:
            key = []
            for i in connectors.json()['data']:
                if i['label'] == 'mysql':
                    key.append(i['value'])
                    key.append(i['label'])
            # 获取connectors成功，从yaml文件里得到请求指定connector详情的url
            requests_url_get_connector_detail = yaml_datas['host'] + yaml_datas['api_url']['获取connector详情']
            # 定义请求体
            connector_detail_payload = {
                "key": key[0]
            }
            # 发起请求，获取指定connector的详情，详情字段用作步骤二的入参
            connector_detail = requests.get(requests_url_get_connector_detail, params=connector_detail_payload,
                                            headers=requests_header)
            if connector_detail.status_code == 500:
                print("调用内核获取connector详情出错！")
            else:
                # 从yaml文件里得到步骤二的请求url
                requests_url_second = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_second']
                # 定义步骤二的请求体，其中connectInfoDatabase部分参数是从connector_detail里获取
                requests_payload_second = {
                    "connectorType": key[0],
                    "endpoint": yaml_datas['data_add_second_database']['endpoint'],
                    "tls": yaml_datas['data_add_second_database']['tls'],
                    "description": yaml_datas['data_add_second_database']['description'],
                    "type": yaml_datas['data_add_second_database']['type'],
                    "connectInfoDatabase": [
                        {
                            "key": connector_detail.json()['data'][0]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][0]['value']
                        }, {
                            "key": connector_detail.json()['data'][1]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][1]['value']
                        }, {
                            "key": connector_detail.json()['data'][2]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][2]['value']
                        }, {
                            "key": connector_detail.json()['data'][3]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][3]['value']
                        }, {
                            "key": connector_detail.json()['data'][4]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][4]['value']
                        }, {
                            "key": connector_detail.json()['data'][5]['key'],
                            "value": yaml_datas['data_add_second_database']['connectInfoDatabase'][5]['value']
                        }
                    ]
                }
                # 从yaml文件里获取步骤三的请求url
                requests_url_third = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_third']
                # 定义步骤三的请求体
                requests_payload_third = {
                    "protocol": yaml_datas['data_add_third_http']['protocol'],
                    "method": yaml_datas['data_add_third_http']['method_post'],
                    "contentType": yaml_datas['data_add_third_http']['contentType'],
                    "path": yaml_datas['data_add_third_http']['path_database'],
                    "mockType": yaml_datas['data_add_third_http']['mockType_false'],
                    "transferProtocol": yaml_datas['data_add_third_http']['transferProtocol_database'],
                    "requestGroovy": yaml_datas['data_add_third_http']['requestGroovy'],
                    "responseGroovy": yaml_datas['data_add_third_http']['responseGroovy'],
                    "paramOutType": yaml_datas['data_add_third_http']['paramOutType'],
                    "paramPath": yaml_datas['data_add_third_http']['paramPath_database'],
                    "paramQuery": yaml_datas['data_add_third_http']['paramQuery_database'],
                    "paramHeader": yaml_datas['data_add_third_http']['paramHeader_database'],
                    "paramForm": yaml_datas['data_add_third_http']['paramForm'],
                    "paramBody": {
                        "keyword": yaml_datas['data_add_third_http']['paramBody']['keyword'],
                        "name": yaml_datas['data_add_third_http']['paramBody']['name'],
                        "type": yaml_datas['data_add_third_http']['paramBody']['type'],
                        "must": yaml_datas['data_add_third_http']['paramBody']['must'],
                        "description": yaml_datas['data_add_third_http']['paramBody']['description'],
                        "children": yaml_datas['data_add_third_http']['paramBody']['children'],
                    },
                    "paramOut": {
                        "keyword": yaml_datas['data_add_third_http']['paramOut']['keyword'],
                        "name": yaml_datas['data_add_third_http']['paramOut']['name'],
                        "type": yaml_datas['data_add_third_http']['paramOut']['type'],
                        "must": yaml_datas['data_add_third_http']['paramOut']['must'],
                        "description": yaml_datas['data_add_third_http']['paramOut']['description'],
                        "children": yaml_datas['data_add_third_http']['paramOut']['children'],
                    },
                    "paramBodyType": yaml_datas['data_add_third_http']['paramBodyType'],
                    "type": yaml_datas['data_add_third_http']['type_database']
                }
                # 步骤一，发起请求
                res_first = requests.post(requests_url_first, json=requests_payload_first, headers=requests_header)
                # 得到步骤一的firstKey，作为最后一步submit的入参
                firstKey = res_first.json()['data']
                # 步骤二，发起请求
                res_second = requests.post(requests_url_second, json=requests_payload_second, headers=requests_header)
                # 得到步骤二的secondKey，作为最后一步submit的入参
                secondKey = res_second.json()['data']
                # 步骤三，发起请求
                res_third = requests.post(requests_url_third, json=requests_payload_third, headers=requests_header)
                # 得到步骤三的thirdKey，作为最后一步submit的入参
                thirdKey = res_third.json()['data']
                # 从yaml文件里得到submit的请求url
                requests_url_submit = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_submit']
                # 定义submit的请求体
                requests_payload_submit = {
                    "firstKey": firstKey,
                    "secondKey": secondKey,
                    "thirdKey": thirdKey
                }
                # 获取请求之前服务总数
                datas_number_before = MysqlExecute().mysql_execute(
                    f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
                res_submit = requests.get(requests_url_submit, params=requests_payload_submit, headers=requests_header)
                if res_submit.status_code == 500:
                    print("调用内核注册数据服务失败！")
                    return "调用内核注册数据服务失败！"
                else:
                    # 获取发起新增请求后的服务总数量
                    datas_number_after = MysqlExecute().mysql_execute(
                        f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
                    # 获取新增服务的步骤一、二数据
                    api_http_first_and_second = MysqlExecute().mysql_execute(
                        f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
                    # 获取新增服务步骤三数据
                    api_http_third = MysqlExecute().mysql_execute(
                        f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_http_first_and_second[0][0]}")
                    # 获取新增服务中枢内核Redis中数据
                    dataAddress = api_http_first_and_second[0][2]
                    api_http_redis_centralsystem = RedisExecute().redis_execute("centralsystem", "select", dataAddress)
                    # 获取新增服务数据网络Redis中数据
                    api_http_first_redis_data_network = RedisExecute().redis_execute("data_network", "select", firstKey)
                    api_http_second_redis_data_network = RedisExecute().redis_execute("data_network", "select",
                                                                                      secondKey)
                    api_http_third_redis_data_network = RedisExecute().redis_execute("data_network", "select", thirdKey)
                    # 返回response的JSON序列化数据，请求前后的服务总数量，用作断言
                    return res_submit.json(), datas_number_before, datas_number_after, api_http_first_and_second, api_http_third, api_http_redis_centralsystem, api_http_first_redis_data_network, api_http_second_redis_data_network, api_http_third_redis_data_network

    def data_add_map(self):
        """
        数据服务新增_first: /manager-system-webapi/data/manager/first
        数据服务新增_second: /manager-system-webapi/data/manager/second
        数据服务新增_third: /manager-system-webapi/data/manager/third
        数据服务新增_submit: /manager-system-webapi/data/manager/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 获取步骤一的请求URL
        requests_url_first = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_first']
        # 获取任意一个未删除的学科，用作步骤一的入参
        subjects = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0 order by create_time desc limit 1")
        if subjects == ():
            subjects = []
        else:
            subjects = [
                {
                    "id": subjects[0][0],
                    "level": subjects[0][5],
                    "parent": subjects[0][4],
                    "name": subjects[0][1],
                    "icon": subjects[0][6],
                    "description": subjects[0][2],
                    "count": ""
                }
            ]
        # 获取任意一个未删除的标签，用作步骤一的入参
        tags = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0 order by create_time desc limit 1")
        # 获取未删除的数据节点id
        if tags == ():
            tags = []
        else:
            tags = [
                {
                    "id": tags[0][0],
                    "name": tags[0][1],
                    "description": tags[0][2],
                    "label": tags[0][1],
                    "value": tags[0][0]
                }
            ]
        data_node_id_list = []
        for i in MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0"):
            data_node_id_list.append(i[0])
        # 从所有未删除的数据节点id的列表中随机取两位元素，生成新的列表，作为步骤一的入参
        dataNodeIdList = random.sample(data_node_id_list, 0)
        requests_payload_first = {
            "name": yaml_datas['data_add_first']['name_map'],
            "version": yaml_datas['data_add_first']['version'],
            "description": yaml_datas['data_add_first']['description'],
            "subjects": subjects,
            "tags": tags,
            "dataNodeIdList": dataNodeIdList,
            "credence": yaml_datas['data_add_first']['credence'],
            "authorizationType": yaml_datas['data_add_first']['authorizationType'],
            "browseGraph": yaml_datas['data_add_first']['browseGraph'],
            "license": yaml_datas['data_add_first']['license'],
            "intellectualProp": yaml_datas['data_add_first']['intellectualProp'],
            "source": yaml_datas['data_add_first']['source'],
            "authorName": yaml_datas['data_add_first']['authorName'],
            "authorMail": yaml_datas['data_add_first']['authorMail'],
            "associatedResource": yaml_datas['data_add_first']['associatedResource'],
            "associatedResourceUrl": yaml_datas['data_add_first']['associatedResourceUrl'],
            "intellectualGraph": yaml_datas['data_add_first']['intellectualGraph'],
            "minX": yaml_datas['data_add_first']['minX'],
            "maxX": yaml_datas['data_add_first']['maxX'],
            "minY": yaml_datas['data_add_first']['minY'],
            "maxY": yaml_datas['data_add_first']['maxY'],
            "resolution": yaml_datas['data_add_first']['resolution'],
            "coordinateReferenceSystem": yaml_datas['data_add_first']['coordinateReferenceSystem'],
            "elevation": yaml_datas['data_add_first']['elevation'],
            "geologicTime": yaml_datas['data_add_first']['geologicTime'],
            "geologicAge": yaml_datas['data_add_first']['geologicAge'],
            "geologicalBase": yaml_datas['data_add_first']['geologicalBase'],
            "geologicalTop": yaml_datas['data_add_first']['geologicalTop'],
            "gtsVersion": yaml_datas['data_add_first']['gtsVersion'],
            "baseInfoStatus": yaml_datas['data_add_first']['baseInfoStatus'],
            "spatialInfoStatus": yaml_datas['data_add_first']['spatialInfoStatus'],
            "temporalInfoStatus": yaml_datas['data_add_first']['temporalInfoStatus']
        }
        # 根据map类型以及版本号获取map详情，作为步骤二入参
        requests_url_get_map_detail = yaml_datas['host'] + yaml_datas['api_url']['获取map详情']
        map_detail_WMS = requests.get(requests_url_get_map_detail, params={"version": "WMS 1.1.1"},
                                      headers=requests_header)
        map_detail_WMTS = requests.get(requests_url_get_map_detail, params={"version": "WMTS1.0.0"},
                                       headers=requests_header)
        map_detail_WFS = requests.get(requests_url_get_map_detail, params={"version": "WFS 2.0.0"},
                                      headers=requests_header)
        map_detail_TFS = requests.get(requests_url_get_map_detail, params={"version": "TMS 1.0.0"},
                                      headers=requests_header)
        # 从yaml文件里获取步骤二的请求url
        requests_url_second = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_second']
        # 定义步骤二的请求体
        requests_payload_second = {
            "description": yaml_datas['data_add_second_map']['description'],
            "endpoint": yaml_datas['data_add_second_map']['endpoint'],
            "gisProtocol": yaml_datas['data_add_second_map']['gisProtocol'],
            "mapInfoList": [{
                "mapProtocol": yaml_datas['data_add_second_map']['mapInfoList'][0]['mapProtocol'],
                "version": yaml_datas['data_add_second_map']['mapInfoList'][0]['version'],
                "requestList": map_detail_WMS.json()['data']
            }, {
                "mapProtocol": yaml_datas['data_add_second_map']['mapInfoList'][1]['mapProtocol'],
                "version": yaml_datas['data_add_second_map']['mapInfoList'][1]['version'],
                "requestList": map_detail_WMTS.json()['data']
            }, {
                "mapProtocol": yaml_datas['data_add_second_map']['mapInfoList'][2]['mapProtocol'],
                "version": yaml_datas['data_add_second_map']['mapInfoList'][2]['version'],
                "requestList": map_detail_WFS.json()['data']
            }, {
                "mapProtocol": yaml_datas['data_add_second_map']['mapInfoList'][3]['mapProtocol'],
                "version": yaml_datas['data_add_second_map']['mapInfoList'][3]['version'],
                "requestList": map_detail_TFS.json()['data']
            }],
            "mapProtocolList": yaml_datas['data_add_second_map']['mapProtocolList'],
            "path": yaml_datas['data_add_second_map']['path'],
            "tls": yaml_datas['data_add_second_map']['tls'],
            "type": yaml_datas['data_add_second_map']['type']
        }
        # 步骤一发起请求
        res_first = requests.post(requests_url_first, json=requests_payload_first, headers=requests_header)
        # 得到步骤一的firstKey，用作submit的入参
        firstKey = res_first.json()['data']
        # 步骤二发起请求
        res_second = requests.post(requests_url_second, json=requests_payload_second, headers=requests_header)
        # 得到步骤二的secondKey，用作submit的入参
        secondKey = res_second.json()['data']
        # 从yaml文件里的到submit的请求url
        requests_url_submit = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_submit']
        # 定义submit的请求体
        requests_payload_submit = {
            "firstKey": firstKey,
            "secondKey": secondKey
        }
        # 获取请求之前的数据服务总数量
        datas_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
        res_submit = requests.get(requests_url_submit, params=requests_payload_submit, headers=requests_header)
        if res_submit.status_code == 500:
            print("调用内核注册数据服务失败！")
            return "调用内核注册数据服务失败！"
        else:
            # 获取发起新增请求后的服务总数量
            datas_number_after = MysqlExecute().mysql_execute(
                f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
            # 获取新增服务的步骤一、二数据
            api_http_first_and_second = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
            # 获取新增服务步骤三数据
            api_http_third = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_http_first_and_second[0][0]}")
            # 获取新增服务中枢内核Redis中数据
            dataAddress = api_http_first_and_second[0][2]
            api_http_redis_centralsystem = RedisExecute().redis_execute("centralsystem", "select", dataAddress)
            # 获取新增服务数据网络Redis中数据
            api_http_first_redis_data_network = RedisExecute().redis_execute("data_network", "select", firstKey)
            api_http_second_redis_data_network = RedisExecute().redis_execute("data_network", "select", secondKey)
            # 返回response的JSON序列化数据，请求前后的服务总数量，用作断言
            return res_submit.json(), datas_number_before, datas_number_after, api_http_first_and_second, api_http_third, api_http_redis_centralsystem, api_http_first_redis_data_network, api_http_second_redis_data_network

    def data_add_imagery(self):
        """
        数据服务新增_first: /manager-system-webapi/data/manager/first
        数据服务新增_second: /manager-system-webapi/data/manager/second
        数据服务新增_third: /manager-system-webapi/data/manager/third
        数据服务新增_submit: /manager-system-webapi/data/manager/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 获取步骤一的请求URL
        requests_url_first = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_first']
        # 获取任意一个未删除的学科，用作步骤一的入参
        subjects = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0 order by create_time desc limit 1")
        if subjects == ():
            subjects = []
        else:
            subjects = [
                {
                    "id": subjects[0][0],
                    "level": subjects[0][5],
                    "parent": subjects[0][4],
                    "name": subjects[0][1],
                    "icon": subjects[0][6],
                    "description": subjects[0][2],
                    "count": ""
                }
            ]
        # 获取任意一个未删除的标签，用作步骤一的入参
        tags = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0 order by create_time desc limit 1")
        # 获取未删除的数据节点id
        if tags == ():
            tags = []
        else:
            tags = [
                {
                    "id": tags[0][0],
                    "name": tags[0][1],
                    "description": tags[0][2],
                    "label": tags[0][1],
                    "value": tags[0][0]
                }
            ]
        data_node_id_list = []
        for i in MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0"):
            data_node_id_list.append(i[0])
        # 从所有未删除的数据节点id的列表中随机取两位元素，生成新的列表，作为步骤一的入参
        dataNodeIdList = random.sample(data_node_id_list, 0)
        # 定义步骤一的请求体
        requests_payload_first = {
            "name": yaml_datas['data_add_first']['name_imagery'],
            "version": yaml_datas['data_add_first']['version'],
            "description": yaml_datas['data_add_first']['description'],
            "subjects": subjects,
            "tags": tags,
            "dataNodeIdList": dataNodeIdList,
            "credence": yaml_datas['data_add_first']['credence'],
            "authorizationType": yaml_datas['data_add_first']['authorizationType'],
            "browseGraph": yaml_datas['data_add_first']['browseGraph'],
            "license": yaml_datas['data_add_first']['license'],
            "intellectualProp": yaml_datas['data_add_first']['intellectualProp'],
            "source": yaml_datas['data_add_first']['source'],
            "authorName": yaml_datas['data_add_first']['authorName'],
            "authorMail": yaml_datas['data_add_first']['authorMail'],
            "associatedResource": yaml_datas['data_add_first']['associatedResource'],
            "associatedResourceUrl": yaml_datas['data_add_first']['associatedResourceUrl'],
            "intellectualGraph": yaml_datas['data_add_first']['intellectualGraph'],
            "minX": yaml_datas['data_add_first']['minX'],
            "maxX": yaml_datas['data_add_first']['maxX'],
            "minY": yaml_datas['data_add_first']['minY'],
            "maxY": yaml_datas['data_add_first']['maxY'],
            "resolution": yaml_datas['data_add_first']['resolution'],
            "coordinateReferenceSystem": yaml_datas['data_add_first']['coordinateReferenceSystem'],
            "elevation": yaml_datas['data_add_first']['elevation'],
            "geologicTime": yaml_datas['data_add_first']['geologicTime'],
            "geologicAge": yaml_datas['data_add_first']['geologicAge'],
            "geologicalBase": yaml_datas['data_add_first']['geologicalBase'],
            "geologicalTop": yaml_datas['data_add_first']['geologicalTop'],
            "gtsVersion": yaml_datas['data_add_first']['gtsVersion'],
            "baseInfoStatus": yaml_datas['data_add_first']['baseInfoStatus'],
            "spatialInfoStatus": yaml_datas['data_add_first']['spatialInfoStatus'],
            "temporalInfoStatus": yaml_datas['data_add_first']['temporalInfoStatus']
        }
        # 从yaml文件里获取步骤二的请求url
        requests_url_second = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_second']
        # 定义步骤二的请求体
        requests_payload_second = {
            "serviceType": yaml_datas['data_add_second_imagery']['serviceType'],
            "endpoint": yaml_datas['data_add_second_imagery']['endpoint'],
            "tls": yaml_datas['data_add_second_imagery']['tls'],
            "description": yaml_datas['data_add_second_imagery']['description'],
            "type": yaml_datas['data_add_second_imagery']['type']
        }
        # 从yaml文件里获取步骤三的请求URL
        requests_url_third = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_third']
        # 定义步骤三的请求体
        requests_payload_third = {
            "protocol": yaml_datas['data_add_third_http']['protocol'],
            "method": yaml_datas['data_add_third_http']['method_get'],
            "contentType": yaml_datas['data_add_third_http']['contentType_urlencoded'],
            "path": yaml_datas['data_add_third_http']['path_imagery'],
            "mockType": yaml_datas['data_add_third_http']['mockType'],
            "mockData": yaml_datas['data_add_third_http']['mockData'],
            "transferProtocol": yaml_datas['data_add_third_http']['transferProtocol'],
            "requestGroovy": yaml_datas['data_add_third_http']['requestGroovy'],
            "responseGroovy": yaml_datas['data_add_third_http']['responseGroovy'],
            "paramOutType": yaml_datas['data_add_third_http']['paramOutType'],
            "paramPath": [
                {
                    "keyword": yaml_datas['data_add_third_http']['paramPath'][0]['keyword'],
                    "must": yaml_datas['data_add_third_http']['paramPath'][0]['must'],
                    "name": yaml_datas['data_add_third_http']['paramPath'][0]['name'],
                    "Description": yaml_datas['data_add_third_http']['paramPath'][0]['Description'],
                    "description": yaml_datas['data_add_third_http']['paramPath'][0]['description']
                }
            ],
            "paramQuery": [
                {
                    "id": yaml_datas['data_add_third_http']['paramQuery'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramQuery'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramQuery'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramQuery'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramQuery'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramQuery'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramQuery'][0]['keyword'],
                }
            ],
            "paramHeader": [
                {
                    "id": yaml_datas['data_add_third_http']['paramHeader'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramHeader'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramHeader'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramHeader'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramHeader'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramHeader'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramHeader'][0]['keyword'],
                }
            ],
            "paramForm": yaml_datas['data_add_third_http']['paramForm'],
            "paramBody": {
                "keyword": yaml_datas['data_add_third_http']['paramBody']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramBody']['name'],
                "type": yaml_datas['data_add_third_http']['paramBody']['type'],
                "must": yaml_datas['data_add_third_http']['paramBody']['must'],
                "description": yaml_datas['data_add_third_http']['paramBody']['description'],
                "children": yaml_datas['data_add_third_http']['paramBody']['children'],
            },
            "paramOut": {
                "keyword": yaml_datas['data_add_third_http']['paramOut']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramOut']['name'],
                "type": yaml_datas['data_add_third_http']['paramOut']['type'],
                "must": yaml_datas['data_add_third_http']['paramOut']['must'],
                "description": yaml_datas['data_add_third_http']['paramOut']['description'],
                "children": yaml_datas['data_add_third_http']['paramOut']['children'],
            },
            "paramBodyType": yaml_datas['data_add_third_http']['paramBodyType'],
            "type": yaml_datas['data_add_third_http']['type']
        }
        # 步骤一发起请求
        res_first = requests.post(requests_url_first, json=requests_payload_first, headers=requests_header)
        # 得到步骤一的firstKey，用作submit的入参
        firstKey = res_first.json()['data']
        # 步骤二发起请求
        res_second = requests.post(requests_url_second, json=requests_payload_second, headers=requests_header)
        # 得到步骤二的secondKey，用作submit的入参
        secondKey = res_second.json()['data']
        # 步骤三发起请求
        res_third = requests.post(requests_url_third, json=requests_payload_third, headers=requests_header)
        # 得到步骤三的thirdKey，用作submit的入参
        thirdKey = res_third.json()['data']
        # 从yaml文件里得到submit的请求URL
        requests_url_submit = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_submit']
        # 定义submit的请求体
        requests_payload_submit = {
            "firstKey": firstKey,
            "secondKey": secondKey,
            "thirdKey": thirdKey
        }
        # 获取发起请求之前的服务总数量
        datas_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
        # 发起新增服务
        res_submit = requests.get(requests_url_submit, params=requests_payload_submit, headers=requests_header)
        if res_submit.status_code == 500:
            print("调用内核注册数据服务失败！")
            return "调用内核注册数据服务失败！"
        else:
            # 获取发起新增请求后的服务总数量
            datas_number_after = MysqlExecute().mysql_execute(
                f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
            # 获取新增服务的步骤一、二数据
            api_http_first_and_second = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
            # 获取新增服务步骤三数据
            api_http_third = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_http_first_and_second[0][0]}")
            # 获取新增服务中枢内核Redis中数据
            dataAddress = api_http_first_and_second[0][2]
            api_http_redis_centralsystem = RedisExecute().redis_execute("centralsystem", "select", dataAddress)
            # 获取新增服务数据网络Redis中数据
            api_http_first_redis_data_network = RedisExecute().redis_execute("data_network", "select", firstKey)
            api_http_second_redis_data_network = RedisExecute().redis_execute("data_network", "select", secondKey)
            api_http_third_redis_data_network = RedisExecute().redis_execute("data_network", "select", thirdKey)
            # 返回response的JSON序列化数据，请求前后的服务总数量，用作断言
            return res_submit.json(), datas_number_before, datas_number_after, api_http_first_and_second, api_http_third, api_http_redis_centralsystem, api_http_first_redis_data_network, api_http_second_redis_data_network, api_http_third_redis_data_network

    def data_add_linkdata(self):
        """
        数据服务新增_first: /manager-system-webapi/data/manager/first
        数据服务新增_second: /manager-system-webapi/data/manager/second
        数据服务新增_third: /manager-system-webapi/data/manager/third
        数据服务新增_submit: /manager-system-webapi/data/manager/add
        :return:
        """
        # 从继承类Basic中获取类属性：yaml_datas
        yaml_datas = self.yaml_datas
        # 从继承类GetLoginToken里获取类属性：requests_header
        requests_header = {"Authorization": self.get_login_token()['data']['token']}
        # 获取步骤一的请求URL
        requests_url_first = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_first']
        # 获取任意一个未删除的学科，用作步骤一的入参
        subjects = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_subject where deleted = 0 order by create_time desc limit 1")
        if subjects == ():
            subjects = []
        else:
            subjects = [
                {
                    "id": subjects[0][0],
                    "level": subjects[0][5],
                    "parent": subjects[0][4],
                    "name": subjects[0][1],
                    "icon": subjects[0][6],
                    "description": subjects[0][2],
                    "count": ""
                }
            ]
        # 获取任意一个未删除的标签，用作步骤一的入参
        tags = MysqlExecute().mysql_execute(
            f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_tag where deleted = 0 order by create_time desc limit 1")
        # 获取未删除的数据节点id
        if tags == ():
            tags = []
        else:
            tags = [
                {
                    "id": tags[0][0],
                    "name": tags[0][1],
                    "description": tags[0][2],
                    "label": tags[0][1],
                    "value": tags[0][0]
                }
            ]
        data_node_id_list = []
        for i in MysqlExecute().mysql_execute(
                f"select id from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_node where deleted = 0"):
            data_node_id_list.append(i[0])
        # 从所有未删除的数据节点id的列表中随机取两位元素，生成新的列表，作为步骤一的入参
        dataNodeIdList = random.sample(data_node_id_list, 0)
        # 定义步骤一的请求体
        requests_payload_first = {
            "name": yaml_datas['data_add_first']['name_linkdata'],
            "version": yaml_datas['data_add_first']['version'],
            "description": yaml_datas['data_add_first']['description'],
            "subjects": subjects,
            "tags": tags,
            "dataNodeIdList": dataNodeIdList,
            "credence": yaml_datas['data_add_first']['credence'],
            "authorizationType": yaml_datas['data_add_first']['authorizationType'],
            "browseGraph": yaml_datas['data_add_first']['browseGraph'],
            "license": yaml_datas['data_add_first']['license'],
            "intellectualProp": yaml_datas['data_add_first']['intellectualProp'],
            "source": yaml_datas['data_add_first']['source'],
            "authorName": yaml_datas['data_add_first']['authorName'],
            "authorMail": yaml_datas['data_add_first']['authorMail'],
            "associatedResource": yaml_datas['data_add_first']['associatedResource'],
            "associatedResourceUrl": yaml_datas['data_add_first']['associatedResourceUrl'],
            "intellectualGraph": yaml_datas['data_add_first']['intellectualGraph'],
            "minX": yaml_datas['data_add_first']['minX'],
            "maxX": yaml_datas['data_add_first']['maxX'],
            "minY": yaml_datas['data_add_first']['minY'],
            "maxY": yaml_datas['data_add_first']['maxY'],
            "resolution": yaml_datas['data_add_first']['resolution'],
            "coordinateReferenceSystem": yaml_datas['data_add_first']['coordinateReferenceSystem'],
            "elevation": yaml_datas['data_add_first']['elevation'],
            "geologicTime": yaml_datas['data_add_first']['geologicTime'],
            "geologicAge": yaml_datas['data_add_first']['geologicAge'],
            "geologicalBase": yaml_datas['data_add_first']['geologicalBase'],
            "geologicalTop": yaml_datas['data_add_first']['geologicalTop'],
            "gtsVersion": yaml_datas['data_add_first']['gtsVersion'],
            "baseInfoStatus": yaml_datas['data_add_first']['baseInfoStatus'],
            "spatialInfoStatus": yaml_datas['data_add_first']['spatialInfoStatus'],
            "temporalInfoStatus": yaml_datas['data_add_first']['temporalInfoStatus']
        }
        # 从yaml文件里获取步骤二的请求URL
        requests_url_second = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_second']
        # 定义步骤二的请求体
        requests_payload_second = {
            "description": yaml_datas['data_add_second_linkdata']['description'],
            "doi": yaml_datas['data_add_second_linkdata']['doi'],
            "endpoint": yaml_datas['data_add_second_linkdata']['endpoint'],
            "fileSize": yaml_datas['data_add_second_linkdata']['fileSize'],
            "fileType": yaml_datas['data_add_second_linkdata']['fileType'],
            "linkType": yaml_datas['data_add_second_linkdata']['linkType'],
            "records": yaml_datas['data_add_second_linkdata']['records'],
            "subDataType": yaml_datas['data_add_second_linkdata']['subDataType'],
            "tls": yaml_datas['data_add_second_linkdata']['tls'],
            "type": yaml_datas['data_add_second_linkdata']['type']
        }
        # 从yaml文件里获取步骤三的请求url
        requests_url_third = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_third']
        # 定义步骤三的请求体
        requests_payload_third = {
            "protocol": yaml_datas['data_add_third_http']['protocol'],
            "method": yaml_datas['data_add_third_http']['method_get'],
            "contentType": yaml_datas['data_add_third_http']['contentType'],
            "path": yaml_datas['data_add_third_http']['path_linkdata'],
            "mockType": yaml_datas['data_add_third_http']['mockType'],
            "mockData": yaml_datas['data_add_third_http']['mockData'],
            "transferProtocol": yaml_datas['data_add_third_http']['transferProtocol'],
            "requestGroovy": yaml_datas['data_add_third_http']['requestGroovy'],
            "responseGroovy": yaml_datas['data_add_third_http']['responseGroovy'],
            "paramOutType": yaml_datas['data_add_third_http']['paramOutType'],
            "paramPath": [
                {
                    "keyword": yaml_datas['data_add_third_http']['paramPath'][0]['keyword'],
                    "must": yaml_datas['data_add_third_http']['paramPath'][0]['must'],
                    "name": yaml_datas['data_add_third_http']['paramPath'][0]['name'],
                    "Description": yaml_datas['data_add_third_http']['paramPath'][0]['Description'],
                    "description": yaml_datas['data_add_third_http']['paramPath'][0]['description']
                }
            ],
            "paramQuery": [
                {
                    "id": yaml_datas['data_add_third_http']['paramQuery'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramQuery'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramQuery'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramQuery'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramQuery'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramQuery'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramQuery'][0]['keyword'],
                }
            ],
            "paramHeader": [
                {
                    "id": yaml_datas['data_add_third_http']['paramHeader'][0]['id'],
                    "title": yaml_datas['data_add_third_http']['paramHeader'][0]['title'],
                    "must": yaml_datas['data_add_third_http']['paramHeader'][0]['must'],
                    "type": yaml_datas['data_add_third_http']['paramHeader'][0]['type'],
                    "name": yaml_datas['data_add_third_http']['paramHeader'][0]['name'],
                    "description": yaml_datas['data_add_third_http']['paramHeader'][0]['description'],
                    "keyword": yaml_datas['data_add_third_http']['paramHeader'][0]['keyword'],
                }
            ],
            "paramForm": yaml_datas['data_add_third_http']['paramForm'],
            "paramBody": {
                "keyword": yaml_datas['data_add_third_http']['paramBody']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramBody']['name'],
                "type": yaml_datas['data_add_third_http']['paramBody']['type'],
                "must": yaml_datas['data_add_third_http']['paramBody']['must'],
                "description": yaml_datas['data_add_third_http']['paramBody']['description'],
                "children": yaml_datas['data_add_third_http']['paramBody']['children'],
            },
            "paramOut": {
                "keyword": yaml_datas['data_add_third_http']['paramOut']['keyword'],
                "name": yaml_datas['data_add_third_http']['paramOut']['name'],
                "type": yaml_datas['data_add_third_http']['paramOut']['type'],
                "must": yaml_datas['data_add_third_http']['paramOut']['must'],
                "description": yaml_datas['data_add_third_http']['paramOut']['description'],
                "children": yaml_datas['data_add_third_http']['paramOut']['children'],
            },
            "paramBodyType": yaml_datas['data_add_third_http']['paramBodyType'],
            "type": yaml_datas['data_add_third_http']['type']
        }
        # 步骤一发起请求
        res_first = requests.post(requests_url_first, json=requests_payload_first, headers=requests_header)
        # 得到步骤一的firstKey，用作submit的入参
        firstKey = res_first.json()['data']
        # 步骤二发起请求
        res_second = requests.post(requests_url_second, json=requests_payload_second, headers=requests_header)
        # 得到步骤二的secondKey，用作submit的入参
        secondKey = res_second.json()['data']
        # 步骤三发起请求
        res_third = requests.post(requests_url_third, json=requests_payload_third, headers=requests_header)
        # 得到步骤三的thirdKey，用作submit的入参
        thirdKey = res_third.json()['data']
        # 从yaml文件里得到submit的请求URL
        requests_url_submit = yaml_datas['host'] + yaml_datas['api_url']['数据服务新增_submit']
        # 定义submit的请求体
        requests_payload_submit = {
            "firstKey": firstKey,
            "secondKey": secondKey,
            "thirdKey": thirdKey
        }
        # 获取请求之前的服务总数量
        datas_number_before = MysqlExecute().mysql_execute(
            f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
        # 发起新增请求
        res_submit = requests.get(requests_url_submit, params=requests_payload_submit, headers=requests_header)
        if res_submit.status_code == 500:
            print("调用内核注册数据服务失败！")
            return "调用内核注册数据服务失败！"
        else:
            # 获取发起新增请求后的服务总数量
            datas_number_after = MysqlExecute().mysql_execute(
                f"select count(*) from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where deleted = 0")
            # 获取新增服务的步骤一、二数据
            api_http_first_and_second = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_info where name in ('Data_name_http_add_auto_test','Data_name_database_add_auto_test','Data_name_imagery_add_auto_test','Data_name_map_add_auto_test','Data_name_linkdata_add_auto_test')")
            # 获取新增服务步骤三数据
            api_http_third = MysqlExecute().mysql_execute(
                f"select * from {yaml_datas['mysql_hz_prod']['database_name']}.d_data_manager_api where id = {api_http_first_and_second[0][0]}")
            # 获取新增服务中枢内核Redis中数据
            dataAddress = api_http_first_and_second[0][2]
            api_http_redis_centralsystem = RedisExecute().redis_execute("centralsystem", "select", dataAddress)
            # 获取新增服务数据网络Redis中数据
            api_http_first_redis_data_network = RedisExecute().redis_execute("data_network", "select", firstKey)
            api_http_second_redis_data_network = RedisExecute().redis_execute("data_network", "select", secondKey)
            api_http_third_redis_data_network = RedisExecute().redis_execute("data_network", "select", thirdKey)
            # 返回response的JSON序列化数据，请求前后的服务总数量，用作断言
            return res_submit.json(), datas_number_before, datas_number_after, api_http_first_and_second, api_http_third, api_http_redis_centralsystem, api_http_first_redis_data_network, api_http_second_redis_data_network, api_http_third_redis_data_network

