import os
from glob import glob
import json
import argparse

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
        self.args = args
    
    def tokenize(self, sentence, subject_pos_range, object_pos_range):
        """ Tokenizer.

        Args:
            sentence: 한국어 문장 (type: str)
            subject_pos_range: subject entity의 위치 인덱스 범위 (인덱스는 문자열 인덱스)
            object_pos_range: object entity의 위치 인덱스 범위 (인덱스는 문자열 인덱스)

        Returns:
            tokenized_input_ids: BERT-input ids
            subj_pos: subject entity marker 시작 위치 인덱스
            obj_pos: object entity marker 시작 위치 인덱스

        Example:
            sentence: '제임스 얼 "지미"카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.'
            subject_pos_range: [0, 5] (제임스 얼)
            object_pos_range: [10, 16] (카터 주니어)

            1. special token 추가
                '[unused1] 제임스 얼 [unused2] "지미"[unused3] 카터 주니어 [unused4](, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.'
            2. 
        """
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", dest="filepath", type=str, help="filepath")
    
    args = parser.parse_args()

    files = glob('../data/KBN_data/*')
    files.sort()
