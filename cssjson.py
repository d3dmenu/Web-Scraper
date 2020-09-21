# /**
#  * CSS-JSON Converter for Python
#  * Converts CSS to JSON.
#  * Version 2.1
#  *
#  * Released under the MIT license.
#  *
#  * Copyright (c) 2020 Tinnapat Rattanatham

#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
#  to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in all copies or substantial portions
#  of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#  */

import re
import json
from collections import defaultdict


class cssjson:
    def __init__(self):
        self.children = r"([^\s\;\{\}][^\;\{\}]*)\{"
        self.attributes = r"([^\;\{\}]*)\;"
        self.endX = r"\}"

        # This is used, a concatenation of all above. We use alternation to
        # capture.
        # self.altX = r"(\/\*[\s\S]*?\*\/)|([^\s\;\{\}][^\;\{\}]*(?=\{))|(\})|([^\;\{\}]+\;(?!\s*\*\/))"
        self.altX = r"(\/\*[\s\S]*?\*\/)|([^\s\;\{\}][^\;\{\}]*(?=\{))|(\})|([^\;\{\}]+\;(?!\s*\*\/))|([^\s\;\{\}][^\;\{\}]*)"
        # json groups
        self.data = {"children": {}, "attributes": {}}
        self.key = 0
        self.value = 1

        # json status
        self.statename = ""

        # Capture groups
        self.capComment = 0
        self.capSelector = 1
        self.capEnd = 2
        self.capAttr = 3
        self.capLast = 4

    def visualizer(self, cssString):
        dom = re.findall(self.altX, cssString)
        # print(dom)
        _result, _dict, _key, _value = {}, {}, "", ""
        for group in range(len(dom)):

            for index in range(len(dom[group])):
                args = dom[group][index]

                if args != "":
                    if index == self.capComment:
                        pass  # Comment

                    elif index == self.capSelector:
                        # Get name dict
                        self.statename = args
                        if args not in self.data["children"]:
                            self.data["children"][self.statename] = {
                                # "children": {},
                                "attributes": {},
                            }
                        else:
                            pass

                        _dict = self.data["children"][self.statename]["attributes"]

                    elif index == self.capEnd:

                        # print(_dict)
                        for i in _dict:
                            # print(i, _dict[i], type(_dict[i]), self.value)
                            if type(_dict[i]) != list:
                                _dict[i] = [_dict[i]]

                            if len(_dict[i]) <= self.value:

                                try:
                                    _result[i] = float("".join(map(str, _dict[i])))
                                except:
                                    _result[i] = "".join(map(str, _dict[i]))
                            else:
                                _result[i] = _dict[i]

                        self.data["children"][self.statename]["attributes"] = _result

                        # Set variable to empty
                        _result, _dict, _key, _value = {}, {}, "", ""

                    elif index == self.capAttr or index == self.capLast:
                        # Check key ':' split string
                        ex = str(args).split(":")

                        # Extract string [key:value]
                        try:
                            _key = ex[self.key]
                            _value = ex[self.value]
                        except:
                            pass
                        # print(_key, _value)
                        # Appending key and value
                        # remove symbols ";"
                        _dict.setdefault(_key, [])
                        try:
                            _dict[_key].append(_value.replace(";", ""))
                        except:
                            pass


# code = cssjson()


# f = open("reader.txt", "r", encoding="utf-8")
# n = f.read()
# f.close()
# code.visualizer(n)

# app_json = json.dumps(code.data, sort_keys=False)
# print("\n", app_json)
