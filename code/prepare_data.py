import os
import json
import argparse
from glob import glob

def modify_data(json_file):
    """ 전체 wikipedia_XXXX.json 파일의 data 내용 수정하는 함수.

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
        {'file_name': 
        'sentence':
        }
    """
    pass

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

    total_data = combine_json_data(file_list)
            
    for data in total_data:
        write_data("triple_data.txt", data)
    
