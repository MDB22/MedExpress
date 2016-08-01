import os

for file in os.listdir("./"):
    if file.endswith(".kml"):
        print(file)