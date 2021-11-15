from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests
#import lxml

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def post_form():
	if request.method == "POST":
		global link, tag, desired_element
		link = request.form["link"]
		tag = request.form["tag"]
		html_text = requests.get(f"{link}").text
		soup = BeautifulSoup(html_text, "lxml")
		desired_element = soup.find_all(f"{tag}")
		counter = len(desired_element)
		return redirect("/result", url=link, results=desired_element, counter=counter)
	return render_template("index.html")

@app.route("/result", methods=["POST"])
def show_results():
	return render_template("result.html")


if __name__ == "__main_":
	app.run(debug=True, port=8000)
