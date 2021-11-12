from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import lxml

app = Flask(__name__)


@app.route("/")
def get_dev_jobs():
	html_text = requests.get("https://www.reed.co.uk/jobs/python-jobs").text
	soup = BeautifulSoup(html_text, "lxml")
	jobs = soup.find_all("article", class_="job-result")

	for index, job in enumerate(jobs):
			title = job.find("h3", class_="title").text.replace("\n", "")
			company_name = job.find(class_="posted-by").a.text
			company = job.find("div", class_="posted-by").text
			company = company.strip()
			company = company.split("by")
			company[0] = company[0][7:]

			metadata = job.find("div", class_="metadata")
			salary = metadata.find("li", class_="salary").text
			location = metadata.find("span").text
			time = metadata.find("li", class_="time").text
			description = job.find(class_="description").p.text

			remote = metadata.text
			if "Work from home" in remote:
				work_remotely = "Yes"
			else:
				work_remotely = "No"

			more_info = job.header.h3.a["href"]

			result = {
					"Date Posted:": company[0],
					"Company:": company_name,
					"Job Title:": title,
					"Salary:": salary,
					"Location:": location,
					"Time:": time,
					"Work from home:": work_remotely,
					"Description:": description,
					"More info:": more_info}

			return render_template("index.html", result=result)



if __name__ == "__main_":
	app.run(debug=True, port=8000)