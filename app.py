
# ! First Run

# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# msg = "Welcome to this channel"
# print(msg)

# ! Second Run

from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome to my channel"


@app.route('/success/<int:score>')
def success(score):
    return "<html><body><h1>The Result is passed</h1></body></html>"


@app.route('/fail/<int:score>')
def fail(score):
    return "The person has failed and the marks is " + str(score)

# * Result Checker


@app.route('/results/<int:marks>')
def results(marks):
    result = ""
    if marks < 50:
        result = 'fail'
    else:
        result = 'success'
    return redirect(url_for(result, score=marks))
    # return result


if __name__ == '__main__':
    app.run(debug=True)
