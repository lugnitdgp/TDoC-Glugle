from flask import Flask, render_template, request

app= Flask(__name__)
@app.route('/')
def entry_point():
    return render_template('homepage.html')
    
@app.route('/search_results')
def search_results():
    results=request.args.get('query')
    return render_template('results.html',results=results)


if __name__=='__main__':
    app.run(debug=True)
