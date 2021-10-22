from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def entry_point():
    return render_template('home.html')


@app.route('/sum')
def sum():
    fnum = request.args.get('num1')
    snum = request.args.get('num2')
    sum = int(fnum) + int(snum)
    return render_template('result.html', sum=sum)


if __name__ == '__main__':
    app.run(debug=True)
