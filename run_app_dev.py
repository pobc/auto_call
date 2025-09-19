#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import create_app
import socket
from waitress import serve
from flask_cors import CORS

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

CORS(app)  # 启用 CORS 跨域支持
# 获取主机名
hostname = socket.gethostname()
# 获取本机 IP
local_ip = socket.gethostbyname(hostname)

if __name__ == '__main__':
    """
    """
    print(f"http://{local_ip}:5000/phone_num_list")
    # app.run(host='0.0.0.0', port=5000, debug=False)
    serve(app, host='0.0.0.0', port=5000)


