from flask import Flask,render_template,url_for,request
app=Flask(__name__)
@app.route("/")
def index():
   return render_template('index.html')

@app.route("/result")
def ran():
   num1=request.args.get("num1")
   num2=request.args.get("num2")
   sum=int(num1)+int(num2)
   return render_template("ans.html",sum=sum)

if __name__=="__main__":
    app.run(debug=True)
