import os
import json
import numpy as np
import torch
from torch.utils.data import Dataset

from utils import EntityPosMarker, get_data_from_txt

class REDataset(Dataset):
    def __init__(self, path, args):
        super().__init__()

        data = get_data_from_txt(path)