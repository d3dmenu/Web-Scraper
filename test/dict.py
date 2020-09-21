import json

data = {
    "children": {
        "_D1W65": {
            "children": {"value": 62},
            "attributes": {"bold": "True", "size": 12},
        }
    },
    "attributes": {},
}
# add element
data["children"]["_1WD59"] = {
    "children": {"value": 79},
    "attributes": {"color": "#000", "size": 20, "color": "#111"},
}
# edit element
# data["children"]["_D1W65"]["children"] = {"value": 89}
# print(data, "\n")

# app_json = json.dumps(data, sort_keys=False)
# print(app_json)

_dict = {
    "text-decoration": ["none"],
    "color": ["rgba(0,0,0,.8)", "rgba(0,0,0,.54)"],
    "white-space": ["nowrap"],
    "display": ["block"],
    "margin-left": ["13px"],
}

for i in _dict:
    # print(i, "".join(map(str, _dict[i])))
    print(i, _dict[i])
# print(_dict["color"][1])
