from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/about')

def clusters():
    return render_template('clusters.html')


if __name__ == '__main__':
    app.run(debug = True)


