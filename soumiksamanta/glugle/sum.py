from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def addNumbers():
    if request.method == 'POST':
        a = request.form["a"]
        b = request.form["b"]
        return redirect(url_for("sum", a=a, b=b))

    return render_template("sum_in.html")


@app.route("/sum")
def sum():
    a  = int(request.args.get('a', None))
    b  = int(request.args.get('b', None))
    return render_template("sum_out.html", a=a, b=b, sum=(a+b))