# /**
#  * CSS-JSON Converter for JavaScript
#  * Converts CSS to JSON and back.
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

import os
import re
import sys
import bs4
import time
import json
import requests
import lxml.html
import pandas as pd

# from lib import setup
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from cssjson import cssjson

# Helper function


class helper:

    # Helper Method

    def __init__(self, url, path, style, option):
        self.url = url
        self.path = path
        self.style = style
        self.option = option
        self.css_name = []
        self.class_name = []  # qaNIZv
        self.found_attr = []
        self.notfound_attr = []
        self.text_css = ""

        self.allcss = ""
        # This is used, a concatenation of all above. We use alternation to
        # chldren.
        self.children = r"([^\s\;\{\}][^\;\{\}]*)\{"
        os.chdir(self.path)

    def import_data():
        file = open("index.html", "r", encoding="utf-8")
        html = file.read()
        file.close()
        return html

    def export_data(e):
        file = open("index.html", "w+", encoding="utf-8")
        file.write(e)
        file.close()

    def load_url(self):
        if self.option:
            options = webdriver.ChromeOptions()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--incognito")
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                self.path + "chromedriver.exe", chrome_options=options
            )
        else:
            self.driver = webdriver.Chrome(self.path + "chromedriver.exe")

        self.driver.get(self.url)

        # Delay setting
        time.sleep(3)
        source = self.driver.page_source
        helper.export_data(source)

    def cleansing_syntag(self):
        html = helper.import_data()

        word = BeautifulSoup(html, "lxml").text
        word = word.replace("\n", "")
        helper.export_data(word, "index")

    def get_class_v1(self):
        html = helper.import_data()

        # Search index key "class="
        index = [m.start() for m in re.finditer("class=", html)]

        for i in range(len(index)):
            value = ""

            # Loop check name
            for j in range(7, 300):
                key = index[i] + j
                if html[key] != '"':
                    value += str(html[key])
                else:

                    # Write item to data_class
                    if value != "":
                        if value not in self.class_name:
                            self.class_name.append(value)
                    break

    def get_class_v2(self):
        html = helper.import_data()
        dom = re.findall(self.children, html)
        return dom

    def get_cssurl(self):
        html = helper.import_data()
        soup = BeautifulSoup(html, "html.parser")
        os.chdir(self.style)
        
        for link in soup.find_all("link", rel="stylesheet", href=True):
            print("[Loading] -", link["href"])
            url_css = link["href"]
            r = requests.get(url_css, allow_redirects=True)

            css = url_css.split("/")
            name_css = css[-1]
            self.css_name.append(name_css)
            open(name_css, "wb").write(r.content)

            cj = cssjson()
            text = str(r.content, "utf-8")

            try:  # cannot convert file bundle
                cj.visualizer(text)
                self.allcss += text
            except:
                pass

    def get_attr(self, classname):
        size, style = len(classname), ""
        for i in range(len(self.css_name)):
            file = open(self.css_name[i], "r", encoding="utf-8")
            self.text_css = file.read()
            file.close()
            if self.text_css.count(classname) != 0:
                index = self.text_css.index(classname)
                for j in range(size, 900):
                    key = index + j
                    if self.text_css[key - 1] != "}":
                        style += str(self.text_css[key])
                    else:
                        if style != "":
                            self.found_attr.append(classname)
                            return helper.toJSON(style, classname)
        else:
            if classname not in self.notfound_attr:
                self.notfound_attr.append(classname)
                return None

    def toJSON(text, classname):
        # print(text)
        word = str(text)
        word = word.replace(":", '":"')
        word = word.replace(";", '","')
        word = word.replace("{", '{"')
        word = word.replace("}", '"}')
        return '{"' + str(classname) + '":' + str(word) + "}"

    def Hextodecimal(hex):
        return int(hex, 16)

    def RGBtoHex(r, g, b):
        rgb = (r, g, b)
        hex_result = "".join([format(val, "02X") for val in rgb])
        return helper.Hextodecimal((f"{hex_result}"))

    def RemtoPx(size):
        return size / 0.0625


# print(helper.h(245, 114, 36))
# print(helper.Hextodecimal("212121"))
# print(helper.RemtoPx(1.5))
