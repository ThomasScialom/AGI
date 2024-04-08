import os
import json
import random
import pandas as pd

def get_exs(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [json.loads(l) for l in lines]
    return lines
