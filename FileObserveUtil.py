# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/31
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time

import requests
import threading

from queue import Queue

from pathlib import Path

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.MdFileUtil import MdFile


class MyHandler(FileSystemEventHandler):
    def __init__(self, pattern=None):
        self.pattern = pattern or ".md"
        self.event_q = Queue()
        self.dummyThread = None

    def on_any_event(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            self.event_q.put((event, time.time()))

    def start(self):
        self.dummyThread = threading.Thread(target=self._process)
        self.dummyThread.daemon = True
        self.dummyThread.start()

    @staticmethod
    def _process():
        while True:
            time.sleep(1)


class Watcher(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path, url=''):
        self.path = path
        self.handler = MyHandler()
        self.handler.start()
        self.last_event = None

        self.pdata = {}
        self.url = url

        self.logger = Log()

    def handle_event(self, event, ts):
        self.pdata["method"] = event.event_type
        self.pdata["time"] = ts
        self.pdata["src_name"] = Path(event.src_path).stem

        if event.event_type == 'deleted':
            self.pdata["payload"] = ''
        elif event.event_type == 'moved':
            self.pdata["dest_name"] = Path(event.dest_path).stem
            self.pdata["payload"] = ''
        else:
            md_file = event.src_path
            md = MdFile(md_file)
            self.pdata["payload"] = md.get_start()

        if self.url:
            self.post_request()
        self.pdata.pop("payload")
        self.logger.info(self.pdata)

    def post_request(self):
        r = requests.post(url=self.url, data=self.pdata)

    def run_watcher(self):
        observer = Observer()
        observer.schedule(self.handler, self.path)
        observer.start()
        try:
            while True:
                while not self.handler.event_q.empty():
                    event, ts = self.handler.event_q.get()
                    if not (self.last_event and event == self.last_event):
                        self.handle_event(event, ts)
                    self.last_event = event
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def run_with_thread(self):
        watcher_thread = threading.Thread(target=self.run_watcher, name="watcher_1")
        watcher_thread.start()


class Log(object):

    def __init__(self):

        # 文件的命名
        self.log_file = Path(__file__).parent.absolute() / 'filemonitor.log'
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.log_file, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == '__main__':
    watcher = Watcher('D:\\Test')
    watcher.run_with_thread()
