import os
import json
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
    """ file_list에 존재하는 전체 wikipedia_XXXX.json 파일을 parsing하여
        모든 triple data를 하나의 리스트에 저장하고 리스트를 return하는 함수.
    """
    data = []
    for json_file in file_list:
        with open(json_file) as f:
            json_data = json.load(f)
            for sent in json_data:
                data.append(sent)
    return data

def write_rel2id(filename, data):
    """ 전체 data에 존재하는 relation을 숫자로 인코딩하여 json file로 저장하는 함수.
    """
    rel2id = dict()
    rel_idx = 0
    for item in data:
        if item["description"] not in rel2id:
            rel2id[item["description"]] = rel_idx
            rel_idx += 1

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(rel2id, f, ensure_ascii=False, indent=4)
    
def write_text_file(output_filename, data):
    """ data 안의 dict 형태로 담겨 있는 triple data를
        하나의 텍스트 파일로 저장하는 함수.
        Use to write train.txt, dev.txt, test.txt.
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

    # 변형된 전체 데이터 통합하여 하나의 리스트에 저장
    total_data = combine_json_data(modified_file_list)
    
    write_rel2id("../data/rel2id.json", total_data)

    # total_data_num = 전체 데이터 개수
    total_data_num = len(total_data)
    print(f"Total number of data: {len(total_data)}")
    print('*' * 30)
    # train, dev, test split
    train_data = total_data[:int(0.6 * total_data_num)]
    dev_data = total_data[int(0.6 * total_data_num):int(0.8 * total_data_num)]
    test_data = total_data[int(0.8 * total_data_num):]

    print(f"The number of train data: {len(train_data)}")
    print(f"The number of dev data: {len(dev_data)}")
    print(f"The number of test data: {len(test_data)}")
    print('*' * 30)

    for data in total_data:
        write_data("./triple_data.txt", data)
    
