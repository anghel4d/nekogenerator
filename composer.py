import json
import os
import subprocess
import sys
from PIL import Image
from multiprocessing import Pool

start_cat = int(sys.argv[2])
builder_data_dir = sys.argv[4]
if not os.path.exists(builder_data_dir):
    print("Try again NIGGER!")
    exit(696969)

script_dir = os.path.dirname(__file__)

def build(catIndex):
    print(catIndex)

def builda(catIndex):
    builderPath = builder_data_dir + '/' + str(catIndex + 1) + ".json"
    absBuilderPath = os.path.join(script_dir, builderPath)
    catFiles = []
    with open(absBuilderPath) as json_file:
        catFiles = json.load(json_file)

    background = Image.open('parts/' + 'output.png')
    print(catIndex)

    os.makedirs(os.path.dirname("./cats"), exist_ok=True)
    for fileIndex in range(len(catFiles)):
        foreground = Image.open('parts/' + catFiles[fileIndex])

        # Check dimensions and resize if necessary
        if foreground.size != background.size:
            foreground = foreground.resize(background.size)

        background = Image.alpha_composite(background, foreground)

    background.save('./cats/' + str(catIndex+1) + '.png')

if __name__ == '__main__':
    num_threads = int(sys.argv[1])
    cats_wanted = int(sys.argv[3])

    # main SIMD loop
    iterations = cats_wanted // num_threads - 1
    for i in range(start_cat - 1, iterations):
        with Pool(num_threads) as p:
            indices = []
            for t in range(0, num_threads):
                indices.append((i * num_threads) + t)
            p.map(build, indices)
    
    # Scalar tail
    remaining = cats_wanted - (iterations * num_threads)
    last_cat = cats_wanted - remaining
    for i in range(last_cat, cats_wanted):
        with Pool(remaining) as p:
            indices = []
            for t in range(0, remaining):
                indices.append((i * remaining) + t)
            p.map(build, indices)
            
"""
size_t i = 0;

  // main SIMD loop
  for (; i + 32 < n; i)
  {
    __m128i word = _mm_lddqu_si128((const __m128i *)(src + i));
    __m128i mask = _mm_cmpeq_epi8(word, _mm_setzero_si128());

    // test if there are any 0 bytes and terminate
    if ((_mm_movemask_epi8(mask) & 0xffff'ffff) != 0)
      break;

    _mm_storeu_si128((__m128i *)(dst + i), word);
  }

  // scalar tail
  for (size_t i = 0; i < n && src[i]; ++i)
    dst[i] = src[i];
  return dst;
  """