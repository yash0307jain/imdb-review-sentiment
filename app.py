from flask import Flask, render_template, request
from scraper import scrapReviews
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/scrap_review", methods=['POST'])
def getReviews():
    if request.method == "POST":
        movie = request.form['movie']
        try:
            status = scrapReviews(movie)
            return render_template('result.html', result=status)
        except Exception as e:
            return render_template('result.html', result=str(e))

if __name__ == '__main__':
    app.run(debug=True)