from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbhomework


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/order', methods=['GET'])
def view_get():
    order = list(db.order.find({},{'_id': False}))
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!','order':order})


@app.route('/order', methods=['POST'])
def order_post():
    name = request.form['name']
    num = request.form['num']
    add = request.form['add']
    phone = request.form['phone']

    doc = {
        'name': name,
        'num': num,
        'add': add,
        'phone': phone
    }
    db.order.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=3500, debug=True)
