from hashlib import sha256
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request
import redis
import os
import json

load_dotenv(os.getenv('ENV_FILE', '.env'))

app = Flask(__name__)

rdb = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'),
                  password=os.getenv('REDIS_SECRET'), decode_responses=True)


# rdb = redis.Redis(host='127.0.0.1', port=6379, db=1, password='', decode_responses=True)


@app.route('/', methods=['POST', 'GET'])
def get_note():
    if request.method == 'POST':
        input_note = request.form['note']
        hashed = sha256(input_note.encode()).hexdigest()
        path = hashed[:5]
        url_ex = int(os.getenv('URL_EX'))
        rdb.set(path, input_note, ex=url_ex)
        url = urlparse(request.host_url).geturl()
        messages = json.dumps({"path": url + path})
        return redirect(url_for('.send_note', messages=messages))
    else:
        return render_template("homepage.html")


@app.route('/sendNote')
def send_note():
    messages = json.loads(request.args['messages'])
    path = messages['path']
    return render_template("showlink.html", url=path)


@app.route('/<input_path>')
def search_note(input_path):
    if rdb.get(input_path) is None:
        return redirect(url_for('.get_note'))
    return render_template("confirm.html", id=input_path)


@app.route('/shownote', methods=['POST', 'GET'])
def api_two():
    if request.method == 'POST':
        input = request.form['submit_button']
        input_path = input.split(':')[1]
        note = str(rdb.get(input_path))
        rdb.delete(input_path)
        return render_template("shownote.html", note=note)


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)
