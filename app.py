from flask import Flask, render_template, request
from scraper import scrapReviews
import tensorflow as tf
import pandas as pd
import pickle
import json

app = Flask(__name__)
tokenizer = pickle.load(open('model_data/tokenizer.pkl', 'rb'))
model = tf.keras.models.load_model('model_data/sentiment_analysis_model')

def reviewSentiment(reviews: list[str]):
    df_pipe = pd.DataFrame({'tweet': reviews})
    
    X = tokenizer.texts_to_sequences(df_pipe['tweet'].values)
    X = tf.keras.preprocessing.sequence.pad_sequences(X, padding='pre', maxlen=18)

    sentiment_pred = model.predict(X)

    review_sentiment = []
    for i in range(len(reviews)):
        [negative, positive] = sentiment_pred[i]
        sentiment = "positive" if positive > negative else "negative"
        review_sentiment.append((reviews[i], sentiment))

    return review_sentiment
    

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/scrap_review", methods=['POST'])
def getReviews():
    if request.method == "POST":
        movie = request.form['movie']
        try:
            movie_name = scrapReviews(movie)
            reviews = []
            with open(f'data/{movie_name}.json', 'r') as f:
                reviews = json.load(f)['reviews']
            sentiment = reviewSentiment(reviews)
            return render_template('result.html', result={ "sentiment": sentiment, "movie_name": movie_name } )
        except Exception as e:
            return render_template('result.html', result=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=8000)