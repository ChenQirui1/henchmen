from dotenv import load_dotenv
import datasets
import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from smolagents import HfApiModel, CodeAgent

from markdown_tool import MarkdownTool
from retriever import RetrieverTool

load_dotenv()

knowledge_base = datasets.load_dataset("m-ric/huggingface_doc", split="train")
knowledge_base = knowledge_base.filter(
    lambda row: row["source"].startswith("huggingface/transformers")
)

source_docs = [
    Document(page_content=doc["text"], metadata={"source": doc["source"].split("/")[1]})
    for doc in knowledge_base
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
    strip_whitespace=True,
    separators=["\n\n", "\n", ".", " ", ""],
)
docs_processed = text_splitter.split_documents(source_docs)


retriever_tool = RetrieverTool(docs_processed)

# model_id = "meta-llama/Llama-3.3-70B-Instruct"
# model_id = "facebook/opt-125m"

model_id = "mistralai/Mistral-7B-Instruct-v0.2"
agent = CodeAgent(
    tools=[
        retriever_tool,
        MarkdownTool(),
    ],
    model=HfApiModel(
        # model_id="PowerInfer/SmallThinker-3B-Preview",
        model_id=model_id,
        token=os.getenv("HF_TOKEN"),
        timeout=300,
    ),
    max_steps=4,
    verbosity_level=2,
)

message = "Send to knowledge base: Polar bears have black skin that absorbs UV light to keep them warm. Their white fur reflects light, making them blend in with their surroundings"

agent_output = agent.run(f"Update the knowledge base with this information, {message}")

print("Final output:")
print(agent_output)
