import setup
import json
from helper import helper
from cssjson import cssjson
from setup import installed

# shopee
url = "https://shopee.co.th/%E0%B8%94%E0%B8%AD%E0%B8%81%E0%B9%80%E0%B8%94%E0%B8%8B%E0%B8%B5%E0%B9%88%E0%B8%82%E0%B8%99%E0%B8%B2%E0%B8%94%E0%B9%80%E0%B8%A5%E0%B9%87%E0%B8%81-%E0%B8%9E%E0%B8%A3%E0%B8%B5%E0%B9%80%E0%B8%A1%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B8%A1%E0%B8%AD%E0%B8%AD%E0%B8%81%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B8%94%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B9%80%E0%B8%94%E0%B8%B4%E0%B8%A1-%E0%B8%95%E0%B9%88%E0%B8%B2%E0%B8%87%E0%B8%AB%E0%B8%B9%E0%B9%81%E0%B8%9F%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99-INS-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%9C%E0%B8%B9%E0%B9%89%E0%B8%AB%E0%B8%8D%E0%B8%B4%E0%B8%87-%E0%B9%82%E0%B8%8B%E0%B9%88%E0%B9%84%E0%B8%AB%E0%B8%9B%E0%B8%A5%E0%B8%B2%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%AD%E0%B8%B4%E0%B8%99%E0%B9%84%E0%B8%97-%E0%B8%AD%E0%B8%B2%E0%B8%A3%E0%B8%A1%E0%B8%93%E0%B9%8C%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%9A%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2-%E0%B8%95%E0%B9%88%E0%B8%B2%E0%B8%87%E0%B8%AB%E0%B8%B9%E0%B8%AA%E0%B8%B5%E0%B9%81%E0%B8%94%E0%B8%87%E0%B8%95%E0%B8%B2%E0%B8%82%E0%B9%88%E0%B8%B2%E0%B8%A2%E0%B8%9B%E0%B9%88%E0%B8%B2-%E0%B8%AD%E0%B8%B8%E0%B8%9B%E0%B8%81%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B9%80%E0%B8%AA%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%A5%E0%B8%B2%E0%B8%A2%E0%B8%94%E0%B8%AD%E0%B8%81%E0%B9%84%E0%B8%A1%E0%B9%89-%E0%B9%80%E0%B8%AA%E0%B8%B7%E0%B9%89%E0%B8%AD%E0%B8%9C%E0%B9%89%E0%B8%B2%E0%B9%81%E0%B8%9F%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5-%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%94%E0%B8%B1%E0%B8%9A%E0%B9%81%E0%B8%9F%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5-%E0%B8%A3%E0%B8%B1%E0%B8%94-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%84%E0%B8%AD-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%A1%E0%B8%B7%E0%B8%AD-%E0%B9%81%E0%B8%AB%E0%B8%A7%E0%B8%99-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%A5%E0%B8%B2%E0%B8%A2%E0%B8%94%E0%B8%AD%E0%B8%81%E0%B9%84%E0%B8%A1%E0%B9%89-i.251414252.4732325115"

# lazada
# url = "https://www.lazada.co.th/products/apple-ipad-pro-129-inch-wi-fi-cellular-64gb-space-grey-i160587876-s193401386.html?spm=a2o4m.searchlistbrand.list.1.72e35f5dnoHmvI&search=1"

# Amazon
# url = "https://www.amazon.com/AmazonBasics-Premium-Dual-Monitor-Stand/dp/B07QNY2D3H/ref=sr_1_2?dchild=1&keywords=amazonbasics&pf_rd_p=9349ffb9-3aaa-476f-8532-6a4a5c3da3e7&pf_rd_r=2B29DFQMFKQ6D7M16S5V&qid=1599222229&sr=8-2"

# Ebay
# url = "https://www.ebay.com/itm/New-Balance-Mens-Classic-993-Running-Shoes-Red/192786546031?_trkparms=aid%3D1110012%26algo%3DSPLICE.SOIPOST%26ao%3D1%26asc%3D20200818142651%26meid%3Dcc579c42d01c42b697a4d810d78853f7%26pid%3D101196%26rk%3D3%26rkt%3D12%26mehot%3Dpp%26sd%3D202434093504%26itm%3D192786546031%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DPromotedSellersOtherItemsV2%26brand%3DNew+Balance&_trksid=p2047675.c101196.m2219"

path = "C:/Users/Smurf/Desktop/Engine/driver/"
style = "C:/Users/Smurf/Desktop/Engine/stylesheet/"
# qaNIZv


def main():

    sc = helper(url, path, style, True)
    sc.get_class_v1()  # Get class name from web
    sc.get_cssurl()  # Get css page from web
    data, result = sc.class_name, ""
    for i in range(len(data)):
        result = str(sc.get_attr(data[i]))

    # ============================================================================================================

    convert = cssjson()  # object variable
    class_found = sc.found_attr  # found class in html (found 175 class)
    convert.visualizer(
        sc.allcss
    )  # นำข้อมูลไฟล์ css ทุกไฟล์มารวมกันแล้วเปลี่ยน type เป็น dict
    css_dict = convert.data  # dictionary all css

    datatest = {}
    for j in range(len(class_found)):
        name = "." + class_found[j]
        try:
            # แสดงคุณสมบัติของคลาสที่พบใน html หน้านั้นๆ โดยใช้ข้อมูลจาก ไฟล์ css ทุกไฟล์ที่ทำการหามาตอนแรก [css_dict]
            print("{'%s'}:%s" % (name, css_dict["children"][name]["attributes"]))

            # จัดเรียงคุณสมบัติเพื่อให้ได้ class ที่มีคุณสมบัติครบตามต้องการ
            datatest[name] = {
                "font-size": css_dict["children"][name]["attributes"]["font-size"],
                "font-weight": css_dict["children"][name]["attributes"]["font-weight"],
                # "word-same": 2,
                "line-height": css_dict["children"][name]["attributes"]["line-height"],
                # "state-price": 0,
            }
        except:
            pass
    # try เพราะ ไฟล์ bundle.css มีปัญหาไม่สามารถแปลงไฟล์ได้ส่งผลให้ class ที่อยู่ใน html หน้านั้น แล้วมี Attribute เก็บไว้ใน Bundle ไม่สามารถดึงมาใช้งานได้ เพราะแปลงไฟล์ bundle เป็น dict ไม่ได้

    # ปัญหาใหม่ ตรวจสอบ style จากเว็บแล้วพบ font-size font-weight line-height แต่่วิธีที่เราดึงเราดึงจาก link rel แล้วปรากฏว่า มันมีไม่ครบมีแค่ font-size กับ font-weight
    # คำถามคือทำไมในเว็บถึงมี line-height ได้ ทั้งๆที่ใน link rel ตรวจสอบทุกไฟล css แล้วว่าไม่มี
    print("\n", datatest)
    # ============================================================================================================


if __name__ == "__main__":
    # installed()
    main()
