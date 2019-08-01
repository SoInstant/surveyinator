from flask import Flask
app = Flask('app')

@app.route('/')
def main(): #Homepage
  return 'Hello, World!'

app.run()
