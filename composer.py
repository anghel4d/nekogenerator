import json
import os
import subprocess
import sys
from PIL import Image
from multiprocessing import Pool

start_cat = int(sys.argv[1])

script_dir = os.path.dirname(__file__)

def build(catIndex):
    builderPath = "CatBuilderData/" + str(catIndex + 1) + ".json"
    absBuilderPath = os.path.join(script_dir, builderPath)
    catFiles = []
    with open(absBuilderPath) as json_file:
        catFiles = json.load(json_file)

    background = Image.open('output.png')
    print(catIndex)

    for fileIndex in range(len(catFiles)):
        foreground = Image.open('parts/' + catFiles[fileIndex])

        # Check dimensions and resize if necessary
        if foreground.size != background.size:
            foreground = foreground.resize(background.size)

        background = Image.alpha_composite(background, foreground)

    background.save('./cats/' + str(catIndex+1) + '.png')

if __name__ == '__main__':
    for catIndex in range(start_cat - 1, 500):
        with Pool(10) as p:
            p.map(build, [(catIndex * 10), (catIndex * 10) + 1, (catIndex * 10) + 2,
                          (catIndex * 10) + 3, (catIndex * 10) + 4, (catIndex * 10) + 5,
                          (catIndex * 10) + 6, (catIndex * 10) + 7, (catIndex * 10) + 8,
                          (catIndex * 10) + 9])
