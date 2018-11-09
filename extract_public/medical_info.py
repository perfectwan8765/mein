import urllib.request as rq
import urllib
import datetime
import json
from itertools import count
import pymysql

def get_url_request(url):
    req = rq.Request(url)

    try:
        response = rq.urlopen(req)
        if response.getcode() == 200:
            print("Request Success: %s , %s" % (url,datetime.datetime.now()))
            return response.read().decode('utf-8')
        else:
            print("Request Failure: %s , %s" % (url,datetime.datetime.now()))
            return None

    except Exception as e:
        print(e)
        return None

def get_hospital_div(lat, lon, hpid):
    base = "http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncLcinfoInqire"
    access_key = "?_type=json&serviceKey=" +"ZUWGoqtxSHbAZ2uscevjEZEQOWzRJiJhjlFdwQbfsWHl3hnHeYmVG1BFrnxmK%2FCVga%2F%2FE5MEaobdQu437QBsRw%3D%3D"
    parameters = "&WGS84_LAT=%s&WGS84_LON=%s" % (lat, lon)

    url = base + access_key + parameters

    divData = get_url_request(url)

    if divData == None:
        print('none')
        return ''

    try:
        divData = json.loads(divData)
    except Exception as e:
        print(e)
        return ''

    for item in divData["response"]["body"]["items"]["item"]:
        if item["hpid"] == hpid:
            return(item["dutyDivName"])

    return ''

def save_date_mysql(jsonResult):
    conn = pymysql.connect(host='127.0.0.1', user='zerosw', password='123456', db='meindb')
    cursor = conn.cursor()

    sql = 'insert into infos_maininfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    sql2 = 'insert into infos_sub1info(mondayStart, mondayEnd, tuesdayStart, tuesdayEnd,' \
           ' wednesdayStart, wednesdayEnd, thursdayStart, thursdayEnd, fridayStart, fridayEnd, ' \
           'saturdayStart, saturdayEnd, sundayStart, sundayEnd, holidayStart, holidayEnd, hpid_id)' \
           ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    for idx, item in enumerate(jsonResult):
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

def get_hospital_list(q0, q1, i):
    base = "http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"
    access_key = "?_type=json&serviceKey=" +"ZUWGoqtxSHbAZ2uscevjEZEQOWzRJiJhjlFdwQbfsWHl3hnHeYmVG1BFrnxmK%2FCVga%2F%2FE5MEaobdQu437QBsRw%3D%3D"
    parameters = "&Q0=%s&Q1=%s&pageNo=%d" %(urllib.parse.quote(q0), urllib.parse.quote(q1), i)

    url = base + access_key + parameters
    print("url:", url)

    rData = get_url_request(url)

    if rData == None:
        return None

    hpid_list = []

    rData = json.loads(rData)

    for item in rData["response"]["body"]["items"]["item"]:
        hpid_list.append(item['hpid'])

    return hpid_list


def get_url_data(hp):
    base = "http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlBassInfoInqire"
    access_key = "?_type=json&serviceKey=" +"ZUWGoqtxSHbAZ2uscevjEZEQOWzRJiJhjlFdwQbfsWHl3hnHeYmVG1BFrnxmK%2FCVga%2F%2FE5MEaobdQu437QBsRw%3D%3D"
    pageNo = "&HPID=%s" % hp

    url = base + access_key + pageNo
    print("url:", url)

    rData = get_url_request(url)

    if rData == None:
        print(None)
        return None

    try:
        rData = json.loads(rData)
    except Exception as e:
        print(e)
        return None

    jsonResult = []
    print(rData['response']['body']['items']['item']["hpid"])

    item = rData['response']['body']['items']['item']
    hpid = '' if "hpid" not in item.keys() else item["hpid"]
    lat = 0 if "wgs84Lat" not in item.keys() else item["wgs84Lat"]
    lon = 0 if "wgs84Lon" not in item.keys() else item["wgs84Lon"]
    if lat == 0 and lon == 0:
        div = ""
    else:
        div = get_hospital_div(lat, lon, hpid)
    name = '' if 'dutyName' not in item.keys() else item['dutyName']
    subject = '' if "dgidIdName" not in item.keys() else item["dgidIdName"]
    tel = '' if "dutyTel1" not in item.keys() else item["dutyTel1"]
    etel = '' if"dutyTel3" not in item.keys() else item["dutyTel3"]
    info = '' if "dutyInf" not in item.keys() else item["dutyInf"]
    mondayStart = '' if "dutyTime1s" not in item.keys() else str(item["dutyTime1s"])[:2] + ":" + str(item["dutyTime1s"])[2:]
    mondayEnd = '' if "dutyTime1c" not in item.keys() else str(item["dutyTime1c"])[:2] + ":" + str(item["dutyTime1c"])[2:]
    tuesdayStart = '' if "dutyTime2s" not in item.keys() else str(item["dutyTime2s"])[:2] + ":" + str(item["dutyTime2s"])[2:]
    tuesdayEnd = '' if "dutyTime2c" not in item.keys() else str(item["dutyTime2c"])[:2] + ":" + str(item["dutyTime2c"])[2:]
    wednesdayStart = '' if "dutyTime3s" not in item.keys() else str(item["dutyTime3s"])[:2] + ":" + str(item["dutyTime3s"])[2:]
    wednesdayEnd = '' if "dutyTime3c" not in item.keys() else str(item["dutyTime3c"])[:2] + ":" + str(item["dutyTime3c"])[2:]
    thursdayStart = '' if "dutyTime4s" not in item.keys() else str(item["dutyTime4s"])[:2] + ":" + str(item["dutyTime4s"])[2:]
    thursdayEnd = '' if "dutyTime4c" not in item.keys() else str(item["dutyTime4c"])[:2] + ":" + str(item["dutyTime4c"])[2:]
    fridayStart = '' if "dutyTime5s" not in item.keys() else str(item["dutyTime5s"])[:2] + ":" + str(item["dutyTime5s"])[2:]
    fridayEnd = '' if "dutyTime5c" not in item.keys() else str(item["dutyTime5c"])[:2] + ":" + str(item["dutyTime5c"])[2:]
    saturdayStart = '' if "dutyTime6s" not in item.keys() else str(item["dutyTime6s"])[:2] + ":" + str(item["dutyTime6s"])[2:]
    saturdayEnd = '' if "dutyTime6c" not in item.keys() else str(item["dutyTime6c"])[:2] + ":" + str(item["dutyTime6c"])[2:]
    sundayStart = '' if "dutyTime7s" not in item.keys() else str(item["dutyTime7s"])[:2] + ":" + str(item["dutyTime7s"])[2:]
    sundayEnd = '' if "dutyTime7c" not in item.keys() else str(item["dutyTime7c"])[:2] + ":" + str(item["dutyTime7c"])[2:]
    holidayStart = '' if "dutyTime8s" not in item.keys() else str(item["dutyTime8s"])[:2] + ":" + str(item["dutyTime8s"])[2:]
    holidayEnd = '' if "dutyTime8c" not in item.keys() else str(item["dutyTime8c"])[:2] + ":" + str(item["dutyTime8c"])[2:]
    addr = '' if "dutyAddr" not in item.keys() else item["dutyAddr"]
    emergency = '' if "MKioskTy25" not in item.keys() else item["MKioskTy25"]
    limbs = '' if "MKioskTy5" not in item.keys() else item["MKioskTy5"]
    pregnent = '' if "MKioskTy8" not in item.keys() else item["MKioskTy8"]
    newborn = '' if "MKioskTy10" not in item.keys() else item["MKioskTy10"]
    burn = '' if "MKioskTy11" not in item.keys() else item["MKioskTy11"]
    dialysis = '' if "MKioskTy7" not in item.keys() else item["MKioskTy7"]



    jsonResult.append({"hpid":hpid, "name":name, "div":div, "subject":subject, "tel":tel, "etel":etel, "addr":addr,
                           "lat":lat, "lon":lon, "info":info, "mondayStart":mondayStart, "mondayEnd":mondayEnd,
                           "tuesdayStart":tuesdayStart, "tuesdayEnd":tuesdayEnd, "wednesdayStart":wednesdayStart, "wednesdayEnd":wednesdayEnd,
                           "thursdayStart":thursdayStart, "thursdayEnd":thursdayEnd, "fridayStart":fridayStart, "fridayEnd":fridayEnd,
                           "saturdayStart":saturdayStart, "saturdayEnd":saturdayEnd, "sundayStart":sundayStart, "sundayEnd":sundayEnd,
                           "holidayStart":holidayStart, "holidayEnd":holidayEnd, "emergency":emergency, "limbs":limbs,
                           "pregnent":pregnent, "newborn":newborn, "burn":burn, "dialysis":dialysis
                           })

    # save_date_mysql(jsonResult)

    # return 1
    try:
        with open('medical_info_용산구.json', 'a', encoding='utf-8') as f:
            reJson = json.dumps(jsonResult, indent=4, ensure_ascii=False)
            f.write(reJson)
    except Exception as e :
        print(e)
        print("Fail to create json file_%s" % datetime.datetime.now())

    print("Success to create json file_%s" % datetime.datetime.now())

if __name__ == '__main__':
    f = open('medical_info_용산구.json', 'w', encoding='utf-8')
    f.close()

    for i in count(1):
        h_list = get_hospital_list('서울특별시', '용산구', i)
        if h_list == None:
            print("Break exit")
            break

        for hp in h_list:
            get_url_data(hp)



