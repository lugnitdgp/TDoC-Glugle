from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def calculate():
    sum=''
    if request.method=="POST" and 'number1' in request.form and 'number2' in request.form:
        First=float(request.form.get('number1'))
        Second=float(request.form.get('number2'))
        sum=First+Second
    return render_template("index.html", sum=sum)




