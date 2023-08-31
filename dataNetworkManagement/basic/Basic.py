#!/usr/bin/python3
# -*- coding:utf-8 -*-
from dataNetworkManagement.utils.get_yaml_datas import GetYamlDatas
from dataNetworkManagement.utils.get_excel_datas import GetExcelDatas
from dataNetworkManagement.utils.get_four_randoms import GetFourRandoms


class Basic():
    yaml_datas = GetYamlDatas().get_yaml_datas()
    excel_datas = GetExcelDatas().get_excel_datas()
    four_randoms = GetFourRandoms().get_four_randoms()
