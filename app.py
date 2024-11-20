from flask import Flask, render_template, request
from review_scraper import Scraper

app = Flask(__name__)

scraper = Scraper()
reviews = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        reviews = scraper.get_reviews(url)
        return render_template("index.html", result=reviews)
    else:
        return render_template("index.html")

if  __name__ == "__main__":
    app.run(debug=True)