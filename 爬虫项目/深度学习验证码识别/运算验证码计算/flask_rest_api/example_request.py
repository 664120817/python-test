"""Perform test request"""
import pprint

import requests

DETECTION_URL = " http://127.0.0.1:88/img"
TEST_IMAGE = "1.png"

image_data = open(TEST_IMAGE, "rb").read()

response = requests.post(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)
