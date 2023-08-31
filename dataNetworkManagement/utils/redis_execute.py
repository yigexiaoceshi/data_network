#!/usr/bin/python3
# -*- coding:utf-8 -*-
import redis
import json
from dataNetworkManagement.utils.get_yaml_datas import GetYamlDatas

yaml_datas = GetYamlDatas().get_yaml_datas()
class RedisExecute():
    yaml_datas = GetYamlDatas().get_yaml_datas()

    def redis_execute(self, redis_type, operation_type, *args):
        """
        Redis操作
        :param redis_type:传入data_network连接数据网络杭州prod节点Redis，传入centralsystem连接DDE中枢杭州生产Redis
        :param operation_type: 传入select操作查询，传入delete操作测试数据清除
        :param args: 操作数据网络Redis时，可不传*args；操作中枢Redis须传入数据服务的dpAddress
        :return:
        """
        yaml_datas = self.yaml_datas
        if redis_type == 'data_network':
            try:
                # 连接到数据网络Redis
                redis_connector = redis.Redis(host=yaml_datas['redis_hz_prod_data_network']['host'],
                                              port=yaml_datas['redis_hz_prod_data_network']['port'],
                                              username=yaml_datas['redis_hz_prod_data_network']['username'],
                                              password=yaml_datas['redis_hz_prod_data_network']['password'],
                                              db=yaml_datas['redis_hz_prod_data_network']['db'],
                                              decode_responses=True, encoding="utf-8")
                # 获取所有的key，返回列表，key为列表中的元素，为字符串类型
                # all_keys = redis_connector.keys("*")
                # print("所有的key为:",all_keys)
                keys = redis_connector.keys(f"{args[0]}*")
                if len(keys) > 0:
                    if operation_type == "select":
                        result = []
                        for key in keys:
                            redis_value_str = redis_connector.get(key)
                            redis_value_dict = json.loads(redis_value_str)
                            result.append(redis_value_dict)
                        return result
                    elif operation_type == "delete":
                        # 删除该key
                        redis_connector.delete(*keys)
                else:
                    print(f"key'{keys}'在Redis中不存在！")
            except redis.exceptions.ConnectionError as redis_error:
                print(f"连接Redis失败，错误为：{redis_error}")
        elif redis_type == "centralsystem":
            try:
                # 连接到中枢Redis
                redis_connector = redis.Redis(host=yaml_datas['redis_hz_prod_centralsystem']['host'],
                                              port=yaml_datas['redis_hz_prod_centralsystem']['port'],
                                              username=yaml_datas['redis_hz_prod_centralsystem']['username'],
                                              password=yaml_datas['redis_hz_prod_centralsystem']['password'],
                                              db=yaml_datas['redis_hz_prod_centralsystem']['db'],
                                              decode_responses=True, encoding="utf-8")
                # 获取所有的key，返回列表，key为列表中的元素，为字符串类型
                # all_keys = redis_connector.keys("*")
                # print("所有的key为:",all_keys)
                keys = redis_connector.keys(f"*{args[0]}")
                if len(keys) > 0:
                    if operation_type == "select":
                        redis_value_str = redis_connector.get(keys[0])
                        redis_value_dict = json.loads(redis_value_str)
                        return redis_value_dict
                    elif operation_type == "delete":
                        # 删除该key
                        redis_connector.delete(keys[0])
                else:
                    print(f"key'{keys}'在Redis中不存在！")
            except redis.exceptions.ConnectionError as redis_error:
                print(f"连接Redis失败，错误为：{redis_error}")