class TaskFactualQuestion(Task):
    def __init__(self):
        self.name_method = 'TaskFactualQuestion'
        self.template = """# Task: Generate a factual question about the text bellow that could be answered only using this document.

# Template: no verbosity, follow this template:
    ```
    Question: <<the_question>>
    Answer: <<the_question>>
    ```
# Document
{text}"""

    def create_unnatural_batches(self, file_paths):

        examples = []
        for file_path in file_paths:
            text_chunks = self.file_path2chunks(file_path)
            for text_chunk in text_chunks:
                unnatural_prompt = self.create_unnatural_question(text_chunk)
                prompt_json = self.make_jsonl(unnatural_prompt, list_file_path, list_text_chunk)
        return examples

    def file_path2chunks(self, file_path):
        with open(file_path, 'r') as f:
            text = f.readlines()
        return text

    def create_unnatural_question(self, text):
        return self.template.format(text=text)

    def post_process_generation(self, example):
        generation = example['unnatural']['generation']
        question, answer = generation.split('\nAnswer:')

        example['unnatural']['question'] = question.strip("Question:").strip()
        example['unnatural']['answer'] = answer.strip()
        example['meta']['postprocessed'] = True
