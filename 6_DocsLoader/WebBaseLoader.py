from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding="utf-8")


load_dotenv()

model = ChatGroq(model = 'openai/gpt-oss-120b')

prompt = PromptTemplate(
    template= 'Answer the following question \n {question} from the following text - \n {text}',
    input_variables=['question','text']
)

parser = StrOutputParser()

url = 'https://www.reddit.com/r/Crysis/comments/xb4rjr/crysis_on_win_10_wont_run/'

loader = WebBaseLoader(url)

docs = loader.load()
print(docs)

chain = prompt | model | parser

print(chain.invoke({
   'question': 'Why my game is not loading',
   'text' : docs[0].page_content }))