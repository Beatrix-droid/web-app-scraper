import pathlib

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, uuid
from image_scraper import *

app = Flask(__name__)
app.static_folder = "static"


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

@app.route("/download", methods=["GET", "POST"])
def image_downloader():
	""""A function that downloads the scraped images. The uuid library is used to produce
	unique IDs for the downloaded files."""

	try:
		for img in image_handler(tag, desired_element,link):
			image_link = img
			file_name =  str(uuid.uuid4())
			file_extension = pathlib.Path(image_link).suffix
			picture_name = file_name + file_extension
			download_path = str(pathlib.Path.home()/"Downloads")
			
	except:
		pass

if __name__ == "__main_":
	app.run(debug=True)

