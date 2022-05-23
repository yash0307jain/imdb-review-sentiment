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
        resp = ""
        try:
            resp = scrapReviews(movie)
            time.sleep(5)
            return {'data': movie, 'status': resp}
        except Exception as e:
            return {'error': str(e), "status": 404}

if __name__ == '__main__':
    app.run(debug=True)