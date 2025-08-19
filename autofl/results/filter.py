import json
import os
import pandas as pd

df = pd.read_csv("../data/bugsinpy_bug_validity.csv")
for run_dir in os.listdir("."):
    if not run_dir.startswith("bip"):
        continue
    for model in os.listdir(run_dir):
        model_path = f"{run_dir}/{model}"
        print(f"{model_path} is now processed...")
        for log_file in os.listdir(model_path):
            project = log_file[4:-5]
            if df[df["bug"]==project]["validity"].iloc[0] != "ok":
                continue
            with open(f"{model_path}/{log_file}") as f:
                data = json.load(f)
            buggy_methods = data['buggy_methods']
            if type(buggy_methods) == str and buggy_methods.startswith('Traceback'):
                os.remove(f"{model_path}/{log_file}")
                print(f"{model_path}/{log_file} is removed")
