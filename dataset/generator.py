import csv, os
import random

# Content Product Offers
symbol = ["$", "¥", "€", "£", "฿"]


def CreatDataset(r):
    data = []
    size, weight, same, lineheight, Stateprice = 0, 0, 0, 0, 0
    if r == 1:
        size = random.randint(16, 22)
        weight = random.randint(400, 800)
        same = random.randint(1, 5)
        lineheight = "{:.1f}".format(random.uniform(16, 24))
        Stateprice = 0

    elif r == 0:
        size = random.randint(12, 19)  # 12, 14
        weight = random.randint(200, 400)  # 200, 300
        same = random.randint(1, 5)  # 0
        lineheight = "{:.1f}".format(random.uniform(18, 30))
        Stateprice = 0

    elif r == 2:
        size = random.randint(15, 30)
        weight = random.randint(500, 700)
        same = random.randint(0, 8)
        lineheight = "{:.1f}".format(random.uniform(14, 20.08))
        Stateprice = 1
    data = [r, size, weight, same, lineheight, Stateprice]
    return data


os.chdir("C:/Users/Smurf/Desktop/Engine/dataset/")

with open("dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Class",
            "Font-size",
            "Font-weight",
            "Word-same",
            "Line-height",
            "State-price",
        ]
    )
    r = 0
    for i in range(100000):
        if r == 0:
            r = 1
        elif r == 1:
            r = 2
        elif r == 2:
            r = 0
        writer.writerow(CreatDataset(r))
