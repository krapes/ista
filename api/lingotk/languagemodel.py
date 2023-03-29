from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader, GCSDirectoryLoader, GCSFileLoader
import os
import logging
import time


logging.basicConfig(level=logging.INFO)

#SOURCE_DOCS_DIRECTORY = "../data/dev_data"
#FAKE_MODEL_RESPONSES = {"How do I pay an exempt employee?":  "An exempt employee should be paid a predetermined salary regardless of the amount of hours they work. If an exempt employee is not paid the full salary in a given week, the employer may deduct the amount of hours not worked from the employee's salary. The employer cannot dock the employee's wages for partial day absences"}

class LanguageModel:

    def __init__(self, document_directory=None, document_bucket='subjectguru'):
        logging.info("Initializing LanguageModel")
        self.model = None
        self.source_docs_directory = document_directory
        self.document_bucket = document_bucket
        self.setup()

    def load_files_local(self: str) -> DirectoryLoader:
        logging.info("Loading Docs...")
        loader = DirectoryLoader(self.source_document_directory, glob="**/*.txt")
        source_docs = loader.load()
        logging.info(f"Found {len(source_docs)} in directory {self.source_document_directory}")
        return source_docs

    def load_files_gcs(self):
        logging.info(f"Loading Docs from {self.source_docs_directory}...{os.environ['PROJECT_ID']}")
        loader = GCSDirectoryLoader(project_name=os.environ['PROJECT_ID'],
                                    bucket=self.document_bucket,
                                    prefix=self.source_docs_directory)
        source_docs = loader.load()
        logging.info(f"Found {len(source_docs)} in directory {self.source_docs_directory}")
        return source_docs

    def build_embeddings(self, source_docs: DirectoryLoader) -> Chroma:
        char_text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        doc_texts = char_text_splitter.split_documents(source_docs)
        openai_embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        vStore = Chroma.from_documents(doc_texts, openai_embeddings)
        return vStore

    def train_model(self, vStore: Chroma) -> VectorDBQA:
        logging.info("Training model")
        model = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vStore)
        return model

    def setup(self):
        if self.model is None:
            source_docs = self.load_files_gcs()
            vStore = self.build_embeddings(source_docs)
            self.model = self.train_model(vStore)
        return self.model

    def trial_question(self, question: str) -> dict[str, str]:
        for i in range(0, 35, 1):
            logging.info(f"sleeping {i}")
            time.sleep(1)
        response = {"query": question, "response": question}
        return response

    def ask_question(self, question: str) -> dict[str, str]:
        if self.model is None:
            self.model = self.setup()
        response = self.model({"query": question})
        return {"query": response['query'], "response": response['result']}

    def interactive_questions(self):
        question = input("Please enter your question (or type quit to exit): \n\n")
        while question != "quit":
            response = self.model({"query": question})
            print(f"{response['result']} \n\n")
            question = input("Please enter your question (or type quit to exit): \n\n")



'''
def loadfiles()-> DirectoryLoader:
    logging.info("Loading Docs...")
    loader = DirectoryLoader(source_docs_directory, glob="**/*.txt")
    source_docs = loader.load()
    logging.info(f"Found {len(source_docs)} in directory {source_docs_directory}")
    return source_docs

def build_embeddings(source_docs: DirectoryLoader) -> Chroma:
    char_text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    doc_texts = char_text_splitter.split_documents(source_docs)
    openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vStore = Chroma.from_documents(doc_texts, openAI_embeddings)
    return vStore

def train_model(vStore: Chroma)->VectorDBQA:
    logging.info("Training model")
    model = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vStore)
    return model


def setup():
    global model
    if model is None:
        source_docs = loadfiles()
        vStore = build_embeddings(source_docs)
        model = train_model(vStore)
    return model

def trial_question(question):
    """
    model = setup()
    question = "How do I pay and exempt employee?"
    response = model({"query": question})
    response = {"query": response['query'], "response": response['result']}
    """
    for i in range(0, 1, 1):
        print(f"sleeping {i}")
        time.sleep(1)
    response = {"query": question, "response": fake_model_responses.get(question, question)}
    return response

def ask_question(question):
    global model
    if model is None:
        model = setup()
    response = model({"query": question})
    return {"query": response['query'], "response": response['result']}
def interactive_questions():
    question = input("Please enter your question (or type quit to exit): \n\n")
    while question != "quit":
        response = model({"query": question})
        print(f"{response['result']} \n\n")
        question = input("Please enter your question (or type quit to exit): \n\n")


#print(trial_question('this is my question'))

'''