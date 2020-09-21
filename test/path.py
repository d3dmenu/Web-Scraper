import json


def pathGet(dictionary, path):
    for item in path.split("/"):
        dictionary = dictionary[item]
        print(item)
    return dictionary


def pathSet(dictionary, path, setItem):
    path = path.split("/")
    key = path[-1]
    dictionary = pathGet(dictionary, "/".join(path[:-1]))
    dictionary[key] = setItem


def pathBack(path):
    path = path.split("/")
    del path[-1]
    return "/".join(map(str, path))


_dict = {
    "children": {
        "._1RGarK": {
            "children": {
                "Nick": {
                    "children": {},
                    "attribute": {"height": "177", "weight": "80"},
                },
            },
            "attributes": {
                "box-shadow": "0 1px 1px 0 rgba(0,0,0,.05)",
                "border-radius": ".125rem",
                "overflow": "hidden",
                "background": "#fff",
                "margin-top": "1.25rem",
                "height": "5rem",
            },
        },
    },
    "attributes": {},
}

# pathGet(_dict, "children/._1RGarK/children/Nick")
print(pathBack("children/._1RGarK/children/Nick"))
# pathSet(_dict, "children/hextor", {"children": {}, "attributes": {"height": "178"}})
# print(_dict)
# var = _dict["children"]["._1RGarK"]["children"]["Nick"]["children"]
# print(_dict)
