import os
import json
import re
import random
from collections import defaultdict

from transformers import BertTokenizer

# 문장 하나에 대해 processing하는 함수 클래스
class EntityPosMarker:
    """ 한국어 문장 하나에 대해 entity의 위치를 special token으로 나타낸 후,
        tokenize하여 BERT에 들어갈 수 있는 input ids 형태로 변환.
    
    Attributes:
        tokenizer: BertTokenizer(bert-base-multilingual-cased model을 사용).
        args: Args from command line.
    """
    def __init__(self, args=None):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.err = 0
        self.args = args
    
    def tokenize(self, sentence, subj_pos_range, obj_pos_range):
        """ Entity Marker를 special token 형태로 추가한 후 BERT-input ids로 변환하는 함수.

        Args:
            sentence: 한국어 문장 (type: str)
            subject_pos_range: subject entity의 위치 인덱스 범위 (인덱스는 문자열 인덱스)
            object_pos_range: object entity의 위치 인덱스 범위 (인덱스는 문자열 인덱스)

        Returns:
            tokenized_input_ids: BERT-input ids
            subj_marker_start: subject entity marker 시작 위치 인덱스
            subj_marker_end: subject entity marker 끝 위치 인덱스
            obj_marker_start: object entity marker 시작 위치 인덱스
            obj_marker_end: object entity marker 끝 위치 인덱스

        Example:
            sentence: "한국은 동아시아의 한반도에 위치하고 있다."
            subj_pos_range: [0, 2] ("한국")
            obj_pos_range: [4, 8] ("동아시아")

            1. tokenizer.tokenize(sentence)
                tokens = ['한국', '##은', '동', '##아', '##시아', '##의', '한', '##반', '##도에', '위', '##치', '##하고', '있다', '.']
            2. special token 추가
                tokenized_sentence = ['[CLS]', '[unused1]', '한국', '[unused2]', '##은', '[unused3]', '동', '##아', '##시아', 
                                    '[unused4]', '##의', '한', '##반', '##도에', '위', '##치', '##하고', '있다', '.', '[SEP]']
            3. tokenized sentence를 BERT-input ids로 변환 및 entities 위치 찾아 return
                tokenized_input_ids = [101, 1, 48556, 2, 10892, 3, 9095, 16985, 46861, 4, 10459, 9954, 30134, 108521,
                                    9619, 18622, 12453, 11506, 119, 102]
        """
        # subj_name, obj_name
        subj_name = sentence[subj_pos_range[0]:subj_pos_range[1]]
        obj_name = sentence[obj_pos_range[0]:obj_pos_range[1]]

        subj_start_idx, subj_end_idx = [], []
        obj_start_idx, obj_end_idx = [], []

        # 1. tokenizer.tokenize(sentence)
        tokens = self.tokenizer.tokenize(sentence)

        # subj, obj token 위치 찾기
        for i, token in enumerate(tokens):
            if token[0] == subj_name[0]:
                subj_start_idx.append(i)
            if token[-1] == subj_name[-1]:
                subj_end_idx.append(i)
        
            if token[0] == obj_name[0]:
                obj_start_idx.append(i)
            if token[-1] == obj_name[-1]:
                obj_end_idx.append(i)
        
        # subj token idx
        subj_flag = False
        for i in subj_start_idx:
            for j in subj_end_idx:
                # tmp_tokens = ['한국']
                tmp_tokens = tokens[i:j+1]
                subj_cand = " ".join(tmp_tokens)
                subj_cand = re.sub(" ##", "", subj_cand)
                if subj_cand == subj_name:
                    subj_token_start, subj_token_end = i, j+1
                    subj_flag = True
                    break
            if subj_flag:
                break

        # obj token idx
        obj_flag = False
        for i in obj_start_idx:
            for j in obj_end_idx:
                # tmp_tokens = ['동', '##아', '##시아']
                tmp_tokens = tokens[i:j+1]
                obj_cand = " ".join(tmp_tokens)
                obj_cand = re.sub(" ##", "", obj_cand)
                if obj_cand == obj_name:
                    obj_token_start, obj_token_end = i, j+1
                    obj_flag = True
                    break
            if obj_flag:
                break

        # subj_tokens = tokens[subj_token_start:subj_token_end]
        # obj_tokens = tokens[obj_token_start:obj_token_end]

        # 2. special token 추가
        tokenized_sentence = []
        for i, token in enumerate(tokens):
            if i == subj_token_start:
                tokenized_sentence.append("[unused1]")
            elif i == obj_token_start:
                tokenized_sentence.append("[unused3]")

            if i == subj_token_end:
                tokenized_sentence.append("[unused2]")
            elif i == obj_token_end:
                tokenized_sentence.append("[unused4]")

            tokenized_sentence.append(token)

        tokenized_sentence = ["[CLS]"] + tokenized_sentence + ["[SEP]"]

        # 3. entity marker token 위치 찾기
        try:
            subj_marker_start = tokenized_sentence.index("[unused1]")
            subj_marker_end = tokenized_sentence.index("[unused2]")
        except:
            self.err += 1
            subj_marker_start = 0
            subj_marker_end = 2
        
        try:
            obj_marker_start = tokenized_sentence.index("[unused3]")
            obj_marker_end = tokenized_sentence.index("[unused4]")
        except:
            self.err += 1
            obj_marker_start = 0
            obj_marker_end = 2

        tokenized_input_ids = self.tokenizer.convert_tokens_to_ids(tokenized_sentence)

        return tokenized_input_ids, subj_marker_start, subj_marker_end, obj_marker_start, obj_marker_end

def sample_train_dataset(dataset_path, prop):
    data = []
    with open(os.path.join(dataset_path, "train.txt")) as f:
        lines = f.readlines()
        for line in lines:
            item = json.loads(line)
            data.append(item)
    
    reduced_data = []
    reduced_times = 1 / prop
    
    rel2item = defaultdict(list)
    for item in data:
        rel2item[item["description"]].append(item)
    
    for rel_key in rel2item:
        item_list = rel2item[rel_key]
        random.shuffle(item_list)
        number = int(len(item_list) // reduced_times) if len(item_list) % reduced_times == 0 else int(len(item_list) // reduced_times) + 1
        reduced_data.extend(item_list[:number])
    print(f"The number of data in {dataset_path}/train_{str(prop)}.txt: {len(reduced_data)}")

    with open(os.path.join(dataset_path, "train_" + str(prop) + ".txt"), 'w') as f:
        for item in reduced_data:
            dump = json.dumps(item, ensure_ascii=False)
            f.write(dump + '\n')
    print(f"*********** {dataset_path}/train_{str(prop)}.txt prepared!! ***********")
    
if __name__ == "__main__":
    data_dir = "../data"
    sample_train_dataset(dataset_path=data_dir, prop=0.1)
    sample_train_dataset(dataset_path=data_dir, prop=0.01)
