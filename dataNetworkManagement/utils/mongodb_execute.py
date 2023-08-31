#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymongo
from pymongo import MongoClient
from dataNetworkManagement.basic.Basic import Basic


class MongoExecute(Basic):

    def mongo_execute(self, database_name, collection_name, key, value):
        # try:
            # 创建连接1
            connector = pymongo.MongoClient(yaml_datas['mongodb']['hk_test_uri'])
            # 创建连接2
            # connector = MongoClient(mongo_uri)
            """
            # 获取所有数据库
            all_db = connector.list_database_names()
            # 获取指定数据库的所有集合
            # all_collection = connector['database_name'].list_collection_names()
            # 获取一行数据
            # result = collection.find_one({})
            """
            db = connector[database_name]
            coll = db[collection_name]
            result = coll.find({key: value})
            for document in result:
                return document
        # except:
        #     print("连接失败")


a = MongoExecute().mongo_execute('centralsystem','service_manage','dpAddress','1773AB747F021000')
print(a)