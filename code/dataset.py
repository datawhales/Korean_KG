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
    def __init__(self, path, args):
        super().__init__()

        self.args = args

        data = get_data_from_txt(path)
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
    
        