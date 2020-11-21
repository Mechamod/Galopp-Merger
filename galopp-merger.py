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
    csv_file_paths.sort() # Sort at the end for correct ordered files!

    # Load each file as text and append it to another.
    with open("all_races.csv", "w") as all_races_csv:
        all_races_csv.write("Date,Location,Distance,Prize,Category,Class,Ground_state,Horses")
        for path in csv_file_paths:
            with open(path, "r") as csv_file:
                column_line = True
                for line in csv_file.readlines():
                    if column_line:
                        column_line = False
                        continue
                    all_races_csv.write(line)


if __name__ == '__main__':
    merge()
