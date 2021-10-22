from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sum', methods = ['POST'])
def sum():
    num1 = (int)(request.form['num1'])
    num2 = (int)(request.form['num2'])
    sum = num1 + num2
    return render_template('sum.html', sum = sum)

if __name__ == '__main__':
    app.run(debug=True)