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


theme = "marvel"

root_dir = os.path.dirname(os.path.abspath(__file__))
themes_path = os.path.join(root_dir, "..", "..", "themes", theme)
count = len(os.listdir(themes_path))
  
local_url = "http://127.0.0.1:5009/makeMosaic"
vm_url = "http://sp23-cs340-152.cs.illinois.edu:5009/makeMosaic"

vm_mid = "http://sp23-cs340-adm.cs.illinois.edu:1989/addMMG"
local_mid = "http://127.0.0.1:5000/addMMG"

mmg_data = {
    "name": theme,
    "url": vm_url,
    "author": "Shray (ssriv5)",
    "tileImageCount": count
}
response = requests.put(vm_mid, data=mmg_data)

@app.route('/', methods=["GET"])
def GET_index():
  '''Route for "/" (frontend)'''
  return "starter place"


def generateMosaic(base_image, theme, tiles_across, rendered_tile_size):
  root_dir = os.path.dirname(os.path.abspath(__file__))
  themes_path = os.path.join(root_dir, "..", "..", "themes", theme)

  images = []
  colors = []
  kd_tree = ""

  base_width, base_height = base_image.size
  # print(base_width, base_height)

  for file in os.listdir(themes_path):
    tile = Image.open(f'{themes_path}/{file}').convert('RGB').resize((rendered_tile_size, rendered_tile_size))
    avg_color = np.array(tile).mean(axis=(0, 1))
    images.append(tile)
    colors.append(avg_color)

  kd_tree = KDTree(colors)
  
  base_width, base_height = base_image.size
  aspect_ratio = float(base_height) / float(base_width)

  tile_dim = base_width // tiles_across
  tiles_down = int(aspect_ratio * tiles_across)

  mosaic_width = tiles_across * rendered_tile_size
  mosaic_height = tiles_down * rendered_tile_size

  mosaic = Image.new('RGB', (mosaic_width, mosaic_height))

  for x in range(tiles_across):
    for y in range(tiles_down):
      current_tile = base_image.crop((x * tile_dim,         # left
                                      y * tile_dim,         # top
                                      (x + 1) * tile_dim,   # right 
                                      (y + 1) * tile_dim))  # bottom
      color = np.array(current_tile).mean(axis=(0, 1))
      garbage, index = kd_tree.query([color])

      best_match = images[index[0][0]]
      resized_tile = best_match.resize((rendered_tile_size, rendered_tile_size))
      mosaic.paste(resized_tile, (x * rendered_tile_size, y * rendered_tile_size))  # (left, top)

  return mosaic

@app.route('/makeMosaic', methods=["POST"])
def POST_mmg():
    f = request.files["image"]
    img_data = f.read()
    img = Image.open(BytesIO(img_data)).convert('RGB')

    tiles_across = int(request.args.get("tilesAcross"))
    rendered_tile_size = int(request.args.get("renderedTileSize"))
    file_format = request.args.get("fileFormat", "PNG").upper()

    try:
        mosaic = generateMosaic(img, theme, tiles_across, rendered_tile_size)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    img_buffer = io.BytesIO()
    mosaic.save(img_buffer, format=file_format)


    # output_filename = f"mosaic_output.{file_format.lower()}"
    # mosaic.save(output_filename, format=file_format)

    img_buffer.seek(0)

    response = make_response(img_buffer.read())
    response.headers.set('Content-Type', f'image/{file_format.lower()}')
    response.headers.set('Content-Disposition', f'attachment; filename=mosaic.{file_format.lower()}')

    return response
 
 
