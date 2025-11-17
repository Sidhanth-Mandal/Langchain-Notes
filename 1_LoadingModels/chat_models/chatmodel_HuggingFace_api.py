from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

#using HuggingFaceEndpoint() to connect to hugging face api (loading api key from .env)
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", # this is the name written above every model
    task="text-generation"
)

#using ChatHUggingFace to chat using the connected llm
model = ChatHuggingFace(llm=llm)

result = model.invoke("What is the capital of India")

print(result.content)