from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model = 'text-embedding-3-large' , dimension = 32)

result = embedding.embed_query("Jasprit Bumrah is the best Indian Cricketer")

documents = [
    "Jasprit Bumrah is the best Indian Cricketer",
    "Travis head is a Nightmare for India",
    "Trent Bolt was a lengendary Bowler"
]

result2 = embedding.embed_documents(documents)

print(str(result))
print('-'*20)
print(str(result2))