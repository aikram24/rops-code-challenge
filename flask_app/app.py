from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  return '<h1>Hello, You have successful started an app. </h1>'

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=80)
