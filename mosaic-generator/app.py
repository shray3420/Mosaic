
from flask import Flask, jsonify, render_template, request
import base64
import time
import requests
import string
from sklearn.neighbors import KDTree
import numpy as np
from PIL import Image
import signal
import sys
import subprocess
import os
import io

app = Flask(__name__)


theme_folders = []
for item in os.listdir('themes'):
    if os.path.isdir(f"themes/{item}"):
        theme_folders.append(item)

MMGs = []
for index, theme_folder in enumerate(theme_folders):
    MMG = {
        "url": f"http://sp23-cs340-152.cs.illinois.edu:500{index + 1}",
        "theme": theme_folder,
    }
    MMGs.append(MMG)


def wait_for_service(url, timeout=10, interval=1):
  start_time = time.time()
  while time.time() - start_time < timeout:
    try:
      response = requests.get(url)
      if response.status_code == 200:
        print(f" ---> Service at {url} is available.")
        return True
      
    except requests.exceptions.RequestException:
      pass

open_micro_script = "./startup.sh"

process = subprocess.Popen(
    open_micro_script,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# for mmg in MMGs:
#   url = mmg['url']
#   theme = mmg['theme']
#   print(f"Current Theme: {theme}")
 
#   wait_for_service(mmg["url"])

# print(f"Current: Reducer")
# wait_for_service("http://sp23-cs340-152.cs.illinois.edu:6000")
# # # wait_for_service("http://127.0.0.1:5002")

def terminate(signal, frame):
    script_path = "./kill.sh"
    subprocess.call(script_path, shell=True)
    exit(0)

signal.signal(signal.SIGINT, terminate)


# print(themes)

@app.route('/', methods=["GET"])
def GET_index():
  '''Route for "/" (frontend)'''
  return render_template("index.html")

@app.route('/makeMosaic', methods=["POST"])
def POST_makeMosaic():
  
  start_time = time.time()
  f = request.files["image"]
  f.save("image.png")

  tiles_across = 300
  rendered_tile_size = 8

  response = []
  for mmg in MMGs:
    url = mmg['url']
    theme = mmg['theme']
    print(f"Current Theme: {theme}")
    print(f" ---> Requesting mosaic from {url} ")
    with open("image.png", "rb") as image_file:
      mmg_response = requests.post(
          f"{url}/generateMosaic",
          files={"image": image_file},
          data={"tiles_across": tiles_across, "rendered_tile_size": rendered_tile_size, "theme": theme}
      )

    if mmg_response.status_code == 200:
      print(f" ---> Received {theme} mosaic successfully ")
      response.append({"image": mmg_response.json()["image"]})
    else:
      print(f" ---> Error generating {theme} mosaic from {url}: {mmg_response.text}")

  end_time = time.time()
  
  print(f"Program Runtime: {end_time - start_time} seconds")
  return jsonify(response)




