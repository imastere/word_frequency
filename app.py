from word_frequency.manage import app
from flask import render_template
# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/login')
def user_login():
    return render_template('user/login.html')

@app.route('/register')
def user_register():
    return render_template('user/register.html')

@app.route('/audio')
def audio():
    return render_template('audio/index.html')

@app.route('/player')
def player():
    return render_template('audio/player.html')

@app.route('/word')
def word():
    return render_template('word/index.html')

@app.route('/spelling')
def spelling():
    return render_template('word/spelling.html')


@app.route('/search')
def search():
    return render_template('search/index.html')




if __name__ == '__main__':
    app.run()
