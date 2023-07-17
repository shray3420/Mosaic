from flask import Flask, jsonify, make_response, request
import base64
import time
import requests
import string
from sklearn.neighbors import KDTree
import numpy as np
from PIL import Image
import os
import io
from io import BytesIO

app = Flask(__name__)


from flask import Flask, jsonify, render_template, request
import base64
import time
import requests
import string
from sklearn.neighbors import KDTree
import numpy as np
from PIL import Image
import os
import io
from io import BytesIO

app = Flask(__name__)


local_url = "http://127.0.0.1:6000/reduceMosaic"
vm_url = "http://sp23-cs340-152.cs.illinois.edu:6000/reduceMosaic"

vm_mid = "http://sp23-cs340-adm.cs.illinois.edu:1989/registerReducer"
local_mid = "http://127.0.0.1:5000/registerReducer"

mmg_data = {
    "name": "reducer",
    "url": vm_url,
    "author": "Shray (ssriv5)"
}
response = requests.put(vm_mid, data=mmg_data)

@app.route('/', methods=["GET"])
def GET_index():
  '''Route for "/" (frontend)'''
  return "starter place"



@app.route("/reduceMosaic", methods=["POST"])
def reduce():
    baseImage = Image.open(BytesIO(request.files["baseImage"].read())).convert("RGB")
    mosaic1 = Image.open(BytesIO(request.files["mosaic1"].read())).convert("RGB")
    mosaic2 = Image.open(BytesIO(request.files["mosaic2"].read())).convert("RGB")

    renderedTileSize = int(request.args.get("renderedTileSize"))
    tilesAcross = int(request.args.get("tilesAcross"))
    fileFormat = request.args.get("fileFormat")

    base_width, base_height = baseImage.size
    aspect_ratio = float(base_height) / float(base_width)

    tile_dim = base_width // tilesAcross
    tiles_down = int(aspect_ratio * tilesAcross)

    mosaic_width, mosaic_height = mosaic1.size

    mosaic_reduction = Image.new("RGB", (mosaic_width, mosaic_height))

    for x in range(tilesAcross):
        for y in range(tiles_down):
            base_tile = baseImage.crop((x * tile_dim, y * tile_dim, (x + 1) * tile_dim, (y + 1) * tile_dim))
            base_color = np.array(base_tile).mean(axis=(0, 1))

            mosaic1_tile = mosaic1.crop((x * renderedTileSize, y * renderedTileSize, (x + 1) * renderedTileSize, (y + 1) * renderedTileSize))
            mosaic1_color = np.array(mosaic1_tile).mean(axis=(0, 1))

            mosaic2_tile = mosaic2.crop((x * renderedTileSize, y * renderedTileSize, (x + 1) * renderedTileSize, (y + 1) * renderedTileSize))
            mosaic2_color = np.array(mosaic2_tile).mean(axis=(0, 1))

            mosaic1_diff = np.linalg.norm(base_color - mosaic1_color)
            mosaic2_diff = np.linalg.norm(base_color - mosaic2_color)

            best_tile = mosaic1_tile if mosaic1_diff < mosaic2_diff else mosaic2_tile
            mosaic_reduction.paste(best_tile, (x * renderedTileSize, y * renderedTileSize))

    img_buffer = io.BytesIO()
    mosaic_reduction.save(img_buffer, format=fileFormat)
    img_buffer.seek(0)

    response = make_response(img_buffer.read())
    response.headers.set("Content-Type", f"image/{fileFormat.lower()}")

    return response



