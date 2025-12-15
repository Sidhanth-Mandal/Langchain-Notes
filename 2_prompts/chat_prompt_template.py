from langchain_core.prompts import ChatMessagePromptTemplate


chat_template = ChatMessagePromptTemplate([
    ('system' , 'You are a helpful {doamain} expert') ,
    ('human' , 'Explain in simple terms , what is the {topic}')
])

prompt = chat_template.invoke({'domain': 'cricket' , 'topic' : 'yorker'})


print(prompt)