import json
import os

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
              print(f"Extras layering hotfix: {filename}")
              data.pop(index)
              data.insert(desired_index, string)
        f.seek(0)
        json.dump(data, f, indent=2)

def conditional_move_string_in_json(directory, triples):
  """
  Moves strings to desired locations in JSON files within a directory.

  Args:
    directory: The directory containing the JSON files.
    triples: A list of triples (string1, string2, desired_index).
  """
  for filename in os.listdir(directory):
    if filename.endswith(".json"):
      filepath = os.path.join(directory, filename)
      with open(filepath, "r+") as f:
        data = json.load(f)
        for string1, string2, desired_index in triples:
          # Check if strings exist and desired index is valid
          if string1 in data and string2 in data and 0 <= desired_index < len(data):
            index1 = data.index(string1)
            index2 = data.index(string2)
            if index1 != desired_index:
              print(f"Ginger/Crying hotfix: {filename}")
              data.pop(index1)
              data.insert(desired_index, string1)
            else:
              print(f"Ginger/Crying correct position: {filename}")
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
            print(f"Bells hotfix: {filename}")
            index = data.index(string1)
            data.insert(desired_index, string2)  # Add after string1
            f.seek(0)
            json.dump(data, f, indent=2)

# Example usage
directory = "/home/cris/Documents/dev/composite/CatBuilderData"
string_pairs = [("Extra/Wings.png", 4), ("Extra/Scarlet.png", 4)]
string_triples = [("Hat/BellTop.png", "Hat/BellBottom.png", 2)]
triple = [("Eyes/Crying.png", "Hair/GingerOrange.png", 3), ("Eyes/Crying.png", "Hair/GingerPink.png", 3)]

conditional_move_string_in_json(directory, triple)
move_string_in_json(directory, string_pairs)
insert_string_after_string(directory, string_triples)
