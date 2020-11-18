from flask import Flask,render_template,request

app = Flask(__name__)
ccc = []
@app.route('/aaa/')
def aaa():
    a = 0
    ccc.append(a)
    return a

def recode():
    ddd = []
    ddd = ccc
    print("ddd =====",ddd)
    return ddd

if __name__ == '__main__':
    b = aaa()
    eee = recode()
    print("eee ====",eee)
    print('b===',b)
    print(ccc)
    app.run()
