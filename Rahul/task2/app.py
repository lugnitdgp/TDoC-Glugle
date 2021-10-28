from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def entry_point():
    return render_template('home.html')


@app.route('/sum')
def sum():
    first_num = request.args.get('num1')
    second_num = request.args.get('num2')
    sum = int(first_num) + int(second_num)
    return render_template('search_result.html', sum=sum)


if __name__ == '__main__':
    app.run(debug=True)