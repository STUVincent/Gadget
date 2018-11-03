# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
网页后台服务器

# 当前项目: HTML_Web
# 创建时间: 2018/11/3 17:45 
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
import json
import requests
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


# 参数传输测试
@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        print('GET----------------------------------------------')
        print('{:12s}: {}'.format('Method', request.method))
        print('{:12s}: {}'.format('URL', request.url))
        print('{:12s}: {}'.format('params', request.args))
        print('{:12s}: {}'.format('Header', request.headers))
        print('{:12s}: {}'.format('Form', request.form))
        print('{:12s}: {}'.format('Data', request.data))
        print('{:12s}: {}'.format('JSON', request.json))
        return render_template('home.html', requestInfo='', responseInfo='')

    elif request.method == 'POST':
        print('POST---------------------------------------------')
        # 表格返回数据
        request_form = request.form

        print('{:12s}: {}\n'.format('Form', request_form))

        # Method
        method = request_form['method']
        # 请求 URI
        uri = request_form['URI'].strip()

        # 请求参数  params
        params = dict()
        if len(request_form['Params']) > 0:
            try:
                for params_i in request_form['Params'].split('\r\n'):
                    params_i_value = params_i.split(':')
                    params[eval(params_i_value[0])] = eval(params_i_value[1])
                params_info = json.dumps(params, ensure_ascii=False, sort_keys=True, indent=4)
            except Exception as error:
                params_info = json.dumps({'Error:': repr(error)}, ensure_ascii=False, sort_keys=True, indent=4)
        else:
            params_info = ''

        # 请求头部  headers
        headers = dict()
        if len(request_form['Headers']) > 0:
            try:
                for header_i in request_form['Headers'].split('\r\n'):
                    header_i_value = header_i.split(':')
                    headers[eval(header_i_value[0])] = eval(header_i_value[1])
                headers_info = json.dumps(headers, ensure_ascii=False, sort_keys=True, indent=4)
            except Exception as error:
                headers_info = json.dumps({'Error:': repr(error)}, ensure_ascii=False, sort_keys=True, indent=4)
        else:
            headers_info = ''

        # 请求信息  body
        try:
            data = dict()
            for data_i in request_form['Data'].split('\r\n'):
                data_i_value = data_i.split(':')
                data[eval(data_i_value[0])] = eval(data_i_value[1])

            data_info = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
        except Exception as error:
            del error
            data_info = request_form['Data'].strip()

        # 所有请求相关信息
        request_info = '{} URI: {}\nParams:\n{}\nHeaders:\n{}\nData:\n{}\n'.format(
            method, uri, params_info, headers_info, data_info)

        # ##############################################################################
        # 调用接口
        if method == 'POST':
            api_response = requests.post(uri, params=params, headers=headers, data=data_info.encode('utf-8'))
        else:
            api_response = requests.get(uri, params=params, headers=headers, data=data_info.encode('utf-8'))

        print('{:12s}: {}'.format('URL', api_response.url))
        print('{:12s}: {}'.format('Path_URL', api_response.request.path_url))
        print('{:12s}: {}'.format('StatusCode', api_response.status_code))
        print('{:12s}: {}'.format('Method', api_response.request.method))
        print('{:12s}: {}'.format('Encoding', api_response.encoding))
        print('{:12s}: {}'.format('Headers', api_response.headers))
        print('{:12s}: {}'.format('Body', api_response.request.body))
        print('{:12s}: {}'.format('Cookies', api_response.cookies))
        print('{:12s}: {}'.format('Content', api_response.content))
        print('{:12s}: {}'.format('Text', api_response.text))

        # 响应信息  response_data
        try:
            response_data = json.loads(api_response.text)
            response_data = json.dumps(response_data, ensure_ascii=False, sort_keys=True, indent=4)
        except Exception as error:
            del error
            response_data = api_response.text.strip()

        response_info = '{} StatusCode:{} URI:{}  \nHeaders:\n{}\n\nResponseData:\n{}'.format(
            api_response.request.method, api_response.status_code, api_response.url, api_response.headers,
            response_data)
        return render_template('home.html', uri_d=request_form['URI'], headers_d=request_form['Headers'],
                               params_d=request_form['Params'], data_d=request_form['Data'],
                               requestInfo=request_info, responseInfo=response_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5599, debug=True)
