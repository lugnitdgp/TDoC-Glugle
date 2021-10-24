from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def getsum():
    return render_template('base.html')


@app.route('/sum')
def putsum():
    snum_1 = request.args.get('num_1')
    snum_2 = request.args.get('num_2')
    sum = int(snum_1) + int(snum_2)
    return render_template('answer.html', sum=sum)


if __name__ == '__main__':
    app.run(debug=True)
