import validators
from urllib.parse import urljoin

def image_handler(tag, desired_element, link):
		""" Function check if the requeste tag is an image. If it is, it looks at
		its path (via 'src'). The validator checks if the image path is a URL.
		If it is the image path is appended to the image paths_list. If it is not
		the case, urljoin joins the iamge relative path to the base URL of the website"""

		image_paths = []
		if tag =="img":
			images = [img["src"] for img in desired_element]
			for i in desired_element:
				image_path = i.attrs["src"]
				validated_image_path = validators.url(image_path)
				if validated_image_path == True:
					full_path = image_path
				else:
					full_path = urljoin(link, image_path)
					image_path.append(full_path)
		return image_paths


#print(image_handler("https://www.airbnb.co.uk/s/Kharkiv-River/homes?adults=1&place_id=ChIJm9FBL8tSJkER2hNUX0tUmAk&refinement_paths%5B%5D=%2Fhomes&checkin=2021-11-20&checkout=2021-11-21"))
#image_handler("https://dev.to/dev_elie/building-a-python-web-scraper-in-flask-b87")

