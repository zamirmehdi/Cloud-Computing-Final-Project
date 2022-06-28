from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/api1')
def api_one():  # put application's code here
    return 'This is first endpoint!'


@app.route('/<input>')
def api_two(input):  # put application's code here
    return 'This is second endpoint: ' + input


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
