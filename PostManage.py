# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/04/02
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask import request, current_app, jsonify
from utils.RestResUtil import RestResponse


def post_manage():
    if request.method == 'POST':
        # todo :auth

        request_data = request.get_json()

        method = request_data.get('method', '')
        md_name = request_data.get('md_name', '')
        dest_name = request_data.get('dest_name', '')

        if method == 'created':
            current_app.logger.info('created {}'.format(md_name))
            return jsonify(RestResponse.ok(msg='Success', code=200))
        elif method == 'deleted':
            current_app.logger.info('deleted {}'.format(md_name))
            return jsonify(RestResponse.ok(msg='Success', code=200))
        elif method == 'moved':
            current_app.logger.info('moved {} to {}'.format(md_name, dest_name))
            return jsonify(RestResponse.ok(msg='Success', code=200))
        elif method == 'modified':
            current_app.logger.info('modified {}'.format(md_name))
            return jsonify(RestResponse.ok(msg='Success', code=200))

        return jsonify(RestResponse.fail(msg='Invalid manage method!', code=400)), 400

    else:
        return jsonify(RestResponse.fail(msg='Invalid method!', code=400)), 400
