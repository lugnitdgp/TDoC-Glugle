from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)
app.debug = True

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        num1 = request.form["number1"]
        num2 = request.form["number2"]
        result = int(num1)+int(num2)
        print(result)
        return redirect(url_for("result",res=result))
    else:
        return render_template("index.html")

@app.route("/result/<res>")
def result(res):
    return render_template("result.html",res=res)

if __name__ == "__main__":
    app.run()