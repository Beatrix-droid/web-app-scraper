from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

from urllib.parse import urljoin, urlparse


app = Flask(__name__)


@app.route("/")
def post_form():
	return render_template("index.html")

@app.route("/result", methods=["POST"])
def show_results():
	global link, tag, desired_element
	link = request.form.get("link")
	tag = request.form.get("tag")
	html_text = requests.get(link).text
	soup = BeautifulSoup(html_text, "html.parser")
	desired_element = soup.find_all(tag)
	counter = len(desired_element)
	return render_template("result.html", name="TIM", url=link, results=desired_element)

if __name__ == "__main_":
	app.run(debug=True, port=8000)
