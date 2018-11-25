#!/usr/bin/env python 
# coding:utf-8
# @Time :11/24/18 16:21

import re
from www_douban_com.resources.douban_rent import DoubanRent
from pyhanlp import *
from www_douban_com.resources.douban_rent_enum import (RentStatus, HostNeedRentStatus, HostIsPersonal, AttrExistStatus)



class InfoHandlerBase(object):

    def __init__(self):
        pass

    def clean_data(self, sentence):
        pass

    def _extract_value(self, text, check_from_list, amount=None):
        """
        从 text 中提取 存在于 check_from_list 中的值
        :param text:
        :param check_from_list:
        :param amount:  提取的数量（默认提取所有值）
        :return:
        """
        if not amount:
            amount = len(check_from_list)
        extract_info = []
        count = 0
        for per_char in check_from_list:
            if per_char in text and count < amount:
                count += 1
                extract_info.append(per_char)
        return extract_info

    def _is_value_exist(self, text, check_from_list, all_match=False):
        """
        判断 check_from_list 中的值，是否存在于text中
        :param text:
        :param check_from_list:
        :param all_match: 是否需要全部校验（默认False）
        :return:
        """
        if not all_match:
            for per_char in check_from_list:
                if per_char in text:
                    return True
            return False
        return all([self._is_value_exist(text, [char]) for char in from_list])


class DouBanInfoHandler(InfoHandlerBase):

    """

    帖子base：
        状态： 已下架、正常（默认）

    租主base：
        求租：是、否
        性别： 男女，限男，限女
        个人转租：是、否
        [*del]联系方式：[]

    房子base：
        户型：两室一厅，...
        家私：齐全
        价格：
        单间：是、否
        待租房型：主卧、次卧、...
        独卫：是、否
        电梯房：是、否

    位置base：
        邻近地铁：[]

    使用base：
        拎包入住：是，否
        租金支付方式：押一付一、押二付一、...
        合租：是、否
        租住时长：长租、短租


    租户意向 | 租住类型 | 性别 | 地理位置 | 价格 | 户型 | 电梯房 | 联系方式 | 帖子地址 | 发帖人类型 | 租用方式 |
    """

    def clean_data(self, sentence):
        rent_status = RentStatus.DOWNLINE.value if self._is_value_exist(sentence, DoubanRent.rent_status) else RentStatus.ONLINE.value

        host_need_rent = HostNeedRentStatus.YES.value if "求租" in sentence else HostNeedRentStatus.UNKNOW.value
        host_claim_sex_raw = self._extract_value(sentence, DoubanRent.sex, amount=1)
        host_claim_sex = host_claim_sex_raw[0] if host_claim_sex_raw else None
        host_is_personal = HostIsPersonal.YES.value if "个人" in sentence else HostIsPersonal.UNKNOW.value

        house_type_room_count, house_type_hall_count = self.__extract_house_type(sentence)
        house_furniture = AttrExistStatus.YES.value if any(i in sentence for i in ["家私", "家具", "家电"]) else AttrExistStatus.UNKNOW.value
        house_price_raw = self.__extract_price(sentence)
        house_price = house_price_raw[0] if house_price_raw else None
        house_single_room = AttrExistStatus.YES.value if "单间" in sentence else AttrExistStatus.UNKNOW.value
        house_bedroom_raw = self._extract_value(sentence, DoubanRent.bedroom, amount=1)
        house_bedroom = house_bedroom_raw[0] if house_bedroom_raw else None
        house_private_toilet = AttrExistStatus.YES.value if "独卫" in sentence else AttrExistStatus.UNKNOW.value
        house_elevator = self.__extract_elevator(sentence)

        location_nearby = self.__extract_nearby(sentence)
        location_subway = self._extract_value(sentence, DoubanRent.subway)

        use_everytime_available = AttrExistStatus.YES.value if ("拎包" or "随时") in sentence else AttrExistStatus.UNKNOW.value
        use_pay_deposit, use_pay_payment = self.__extract_payment(sentence)
        use_roommate = self.__extract_rent_way(sentence)
        use_long = self._extract_value(sentence, DoubanRent.duration)

        item = {
            "rent_status": rent_status,
            "host_need_rent": host_need_rent,
            "host_claim_sex": host_claim_sex,
            "host_is_personal": host_is_personal,
            "house_type_room_count": house_type_room_count,
            "house_type_hall_count": house_type_hall_count,
            "house_furniture": house_furniture,
            "house_price": house_price,
            "house_single_room": house_single_room,
            "house_bedroom": house_bedroom,
            "house_private_toilet": house_private_toilet,
            "house_elevator": house_elevator,
            "location_subway": location_subway,
            "location_nearby": location_nearby,
            "use_everytime_available": use_everytime_available,
            "use_pay_deposit": use_pay_deposit,
            "use_pay_payment": use_pay_payment,
            "use_roommate": use_roommate,
            "use_long": use_long,
        }

        return item

    def __extract_price(self, sentence):
        numbers = re.compile('\d+').findall(sentence)
        price = list(map(lambda x: int(x), filter(lambda x: len(x) == 4, numbers))) if numbers else None
        return price

    def __extract_house_type(self, sentence):

        __CHINESE_NUM_MAP = {
            "一": 1,
            "二": 2,
            "两": 2,
            "三": 3,
            "四": 4,
            "未知": -1,
        }

        room_count_raw = re.compile(".*(.)[室|房]").findall(sentence)
        room_count = -1
        if room_count_raw:
            room_count = __CHINESE_NUM_MAP.get(room_count_raw[0], -1)

        hall_count_raw = re.compile(".*(.)[厅]").findall(sentence)
        hall_count = -1
        if hall_count_raw:
            hall_count = __CHINESE_NUM_MAP.get(hall_count_raw[0], -1)

        return room_count, hall_count

    def __extract_payment(self, sentence):

        __CHINESE_NUM_MAP = {
            "一": 1,
            "二": 2,
            "两": 2,
            "三": 3,
        }

        pay_raw = re.compile(".*押(.)付(.)").findall(sentence)
        pay_deposit = -1
        pay_payment = -1
        if pay_raw:
            pay_deposit = __CHINESE_NUM_MAP.get(pay_raw[0][0], -1)
            pay_payment = __CHINESE_NUM_MAP.get(pay_raw[0][1], -1)
        return pay_deposit, pay_payment

    def __extract_elevator(self, sentence):
        if "电梯" in sentence:
            return AttrExistStatus.YES.value
        elif "楼梯" in sentence:
            return AttrExistStatus.NO.value
        else:
            return AttrExistStatus.UNKNOW.value

    def __extract_rent_way(self, sentence):
        if "合租" in sentence:
            return AttrExistStatus.YES.value
        elif "整租" in sentence:
            return AttrExistStatus.NO.value
        else:
            return AttrExistStatus.UNKNOW.value

    def __extract_nearby(self, sentence):
        CRFLexicalAnalyzer = JClass("com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer")
        analyzer = CRFLexicalAnalyzer()
        loc = []
        words = analyzer.analyze(sentence).findWordsByLabel("ns").toArray()
        if words:
            loc = [i.value for i in words]
        return loc



if __name__ == '__main__':
    base = DouBanInfoHandler()
    print(base.clean_data("【罗湖】太安站 两室一厅一厨一卫 主卧出租 1000元／月 限女"))
    # print(d.clean_data('nifrfrfrjiji 反日法人 2299'))

    # info_handler = InfoHandlerBase()
    # print(info_handler._is_value_exist("【罗湖】太安站 两室一厅一厨一卫 主卧出租 1000元／月 限女", ["罗湖", "10001元"], all_match=True))

