from flask import Flask , render_template , request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sum',methods =['POST'])
def sum():
    if request.method == 'POST':
        add= int(request.form['n1'])+ int(request.form['n2'])   
        return render_template('sum.html',addition=add)

if __name__ == '__main__':
    app.run()