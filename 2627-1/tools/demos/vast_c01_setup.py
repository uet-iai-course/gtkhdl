import os, re, urllib.request, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image

URL = "https://visualdata.wustl.edu/varepository/VAST_Challenge_2011/datasets/MC_1_Materials_3-30-2011.zip"
FOLDER = "MC_1_Materials_3-30-2011"

if not os.path.isdir(FOLDER):              # chỉ tải khi chưa có
    urllib.request.urlretrieve(URL, "mc1.zip")
    zipfile.ZipFile("mc1.zip").extractall(".")

for name in sorted(os.listdir(FOLDER)):
    size = os.path.getsize(os.path.join(FOLDER, name)) / 1e6
    print(f"{name:26s} {size:8.2f} MB")
