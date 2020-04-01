# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os

import logging

from flask import Flask

from FileObserveUtil import Watcher
from WebHook import github_moniter

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask('filemoniter')
app.config["DEBUG"] = False
app.config["NOTE_ABS_PATH"] = os.environ.get('PRD_NOTE_PATH', 'D:\\Project\\Notable\\notes')
app.config["FLASK_RUN_PORT"] = 8071

# log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(os.path.join(basedir, 'logs/app.log'), encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# route
app.add_url_rule('/githubwebhook', view_func=github_moniter)

# Watcher

watcher = Watcher(app.config["NOTE_ABS_PATH"])
watcher.run_with_thread()

if __name__ == '__main__':
    app.run(port=8072)
