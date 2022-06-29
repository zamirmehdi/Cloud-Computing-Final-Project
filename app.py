from crypt import methods
from hashlib import sha256
from urllib.parse import urlparse

import requests as requests
from flask import Flask, request, redirect, url_for, render_template, request
import redis
import os
import json

app = Flask(__name__)

rdb = redis.Redis(host='127.0.0.1', port=6379, db=1,
                  password='', decode_responses=True)

@app.route('/', methods = ['POST', 'GET'])
def get_note():
    if request.method == 'POST':
      input_note = request.form['note']
      url = 60
      hashed = sha256(input_note.encode()).hexdigest()
      path = hashed[:5]
      rdb.set(path, input_note, ex=url)
      messages = json.dumps({"path":"http://localhost:5000/"+path})
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
    return render_template("confirm.html", id=input_path)


@app.route('/shownote', methods= ['POST', 'GET'])
def api_two():
    if request.method == 'POST':
        input = request.form['submit_button']
        print(input)
        input_path = input.split(':')[1]
        print(input.split(':'))
        note = str(rdb.get(input_path))
        print(note)
        return render_template("shownote.html", note=note)


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)
