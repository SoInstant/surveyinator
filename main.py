from flask import Flask, render_template
app = Flask('app')

@app.route('/')
def main(): #Homepage
  return render_template("index.html")

app.run()
