from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  page_content="""
        <h1>Welcome! </h1>
        <h3>*** Your App is working ***</h3>
        """
  return page_content

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=80)
