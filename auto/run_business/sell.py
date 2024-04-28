"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 15:17:19
LastEditTime: 2024-04-22 23:27:51
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.adb import input_tap, screenshot
from core.exception_handling import get_excption
from core.image import get_bgr, get_hsv
from core.ocr import number_predict, predict
from core.utils import compare_ranges


def sell_business(num=0):
    """
    说明:
        出售所有商品
    参数:
        :param num: 期望议价的价格
    """
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < 15:
        bgr = get_bgr(screenshot(), (1156, 100))
        logger.debug(f"是否出售货物颜色检查 {bgr}")
        if not compare_ranges([0, 0, 90], bgr, [0, 0, 110]):
            logger.info(f"出售全部货物 {bgr}")
            input_tap((1187, 103))
            time.sleep(0.5)
            break
    if is_empty_goods():
        logger.error("检测到未成功出售物品")
        return False
    else:
        click_bargain_button(num)
        click_sell_button()
        time.sleep(0.5)
        return input_tap((896, 676))


def is_empty_goods():
    bgr = get_bgr(
        screenshot(), (898, 169), cropped_pos1=(870, 132), cropped_pos2=(994, 205)
    )
    return compare_ranges([22, 27, 27], bgr, [22, 27, 27])


def click_bargain_button(num=0):
    """
    说明:
        点击议价按钮
    参数:
        :param num: 议价次数
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 15:
        if num <= 0:
            return True
        bgr = get_bgr(screenshot(), (1176, 461))
        logger.debug(f"抬价界面颜色检查: {bgr}")
        if compare_ranges([0, 170, 240], bgr, [0, 183, 253]):
            input_tap((1177, 461))
            time.sleep(1.0)
        elif bgr == [251, 253, 253]:
            logger.info("议价次数不足")
            return True
        elif bgr == [62, 63, 63]:
            logger.info("疲劳不足")
            input_tap((83, 36))
            return True
        hsv = get_hsv(screenshot(), (626, 273), (516, 224), (787, 439))
        logger.debug(f"抬价是否成功颜色检查(HSV): {hsv}")
        if 30 <= hsv[0] <= 40:
            logger.info("抬价成功")
            num -= 1
        else:
            logger.info("抬价失败")
        if get_excption() == "议价次数不足":
            return False

    return False


def click_sell_button():
    start = time.time()
    while time.time() - start < 10:
        input_tap((1056, 647))
        time.sleep(1)
        image = screenshot()
        bgr = get_bgr(image, (1175, 470))
        logger.debug(f"出售物品界面颜色检查: {bgr}")
        if bgr == [227, 131, 82]:
            logger.info("检测到包含本地商品")
            input_tap((975, 498))
        if bgr != [0, 183, 253] and bgr != [227, 131, 82] and bgr != [251, 253, 253]:
            return True
    return False
