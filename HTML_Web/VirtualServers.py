# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
虚拟服务器，打印请求信息，并返回请求数据

# 当前项目: HTML_Web
# 创建时间: 2018/11/3 17:43 
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
from flask import Flask
from flask import request

app = Flask(__name__)


# 参数传输测试  UTF-8 编码格式
@app.route('/test', methods=['POST'])
def test():
    print('----------------------------------------------')
    print('{:12s}: {}'.format('Method', request.method))
    print('{:12s}: {}'.format('URL', request.url))
    print('{:12s}: {}'.format('params', request.args))
    print('{:12s}: {}'.format('Header', request.headers))
    print('{:12s}: {}'.format('Form', request.form))
    print('{:12s}: {}'.format('Data', request.data))
    print('{:12s}: {}'.format('JSON', request.json))

    # 返回请求数据
    return request.data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5588, debug=True)
