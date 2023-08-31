#!/usr/bin/python3
# -*- coding:utf-8 -*-
import yaml
import os

# 获取yaml文件所在路径
# os.getcwd():获取当前文件所在目录
# os.path.dirname(a)，获取目录a的父级目录
yaml_path = os.path.dirname(os.getcwd()) + '/datas' + '/data_network.yaml'


class GetYamlDatas():

    def get_yaml_datas(self):
        """
        读取yaml文件的数据
        :return:返回文件流
        """
        # 打开yaml文件，定义别名为yaml_file
        with open(yaml_path, 'r') as yaml_file:
            # 读取yaml文件
            yaml_datas = yaml.load(yaml_file, Loader=yaml.FullLoader)
            # 将获取到的文件流返回，并自动关闭yaml文件
            return yaml_datas