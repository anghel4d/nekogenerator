import argparse
import os

def find_files(dir_path, string1, string2):
  matching_files = []
  for filename in os.listdir(dir_path):
    if filename.startswith('.'):
      continue
    file_path = os.path.join(dir_path, filename)
    if os.path.isfile(file_path):
      with open(file_path, 'r') as f:
        file_content = f.read()
        if string1 in file_content and string2 in file_content:
          matching_files.append(filename)
  return matching_files

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Find files containing both strings.")
  parser.add_argument("directory", help="Path to the directory to search.")
  parser.add_argument("string1", help="First string to search for.")
  parser.add_argument("string2", help="Second string to search for.")

  args = parser.parse_args()

  matching_files = find_files(args.directory, args.string1, args.string2)

  if matching_files:
    print("Files containing both strings:")
    for filename in matching_files:
      print(filename)
  else:
    print("No files found containing both strings.")
