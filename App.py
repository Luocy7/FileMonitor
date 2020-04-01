# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os

import logging
from logging import FileHandler

from flask import Flask

from FileObserveUtil import Watcher
from WebHook import github_moniter

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask('filemoniter')
app.config["DEBUG"] = True
app.config["NOTE_ABS_PATH"] = os.environ.get('PRD_NOTE_PATH', 'D:\\Project\\Notable\\notes')
app.config["FLASK_RUN_PORT"] = 5002

# route
app.add_url_rule('/githubwebhook', view_func=github_moniter)

# Watcher

watcher = Watcher(app.config["NOTE_ABS_PATH"])
watcher.run_with_thread()

print('done')
if __name__ == '__main__':
    app.run(port=5001)
