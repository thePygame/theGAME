import json

data = {"12.05.2023": {"POINTS": 55, "DISTANCE": 1145, "BANANAS": 7},
        "13.05.2023": {"POINTS": 10, "DISTANCE": 2567, "BANANAS": 9},
        "14.05.2023": {"POINTS": 25, "DISTANCE": 1456, "BANANAS": 15},
        "15.05.2023": {"POINTS": 15, "DISTANCE": 324, "BANANAS": 3},
        "16.05.2023": {"POINTS": 85, "DISTANCE": 3663, "BANANAS": 8}}

data = {"SCORE": 155, "DISTANCE": 4550, "BANANAS": 48}

with open("data.json", "w") as f:
    json.dump(data, f)

#
# def print_dictionary(data):
#     for i in data:
#         print(f"[{i}] {data[i]}")


# with open("data.json", "r") as f:
#     text = json.load(f)
#     print(f"ZAWARTOŚĆ PLIKU:")
#     print_dictionary(text)
#     # pop = text.pop("13.05.2023")
#     print("POP")
#     print_dictionary(text)
# with open("data.json", "w") as f:
#     json.dump(text, f)
# with open("data.json", "r") as f:
#     text = json.load(f)
#     print(f"ZAWARTOŚĆ PLIKU PO POPIE:")
#     print_dictionary(text)

# def funkcja_funkcja():
#     score = 0
#     with open("data.json", "r") as f:
#         data = json.load(f)
#         for i in data:
#             print(f"[{i}] {data[i]}")
#             if i == "SCORE":
#                 print("ASDASDADS")
#
#             # for j in data[i]:
#             #     print(f"[{j}] {data[i][j]}")
#             #     if j == "SCORE":
#             #         print("MAKAKA")


# funkcja_funkcja()
