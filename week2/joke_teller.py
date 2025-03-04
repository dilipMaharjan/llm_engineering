from token import OP
from annotated_types import T
from dotenv import load_dotenv
from openai import OpenAI
import os

#load the environment variables
load_dotenv()

# get the key
api_key=os.getenv("OPEN_API_KEY")
openai=OpenAI(api_key=api_key)

messages=[
    {"role":"system", "content":"You are a helpful assistant who is here to tell jokes."},
    {"role":"user", "content":"Tell me 20 lined religious Christian joke"}
]

response=openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.7,
    stream=True
)

# print(response.choices[0].message.content)

# Handle streaming response
buffer=[]
streamMessage=''
for chunk in response:
    content=chunk.choices[0].delta.content
    if content:
        buffer.append(content)
    
complete_response=''.join(buffer)
print(complete_response)


    
   
