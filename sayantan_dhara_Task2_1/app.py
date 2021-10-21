from flask import Flask,render_template,request,redirect

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def result():
    num1=request.args['num1'].strip()
    num2=request.args['num2'].strip()
    if num1.isnumeric() and num2.isnumeric():
        addition=0
        try:
            addition=int(num1)+int(num2)
        except ValueError:
            addition=float(num1)+float(num2)
        return render_template('result.html',addition=addition)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)