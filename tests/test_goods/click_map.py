# 澄明数据中心 (1049, 345) 7号自由港 (665, 577) 阿妮塔战备工厂 (832, 664) 阿妮塔发射中心 (164, 420+577) 阿妮塔能源研究所 (614, 454+577)
# 修格里城 (285+1049, 121+345) 铁盟哨站 (501+1049, 122+345) 荒原站 (753+1049, 121+345)
# 曼德矿场 (602+1049, 322+345) 淘金乐园 (701+1049, 604+345)

from core.adb import connect
from core.presets import click_station
MAP_DATA = {
    "澄明数据中心": (1049, 345),
    "7号自由港": (665, 577),
    "阿妮塔战备工厂": (832, 664),
    "阿妮塔发射中心": (164, 420 + 577),
    "阿妮塔能源研究所": (614, 454 + 577),
    "修格里城": (285 + 1049, 121 + 345),
    "铁盟哨站": (501 + 1049, 122 + 345),
    "荒原站": (753 + 1049, 121 + 345),
    "曼德矿场": (602 + 1049, 322 + 345),
    "淘金乐园": (701 + 1049, 604 + 345),
}


connect("127.0.0.1:21523")
click_station("7号自由港")
