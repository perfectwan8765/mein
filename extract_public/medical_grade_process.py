import json

def read_json_file(file_name):
    jData = open(file_name, 'r', encoding='utf-8').read()
    jData = json.loads(jData)

    for item in jData:
        print(item)

def update_json_file(file_name):
    jData = open(file_name, 'r', encoding='utf-8').read()
    jData = json.loads(json.dumps(jData))

    # jData = jData.replace("][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]", "]")
    # # jData = jData.replace("][][][][][][][][][][][][][][][][][", ",")
    # # jData = jData.replace("][][][][", ",")
    jData = jData.replace("][", ",")
    print(jData)
    f = open('medical_new_grade_info_110018.json', 'w', encoding='utf-8')
    f.write(jData)
    f.close()

def check_json_file(file_name1, file_name2):
    jData = open(file_name1, 'r', encoding='utf-8').read()
    jData = json.loads(jData)
    jData2 = open(file_name2, 'r', encoding='utf-8').read()
    jData2 = json.loads(jData2)
    jsonResult = []
    for item in jData:
        for item2 in jData2:
            if item['name'] == item2['name'] :
                print(item['name'], item2['name'])
                if item["highblood"] == "": item['highblood'] = 0
                if item["lungCa"] == "": item['lungCa'] = 0
                if item["stomachCa"] == "": item['stomachCa'] = 0
                if item["liverCa"] == "": item['liverCa'] = 0
                if item["bowelCa"] == "": item['bowelCa'] = 0
                if item["breastCa"] == "": item['breastCa'] = 0
                if item["cesarean"] == "": item['cesarean'] = 0
                if item["antibiotics"] == "": item['antibiotics'] = 0
                if item["injection"] == "": item['injection'] = 0
                if item["diabetes"] == "": item['diabetes'] = 0
                if item["asthma"] == "": item['asthma'] = 0
                if item["dialysis"] == "": item['dialysis'] = 0
                if item['highblood'] == '양호':
                    item['highblood'] = 3
                if item['asthma'] == '양호':
                    item['asthma'] = 3
                if item['diabetes'] == '양호':
                    item['diabetes'] = 3
                item['hpid'] = item2['hpid']
                jsonResult.append(item)

    with open('medical_grade_서초구.json', 'w', encoding='utf-8') as f:
        reJson = json.dumps(jsonResult, indent=4, ensure_ascii=False)
        f.write(reJson)


if __name__ == '__main__' :
    print('start')
    # read_json_file('medical_new_grade_info_110018.json')
    # update_json_file('medical_grade_info_110018.json')
    # check_json_file('medical_new_grade_info_110021.json', 'medical_new_info_서초구.json')