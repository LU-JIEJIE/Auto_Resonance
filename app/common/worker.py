"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-12 00:59:07
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QThread, pyqtSignal

from core.exceptions import StopExecution

from .config import cfg


class Worker(QThread):
    result = pyqtSignal(object)  # 使用 object 类型的信号，以便发送任何类型的数据

    def __init__(self, func, stop, **kargs):
        super(Worker, self).__init__()
        self.func = func
        self.stop_func = stop
        self.kargs = kargs

    def run(self):
        try:
            result = self.func(**self.kargs)
            self.result.emit(result)
        except StopExecution:
            pass

    def stop(self):
        self.stop_func()
