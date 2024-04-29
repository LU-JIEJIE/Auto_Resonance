"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:27:03
LastEditTime: 2024-04-29 22:46:46
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import asyncio
import subprocess
from typing import Union

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import DotInfoBadge
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    InfoBadgePosition,
    InfoBar,
    InfoBarPosition,
    MSFluentWindow,
    NavigationBarPushButton,
    NavigationItemPosition,
    SplashScreen,
)

from app.view.daily_task_interface import DailyTaskInterface
from app.view.running_business_interface import RunningBusinessInterface
from updater import Updater

from ..common import resource  # 图标数据
from ..common.config import VERSION, cfg
from ..common.icon import FluentIconBase
from ..common.signal_bus import signalBus
from .home_interface import HomeInterface
from .logger_interface import LoggerInterface
from .setting_interface import SettingInterface
from .taj_interface import TajInterface
from .this_road_that_interface import ThisRoadThatInterface


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.wights = {}

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.tajInterface = TajInterface(self)
        self.loggerInterface = LoggerInterface(self)
        self.settingInterface = SettingInterface(self)
        self.daily_task_interface = DailyTaskInterface(self)
        self.running_business_interface = RunningBusinessInterface(self)
        self.this_road_that_interface = ThisRoadThatInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()
        # 检查更新
        self.is_updae = False
        asyncio.run(self.checkUpdate())

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToCard.connect(self.switchToCard)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.tajInterface, FIF.AIRPLANE, "铁安局")
        self.addSubInterface(self.daily_task_interface, FIF.CALENDAR, "每日任务")
        self.addSubInterface(self.running_business_interface, FIF.TRAIN, "跑商配置")
        self.addSubInterface(self.this_road_that_interface, FIF.TRAIN, "我建我路")

        # add custom widget to bottom
        self.addSubInterface(
            self.loggerInterface,
            FIF.ALIGNMENT,
            "日志",
            position=NavigationItemPosition.BOTTOM,
        )
        self.updateButton = self.navigationInterface.addItem(
            routeKey="Update",
            icon=FIF.UPDATE,
            text="更新",
            onClick=self.Update,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM,
        )

    def addSubInterface(
        self,
        interface: QWidget,
        icon: Union[FluentIconBase, QIcon, str],
        text: str,
        selectedIcon=None,
        position=NavigationItemPosition.TOP,
        isTransparent=False,
    ) -> NavigationBarPushButton:
        super().addSubInterface(
            interface, icon, text, selectedIcon, position, isTransparent
        )
        self.wights[interface.objectName()] = interface

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon("./app/resource/images/logo.ico"))
        self.setWindowTitle(f"黑月无人驾驶 - {VERSION}")

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        self.setResizeEnabled(False)
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())

    def switchToCard(self, routeKey):
        """switch to card"""
        self.switchTo(self.wights[routeKey])

    def Update(self):
        """
        说明:
            检查更新
        """
        if not self.is_updae:
            subprocess.Popen(
                ["HeiYue Updater.exe"], creationflags=subprocess.DETACHED_PROCESS
            )
            exit()
        else:
            InfoBar.success(
                title="当前已是最新版本",
                content="",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )

    async def checkUpdate(self):
        updater = Updater()
        is_last, _ = await updater.is_last()
        if is_last:
            self.updateBadge = DotInfoBadge.error(
                parent=self.navigationInterface,
                target=self.updateButton,
                position=InfoBadgePosition.NAVIGATION_ITEM,
            )
            self.updateBadge.setFixedSize(10, 10)
            self.is_updae = True
