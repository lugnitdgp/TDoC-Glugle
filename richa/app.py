from flask import Flask, render_template, request
import pymongo


app = Flask(__name__)


@app.route('/')
def search_entry():
    return render_template('home.html')


@app.route('/results')
def searching():
  return "Under Process!"


if __name__ == '__main__':
    app.run(debug=True)