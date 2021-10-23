from flask import Flask, render_template, request
import jinja2

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sum')

def sum():
    fnum=request.args.get('Num1')
    snum=request.args.get('Num2')
    sum=int(fnum)+int(snum)
    return render_template('sum.html', sum = sum)

if __name__=='__main__':
    app.run(debug=True)
