from flask import Flask,render_template,request,redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def Home():
    sum=0
    if request.method == 'POST':
        num1=int(request.form['num1'])
        num2=int(request.form['num2'])
        sum=num1+num2
        return render_template('result.html',sum=sum,num1=num1,num2=num2)
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)