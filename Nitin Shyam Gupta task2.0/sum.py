from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sum')
def sum():
    num1 = request.args.get('fnum')
    num2 = request.args.get('snum')
    sum = int(num1) + int(num2)
    return render_template('result.html', sum = sum)
if __name__== '__main__':
    app.run()
