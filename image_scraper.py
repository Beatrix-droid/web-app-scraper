import validators
from urllib.parse import urljoin


def image_handler(tag, desired_element, link):
	""" Function check if the requeste tag is an image. If it is, it looks at
	its path (via 'src'). The validator checks if the image path is a URL.
	If it is the image path is appended to the image paths_list. If it is not
	the case, urljoin joins the images relative path to the base URL of the website"""

	image_paths = []
	if tag == "img":
		images = [img["src"] for img in desired_element]
		for i in desired_element:
			image_path = i.attrs["src"]
			validated_image_path = validators.url(image_path)
			if validated_image_path:
				full_path = image_path
			else:
				full_path = urljoin(link, image_path)
				image_paths.append(full_path)
	return image_paths
