from utils import get_exs, save_exs

class Task():
    @abstractmethod
    def __init__(self, name_method: str):
        pass

    def get_all_possible_tasks(self, path_files: str):
        pass

    def create_unnatural_batches(self, file_paths):
        pass

    def post_process_generations(self):
        pass

    def make_jsonl(self, unnatural_prompt, list_file_path, list_text_chunk, key_additional=""):
        return {
            'name_method': self.name_method, # the task method name
            'meta': {
                'unnatural_prompt': unnatural_prompt, # the unnatural prompt used to create the unnatural question
                'list_file_path': list_file_path, # list of file paths used to create the unnatural question
                'list_text_chunk': list_text_chunk, # list of text chunks that belong to the files used to create the unnatural question
                'postprocessed': False, # whether the generation has been postprocessed or not, only after the genaration is done
                'key': "_".join(key_additional + list_file_path) # the key used to identify the task
            },
            'unnatural':{
                'generation': None, # the unnatural generation which is init to None
                'question': None, # the unnatural question after postprocessing
                'answer': None, # the unnatural answer after postprocessing
                'additional_info': {}  #  any additional info during postprocessing
            }
        }

class UnnaturalTasker():
    def __init__(self, path_files: str, path_unnatural: str, task_method_name: str):
        self.path_files = path_files
        self.path_unnatural = os.join(path_unnatural, task_method_name, 'jsonl')
        self.task_method_name = task_method
        if task_method_name == "TaskFactualQuestion":
            self.task_method = TaskFactualQuestion()
        else:
            raise NotImplementedError

    def define_new_possible_tasks(self):
        all_possible_tasks = self.task_method.get_all_possible_tasks(self.path_files)
        done_tasks = {ex['meta']['key'] for ex in get_exs(self.path_unnatural)}
        new_tasks = [ex for ex in all_possible_tasks if ex['meta']['key'] not in done_tasks]

    def post_process_generations(self):
        existing_tasks = get_exs(self.path_unnatural)
        for ex in existing_tasks:
            if ex['meta']['postprocessed'] is False:
                self.task_method.post_process_generation(ex)
                assert ex['meta']['postprocessed'] is True
        save_exs(existing_tasks, self.path_unnatural)
