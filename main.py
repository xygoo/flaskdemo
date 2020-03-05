from flask import Flask,request,render_template
from gevent.pywsgi import WSGIServer
app = Flask(__name__)

@app.route("/")
def hello():
    user_agent=request.headers.get('User-Agent')
    return render_template('hello.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)

