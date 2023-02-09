import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options = webdriver.FirefoxOptions()
options.binary = binary

url = "https://fapello.com/ain-nguyen/"

driver = webdriver.Firefox(options=options)
driver.get(url)

# A list to store all image URLs
image_urls = []

# Scroll to the bottom of the page multiple times
# until all images have been loaded
previous_height = 0
while True:
    # Get the source code of the page
    html = driver.page_source

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find all image tags
    images = soup.find_all("img")

    # Loop through the images and add their URLs to the list
    for image in images:
        image_url = image["src"]
        if image_url not in image_urls:
            image_urls.append(image_url)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Check if the page height has changed
    current_height = driver.execute_script("return document.body.scrollHeight;")
    if current_height == previous_height:
        break
    previous_height = current_height

# Close the browser
driver.quit()

# Set the directory to save the images
directory = "scraped_images"
if not os.path.exists(directory):
    os.makedirs(directory)

# Loop through the image URLs and download each image
for i, image_url in enumerate(image_urls):
    response = requests.get(image_url)
    with open(os.path.join(directory, f"image_{i}.jpg"), "wb") as f:
        f.write(response.content)

