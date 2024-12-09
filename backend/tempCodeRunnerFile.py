from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def hello_word():
    return ("Hello")

if __name__ == '__main__':
    app.run(port=3000, debug=True)