from hashlib import sha256
from urllib.parse import urlparse

import requests as requests
from flask import Flask, request, redirect, url_for, render_template
import redis
import os

app = Flask(__name__)
rdb = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'),
                  password=os.getenv('REDIS_SECRET'))
path_list = {}


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
    # return render_template("insex.html")


@app.route('/api1')
def api_one():  # put application's code here

    input_note = "Test note"  # For test
    hashed = sha256(input_note.encode()).hexdigest()
    path = hashed[:5]

    # For Kuber:
    # url = int(os.getenv('URL_EX'))
    # rdb.set(path, input_note, ex=url)

    # res = requests.post('http://localhost:5000/api2', path)

    # For Test:
    path_list[path] = input_note

    url = urlparse(request.host_url).geturl()
    print((url))

    return redirect(url_for('api_two', msg=url + path))


@app.route('/api2', methods=['POST', 'GET'])
def api_two():  # put application's code here

    if request.method == 'POST':
        path = request.form['msg']
        return path
    else:
        msg = request.args.get('msg')
        return msg


@app.route('/<input_path>')
def api_three(input_path):  # put application's code here
    return redirect(url_for('api_four', msg=input_path))


@app.route('/api4')
def api_four():  # put application's code here
    input_path = request.args.get('msg')

    if input_path in path_list.keys():
        return path_list[input_path]
    else:
        return 'Not a valid path. Try again!'


if __name__ == '__main__':
    # app.run()
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)
