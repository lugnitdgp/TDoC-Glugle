from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')
@app.route('/cal', methods=['POST'])
def cal(sum=sum):
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']

        if operation == 'add':
            sum = float(num1) + float(num2)
            return render_template('result.html', sum=sum)

        elif operation == 'subtract':
            sum = float(num1) - float(num2)
            return render_template('result.html', sum=sum)
        
        elif operation == 'multiply':
            sum = float(num1) * float(num2)
            return render_template('result.html', sum=sum)

        elif operation == 'divide':
            sum = float(num1) / float(num2)
            return render_template('result.html', sum=sum)
        else:
            return render_template('result.html')

if __name__ == ' __main__':
    app.run(debug=True)