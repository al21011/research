# -*- coding: utf-8 -*-
import csv
from xml.etree import ElementTree

def xml2csv():
    input_file = "xmlDataFile/export.xml"
    output_file = "healthdata.csv"

    # CSV 作成
    f = open(output_file, "w")

    # ヘッダー
    output_string = "公表年,公表月,公表日,都道府県,患者数（2020年3月28日からは感染者数）,現在は入院等,退院者,死亡者\n"

    # ヘッダー書き込み
    f.write(output_string)

    # XML 読込
    tree = ElementTree.parse(output_file)

    # ルート
    root = tree.getroot()

    text_list = []

    for r in root:

        if r.tag == "date":
            text_list.append(r.find('year').text)
            text_list.append(r.find('month').text)
            text_list.append(r.find('day').text)

        elif r.tag == "prefecture":
            text_list.append(r.text)

        elif r.tag == "info":
            text_list.append(r.find('cases').text)
            text_list.append(r.find('hospitalized').text)
            text_list.append(r.find('released').text)
            text_list.append(r.find('death').text)

        if len(text_list) == 8:
            # CSV に書き込み
            output_string = text_list[0] \
                            + "," + text_list[1] \
                            + "," + text_list[2] \
                            + "," + text_list[3] \
                            + "," + text_list[4] \
                            + "," + text_list[5] \
                            + "," + text_list[6] \
                            + "," + text_list[7] + "\n"

            f.write(output_string)

            # リストをクリア
            text_list = []

    f.close

if __name__ == '__main__':
    xml2csv()