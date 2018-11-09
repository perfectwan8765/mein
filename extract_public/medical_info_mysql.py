import urllib.request as rq
import urllib
import datetime
import json
from itertools import count
import pymysql
import pandas as pd

def update_json_file(file_name):
    jData = open(file_name, 'r', encoding='utf-8').read()
    jData = json.loads(json.dumps(jData))
    # print(jData)
    jData = jData.replace("][", ",")
    f = open('medical_new_info_종로구.json', 'w', encoding='utf-8')
    f.write(jData)
    f.close()

def get_json_file(file_name):
    jData = json.loads(open(file_name, 'r', encoding='utf-8').read())
    # print(jData)
    save_date_mysql(jData)

def save_date_mysql(jsonResult):
    conn = pymysql.connect(host='127.0.0.1', user='zerosw', password='123456', db='meindb')
    cursor = conn.cursor()

    sql = 'insert into infos_maininfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    sql2 = 'insert into infos_subinfo(mondayStart, mondayEnd, tuesdayStart, tuesdayEnd,' \
           ' wednesdayStart, wednesdayEnd, thursdayStart, thursdayEnd, fridayStart, fridayEnd, ' \
           'saturdayStart, saturdayEnd, sundayStart, sundayEnd, holidayStart, holidayEnd, hpid_id)' \
           ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    for item in jsonResult:
        data = (item['hpid'], item['name'], item['div'], item['subject'], item['tel'], item['etel'],
                item['info'], item['lat'], item['lon'], item['addr'], item['emergency'], item['limbs'],
                item['pregnent'], item['newborn'], item['burn'], item['dialysis'])
        print('data:', data)

        data2 = (item['mondayStart'], item['mondayEnd'], item['tuesdayStart'], item['tuesdayEnd'],
                 item['wednesdayStart'], item['wednesdayEnd'], item['thursdayStart'], item['thursdayEnd'],
                 item['fridayStart'], item['fridayEnd'], item['saturdayStart'], item['saturdayEnd'],
                 item['sundayStart'], item['sundayEnd'], item['holidayStart'], item['holidayEnd'], item['hpid'])
        print('data2:', data2)

        cursor.execute(sql, data)
        cursor.execute(sql2, data2)

    conn.commit()
    cursor.close()
    conn.close()
    print("database save")

if __name__ == '__main__':
    # update_json_file('medical_info_종로구.json')
    # get_json_file('medical_new_info_종로구.json')