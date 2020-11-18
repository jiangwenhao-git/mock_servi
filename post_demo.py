#encoding:utf-8

from flask import Flask,render_template,request
import subprocess

#本py文件主要是测试mock返回链接

app = Flask(__name__)
url_base = []   #考虑着要不要把mock地址传递出去，如何传递

@app.route('/')
def index(): #一访问127.0.0.1:5000就会返回index模板中的链接”跳转到搜索页面”
    url_base.append(request.base_url)
    print("mock地址为: ",request.base_url)
    return render_template('index.html')
@app.route('/default/')
def default(): #一访问127.0.0.1:5000就会返回index模板中的链接”跳转到搜索页面”
    url_base.append(request.base_url)
    print("mock地址为: ",request.base_url)
    return render_template('mockdefault.html')
@app.route('/search/')
def search():
    #arguments
    print(request.args) #获取所有参数
    # url_base.append(request.base_url)
    print("mock地址为: ",request.base_url)
    print(request.args.get('q')) #或者参数为q的值
    return 'search'

@app.route('/login/',methods=['GET','POST'])  #指定访问页面的方法
def login():
    print("mock地址为: ", request.base_url)
    if request.method == 'GET': #如果请求方法时GET,返回login.html模板页面
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        return 'post request'
@app.route('/aaa/')
def aaa():
    print("mock地址为: ",request.base_url)
    return request.path

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9002, threaded=True, debug=False)
