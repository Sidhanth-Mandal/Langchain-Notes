from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sys
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

model = ChatGroq(model ='openai/gpt-oss-120b')

prompt1 = PromptTemplate(
    template = 'Generate A detailed report on {topic}',
    input_variables= ['topic']   
)

prompt2 = PromptTemplate(
    template= 'Generate a 3 pointer summary from the following text \n {text}',
    input_variables= ['text']
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic' : 'F1 Racing'})

print(result)