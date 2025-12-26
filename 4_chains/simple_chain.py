from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sys
sys.stdout.reconfigure(encoding="utf-8")


load_dotenv()

model = ChatGroq(model ='openai/gpt-oss-120b')

prompt = PromptTemplate(
    template = 'Generate 5 interesting facts about {topic}' ,
    input_variables = ['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic' : 'cricket'})

print(result)