from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests
import lxml

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def post_form():
	if request.method == "POST":
		link = request.form["link"]
		tag = request.form["tag"]
		return redirect("/result")
	return render_template("index.html")


@app.route("/result", methods=["POST"])
def show_results():
	return render_template("result.html")


if __name__ == "__main_":
	app.run(debug=True, port=8000)



	#html_text = requests.get("https://www.reed.co.uk/jobs/python-jobs").text
	#soup = BeautifulSoup(html_text, "lxml")
	#jobs = soup.find_all("article", class_="job-result")
