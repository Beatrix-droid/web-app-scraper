from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from image_scraper import *



app = Flask(__name__)


@app.route("/")
def post_form():
	return render_template("index.html")

@app.route("/result", methods=["POST"])
def show_results():
	global link, tag, desired_element
	link = request.form.get("link")
	try:
		tag = request.form.get("tag")
		html_text = requests.get(link).text
		soup = BeautifulSoup(html_text, "html.parser")
		desired_element = soup.find_all(tag)
		counter = len(desired_element)
		image_paths = image_handler(tag, desired_element, link)
		return render_template("result.html", tag=tag, url=link, images=image_paths, count=counter, results=desired_element)
	except:
		return render_template("error.html")

if __name__ == "__main_":
	app.run(debug=True)






