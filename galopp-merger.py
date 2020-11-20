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

    print(csv_file_paths)


if __name__ == '__main__':
    merge()
