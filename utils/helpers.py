import os
import sys
from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
import time

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logger = get_logger(__name__)

def label_encode(df,columns):
    le = LabelEncoder()
    label_mappings={}
    for col in columns:
        df[col] = le.fit_transform(df[col])
        label_mappings[col] = dict(zip(le.classes_,le.transform(le.classes_)))
    
    return df,label_mappings