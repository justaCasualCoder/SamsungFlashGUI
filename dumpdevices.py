import json
import requests
from bs4 import BeautifulSoup
devices = {}
request = requests.get("https://twrp.me/Devices/Samsung")
parsed_request = BeautifulSoup(request.content, "html.parser")
device_elements = parsed_request.select("ul#post-list > p > strong > a")
# Iterate through the 'a' tags and extract the device name and corresponding code
for element in device_elements:
    # Extract the device name (text within the 'a' tag)
    device_name = element.text.strip()

    # Split the href and get the last part, then remove the file extension
    code = element["href"].split("/")[-1].split(".")[0]

    # Extract all content within parentheses
    parentheses_content = [
        content.strip() for content in device_name.split("(")[1:]
    ]

    # Use the second set of parentheses if it exists; otherwise, use the first set of parentheses
    if len(parentheses_content) >= 2:
        code = parentheses_content[1].split(")")[0]
    else:
        code = parentheses_content[0].split(")")[0]

    # Remove spaces and convert to lowercase
    code = code.replace(" ", "").lower()

    # Add the device name and customized code to the dictionary
    devices[device_name] = code
with open('devices.json', 'w') as file:
    json.dump(devices, file)
