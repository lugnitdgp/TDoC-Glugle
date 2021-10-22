from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST'])
def results():
    query = request.form['search_query']
    return render_template('results.html', query = query)

if __name__ == '__main__':
    app.run(debug = True)