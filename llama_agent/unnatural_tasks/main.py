import os
import json
import random
import pandas as pd
from typing import List

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task_methods", default=None, type=str)
    parser.add_argument("--path_files", default="./data/raw_files/arxiv1/", type=str)
    parser.add_argument("--path_unnatural", default="./data/unnatural/", type=str)
    parser.add_argument("-l", "--limit", type=int, default=150000)
    args = parser.parse_args()

    print(f"Starting process - {args.template_name}")
    tasker = UnnaturalTasker(
        path_files=args.path_files,
        path_unnatural=args.path_unnatural,
        task_method_name=args.task_methods
    )

    print("Defining the tasks to do.")
    tasker.define_new_possible_tasks()

    print("Postprocessing unnatural generations.")
    tasker.post_process_generations()

    print("Finished - closing scripts.")

if __name__ == "__main__":

    main()
