import os
import json
from typing import Optional
import numpy as np
import torch
from torch.utils.data import Dataset

from utils import EntityPosMarker, get_data_from_txt

class REDataset(Dataset):
    """ Dataloader for KBN data.
    """
    def __init__(self, path, mode, args):
        super().__init__()

        self.args = args

        data = get_data_from_txt(os.path.join(path, mode))
        total_data = len(data)

        marker = EntityPosMarker()
        
        # load rel2id
        if os.path.exists(os.path.join(path, "rel2id.json")):
            with open(os.path.join(path, "rel2id.json")) as f:
                rel2id = json.load(f)
        else:
            raise Exception("Error: There is no 'rel2id.json'!!")
        
        # preprocessing data
        self.tokenized_input_ids = np.zeros((total_data, args.max_length), dtype=int)
        self.mask = np.zeros((total_data, args.max_length), dtype=int)
        self.subj_marker_start = np.zeros(total_data, dtype=int)
        self.subj_marker_end = np.zeros(total_data, dtype=int)
        self.obj_marker_start = np.zeros(total_data, dtype=int)
        self.obj_marker_end = np.zeros(total_data, dtype=int)
        self.label = np.zeros(total_data, dtype=int)

        for i, item in enumerate(data):
            self.label[i] = rel2id[item['description']]  # description = 한국어 relation

            sentence = item['sentence']
            subj_pos_range = item['subj']['pos']
            obj_pos_range = item['obj']['pos']

            tokenized_input_ids, subj_marker_start, subj_marker_end, obj_marker_start, obj_marker_end = marker.tokenize(sentence=sentence, subj_pos_range = subj_pos_range, obj_pos_range=obj_pos_range)

            length = min(len(tokenized_input_ids), args.max_length)
            self.tokenized_input_ids[i][0:length] = tokenized_input_ids[0:length]
            self.mask[i][0:length] = 1
            self.subj_marker_start[i] = min(subj_marker_start, args.max_length - 1)
            self.subj_marker_end[i] = min(subj_marker_end, args.max_length - 1)
            self.obj_marker_start[i] = min(obj_marker_start, args.max_length - 1)
            self.obj_marker_end[i] = min(obj_marker_end, args.max_length - 1)

    def __len__(self):
        return len(self.tokenized_input_ids)

    def __getitem__(self, idx):
        tokenized_input_ids = self.tokenized_input_ids[idx]
        mask = self.mask[idx]
        subj_marker_start = self.subj_marker_start[idx]
        subj_marker_end = self.subj_marker_end[idx]
        obj_marker_start = self.obj_marker_start[idx]
        obj_marker_end = self.obj_marker_end[idx]
        label = self.label[idx]

        return tokenized_input_ids, mask, subj_marker_start, subj_marker_end, obj_marker_start, obj_marker_end, label