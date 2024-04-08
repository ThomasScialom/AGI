from numpy import random
from abc import ABC, abstractmethod

TEXT = """When writing and talking, people sometimes pause to think. Although reasoning-focused works have often framed reasoning as a method of answering questions or completing agentic tasks, reasoning is implicit in almost all written text. For example, this applies to the steps not stated between the lines of a proof or to the theory of mind underlying a conversation. In the Self-Taught Reasoner (STaR, Zelikman et al. 2022), useful thinking is learned by inferring rationales from few-shot examples in question-answering and learning from those that lead to a correct answer. This is a highly constrained setting – ideally, a language model could instead learn to infer unstated rationales in arbitrary text. We present Quiet-STaR, a generalization of STaR in which LMs learn to generate rationales at each token to explain future text, improving their predictions. We address key challenges, including 1) the computational cost of generating continuations, 2) the fact that the LM does not initially know how to generate or use internal thoughts, and 3) the need to predict beyond individual next tokens. To resolve these, we propose a tokenwise parallel sampling algorithm, using learnable tokens indicating a thought’s start and end, and an extended teacher-forcing technique. Encouragingly, generated rationales disproportionately help model difficult-to-predict tokens and improve the LM’s ability to directly answer difficult questions. In particular, after continued pretraining of an LM on a corpus of internet text with Quiet-STaR, we find zero-shot improvements on GSM8K (5.9%→10.9%) and CommonsenseQA (36.3%→47.2%) and observe a perplexity improvement of difficult tokens in natural text. Crucially, these improvements require no fine-tuning on these tasks. Quiet-STaR marks a step towards LMs that can learn to reason in a more general and scalable way"""

GENERATION = """Question: What is the name of the model that learns to generate rationales at each token to explain future text, improving their predictions?

Answer: Quiet-STaR"""

class Folder():
    """
    Represents a folder with a name, containing sub-folders and files.

    Attributes:
        name (str): The name of the folder.
        depth (int): The depth in the tree structure (root=0).
        parent (Folder): The parent Folder.
        sub_folders (list): A list of Folder instances representing the sub-folders contained within this folder.
        files (list): A list of files contained within this folder.
    """
    def __init__(self, name: str, parent: "Folder"):
        self.name = name
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 0 # root = 0

        self.sub_folders = []
        self.files = []

    def __str__(self):
        return self.name + " (depth: {depth}, sub_folders: {sub_folders}, files: {files})".format(
            depth=self.depth, sub_folders=len(self.sub_folders), files=len(self.files))


class File():
    """
    Represents a file with a name, a name, a folder it is located, a type, a pointer to the actual temp path

    Attributes:
        name (str): The name of the file.
        folder(Folder): The folder it is located in.
    """
    def __init__(self, name: str, folder: Folder):
        self.name = name
        self.folder = Folder

class Environement():

    def __init__(self, graph_method="random_1", file_method="default", folder_method="default"):

        self.root_folder = Folder(name="/home/", parent=None)
        self.init_methods(graph_method, file_method, folder_method)
        self.populate(self.root_folder)

    def init_methods(self, graph_method, file_method, folder_method):
        self.graph_method = graph_method
        if graph_method == "random_1":
            self.max_depth = 3
            self.max_breath_folders = 2
            self.max_breath_files = 3

        self.file_method = file_method
        if file_method == "default":
            self.get_nb_files = lambda:  random.choice(range(1, self.max_breath_files))
            self.get_file_names = lambda n: ["file_{i}".format(i=i) for i in range(n)]

        self.folder_method = folder_method
        if folder_method == "default":
            self.get_nb_folders = lambda: random.choice(range(1, self.max_breath_folders))
            self.get_folder_names = lambda n: ["folder_{i}".format(i=i) for i in range(n)]


    def populate(self, folder: Folder):
        if folder.depth >= self.max_depth:
            return
        self.set_new_files(folder)
        self.set_new_folders(folder)

    def set_new_folders(self, parent_folder):
        for folder_name in self.get_folder_names(self.get_nb_folders()):
            new_sub_folder = Folder(name=folder_name, parent=parent_folder)
            self.populate(new_sub_folder)
            parent_folder.sub_folders.append(new_sub_folder)

    def set_new_files(self, parent_folder):
         for new_file in self.get_file_names(self.get_nb_files()):
            parent_folder.files.append(File(name=new_file, folder=parent_folder))

    def visualise_folders(self, node=None):
        tab_offset = lambda depth: "|" + 2*depth*"_" if depth else ""
        if not node:
            node = self.root_folder
        print(tab_offset(node.depth) + str(node))

        for doc in node.files:
            print(tab_offset(node.depth+1) + doc.name)

        for sub_folder in node.sub_folders:
            self.visualise_folders(sub_folder)

env = Environement()
env.visualise_folders()
