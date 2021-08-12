import os
import json
import argparse
from glob import glob

def modify_data(input_filepath):
    """ 전체 wikipedia_XXXX.json 파일의 data를 parsing한 후
        형태를 바꾸어 새로운 json 파일을 생성하는 함수.

    Original data example:
        {'file_name': '/data/taesunwhang/entity_relation/wikipedia/entity/wikipedia_0001.json',
        'sentence': '제임스 얼 "지미"카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.',
        'subject': '제임스 얼',
        'subject_tag': 'PS',
        'subject_pos': [0, 5],
        'object': '카터 주니어',
        'object_tag': 'PS',
        'object_pos': [10, 16],
        'relation': 'successor',
        'description': '항목 주제의 후임자',
        'confidence': 0.8254553079605103}

    Modified data example:
        {'file_name': '/data/modified_KBN_data/wikipedia_0001.json',
        'sentence': '제임스 얼 "지미"카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.',
        'subj': {'name': '제임스 얼',
                'pos': [0, 5],
                'type': 'PS'},
        'obj': {'name': '카터 주니어',
                'pos': [10, 16],
                'type': 'PS'},
        'relation': 'successor',
        'description': '항목 주제의 후임자',
        'confidence': 0.8254553079605103}
    """
    modified_data = []
    # filename = "wikipedia_XXXX.json"
    filename = input_filepath[-19:]

    # original data parsing + modify data
    with open(input_filepath, 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            tmp_dict = dict()

            tmp_dict["file_name"] = "/data/modified_KBN_data/" + data["file_name"][-19:] # ../data/modified_KBN_data/wikipedia_XXXX.json
    
            tmp_dict["sentence"] = data["sentence"] 
            
            tmp_dict["subj"] = dict()
            tmp_dict["subj"]["name"] = data["subject"]
            tmp_dict["subj"]["pos"] = data["subject_pos"]
            tmp_dict["subj"]["type"] = data["subject_tag"]
            
            tmp_dict["obj"] = dict()
            tmp_dict["obj"]["name"] = data["object"]
            tmp_dict["obj"]["pos"] = data["object_pos"]
            tmp_dict["obj"]["type"] = data["object_tag"]

            tmp_dict["description"] = data["description"]
            tmp_dict["confidence"] = data["confidence"]
            
            modified_data.append(tmp_dict)
    
    # modified data to json file
    with open(os.path.join("../data/modified_KBN_data", filename), 'w') as f:
        json.dump(modified_data, f, ensure_ascii=False, indent=4)

def combine_json_data(file_list):
    """ file_list에 존재하는 전체 wikipedia_XXXX.json 파일을
        하나의 리스트에 저장하고 리스트를 return하는 함수.
    """
    data = []
    for json_file in file_list:
        with open(json_file) as f:
            json_data = json.load(f)
            data.append(json_data)
    return data

def write_data(output_filename, data):
    """ data 안의 dict 형태로 담겨 있는 triple 정보를
        하나의 텍스트 파일로 저장하는 함수.    
    """
    with open(output_filename, 'a') as f:
        for item in data:
            dump = json.dumps(item, ensure_ascii=False)
            f.write(dump)
            f.write('\n')


    
if __name__ == "__main__":
    file_list = glob('../data/KBN_data/*')
    file_list.sort()

    if not os.path.exists("../data/modified_KBN_data"):
        os.mkdir("../data/modified_KBN_data")

    # 각 json file 형태 변형하여 새로운 json 파일 생성
    for json_file in file_list:
        modify_data(input_filepath=json_file)

    modified_file_list = glob("../data/modified_KBN_data/*")
    modified_file_list.sort()
    
    total_data = combine_json_data(modified_file_list)
            
    for data in total_data:
        write_data("./triple_data.txt", data)