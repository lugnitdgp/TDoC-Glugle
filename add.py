from flask import Flask , render_template , request
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit',methods =['POST'])
def submit():
    if request.method == 'POST':
        ad= int(request.form['num_one'])+ int(request.form['num_two'])   
        return render_template('result.html',addition=ad)

if __name__ == '__main__':
    app.run()