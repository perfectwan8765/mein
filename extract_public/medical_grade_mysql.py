import json
import pymysql

def get_json_file(file_name):
    jData = json.loads(open(file_name, 'r', encoding='utf-8').read())
    # print(jData)
    save_date_mysql(jData)

def save_date_mysql(jsonResult):
    conn = pymysql.connect(host='127.0.0.1', user='zerosw', password='123456', db='meindb')
    cursor = conn.cursor()

    sql = 'insert into infos_gradeinfo(hurl, highblood, lungCa, stomachCa,' \
           ' liverCa, bowelCa, breastCa, cesarean, antibiotics, injection, ' \
           'diabetes, asthma, dialysis, hpid_id)' \
           ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    for item in jsonResult:
        data = (item['hurl'], item['highblood'], item['lungCa'], item['stomachCa'], item['liverCa'], item['bowelCa'],
                item['breastCa'], item['cesarean'], item['antibiotics'], item['injection'], item['diabetes'], item['asthma'],
                item['dialysis'], item['hpid'])
        print('data:', data)

        cursor.execute(sql, data)

    conn.commit()
    cursor.close()
    conn.close()
    print("database save")

if __name__ == '__main__':
    print('start')
    # get_json_file('medical_grade_종로구.json')