import pandas as pd
import os

def merge():
    print("Start merging alls csv files")

    # Get file paths
    csv_file_paths = []
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = str(os.path.join(root, file))
            if file_path[-4:] == ".csv":
                csv_file_paths.append(file_path)

    # Load each file as text and append it to another.
    # Remove first line, as it contains column names
    got_columns = False
    with open("all_races.csv", "a") as all_races_csv:
        for path in csv_file_paths:
            with open(path, "r") as csv_file:
                for line in csv_file.readlines():

                    # Get columns if not done yet
                    if not got_columns:
                        all_races_csv.write(line)
                        got_column = True

                    # Write each line if it isnt the column line
                    if not line.startswith("Date"):
                        all_races_csv.write(line)


if __name__ == '__main__':
    merge()
