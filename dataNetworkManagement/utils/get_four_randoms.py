#!/usr/bin/python3
# -*- coding:utf-8 -*-
import random

# 获取四位随机字母和数字组合的初始数据
initial_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
# 获取四位随机数字的初始数据
initial_number = '0123456789'


class GetFourRandoms():

    def get_four_randoms(self):
        """
        获取四位随机字母和数字组合
        获取四位随机数字
        :return:
        """
        # 定义一个空字符串
        random_string = ''
        # 定义一个空字符串
        random_number = ''
        # 定义四次循环，因为需求是需要四位随机字母或数字
        for i in range(4):
            # 每循环一次，获取一个初始数据里的随机索引，random.randint(start,end)，获取区间内的随机整数
            initial_string_index = random.randint(0, len(initial_string) - 1)
            # 每循环一次，获取一个初始数据的下标
            initial_number_index = random.randint(0, len(initial_number) - 1)
            # 将获取到的随机下标对应的元素添加到空字符串，四次循环后，得到四位数字和字母的组合
            random_string += initial_string[initial_string_index]
            # 将获取到的随机下标对应的元素添加到空字符串，四次循环后得到四个数字
            random_number += initial_number[initial_number_index]
        # 将得到的四位字母和数字、四位随机数字返回，均为字符串格式，需要四位数字可使用int(string)进行转换
        return random_string, random_number
