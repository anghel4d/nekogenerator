import json
import os
import sys

def move_string_in_json(directory, string_pairs):
  """
  Moves strings to desired locations in JSON files within a directory.

  Args:
      directory: The directory containing the JSON files.
      string_pairs: A list of (string, desired_index) pairs.
  """
  for filename in os.listdir(directory):
    if filename.endswith(".json"):
      filepath = os.path.join(directory, filename)
      with open(filepath, "r+") as f:
        data = json.load(f)
        for string, desired_index in string_pairs:
          if string in data:
            index = data.index(string)
            if index != desired_index:
              data.pop(index)
              data.insert(desired_index, string)
        f.seek(0)
        json.dump(data, f, indent=2)

def insert_string_after_string(directory, string_triples):
  """
  Inserts a string after another string in JSON files within a directory.

  Args:
      directory: The directory containing the JSON files.
      string_triples: A list of (string1, string2, desired_index) triples.
  """
  for filename in os.listdir(directory):
    if filename.endswith(".json"):
      filepath = os.path.join(directory, filename)
      with open(filepath, "r+") as f:
        data = json.load(f)
        for string1, string2, desired_index in string_triples:
          if string1 in data:
            index = data.index(string1)
            data.insert(desired_index, string2)  # Add after string1
            f.seek(0)
            json.dump(data, f, indent=2)

# Example usage
directory = sys.argv[1]
if not os.path.exists(directory):
  print("Try again NIGGER!")
  exit(696969)
string_pairs = [("Extra/Wings.png", 4), ("Extra/Scarlet.png", 4)]
string_triples = [("Hat/BellTop.png", "Hat/BellBottom.png", 2)]
move_string_in_json(directory, string_pairs)
insert_string_after_string(directory, string_triples)
