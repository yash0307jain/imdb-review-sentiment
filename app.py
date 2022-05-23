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
        print(movie)
        status = ""
        try:
            status = scrapReviews(movie)
            return {'data': movie, 'status': status}
        except Exception as e:
            return {'error': str(e), "status": 404}

if __name__ == '__main__':
    app.run(debug=True)