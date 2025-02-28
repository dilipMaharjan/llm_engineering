import requests
from bs4 import BeautifulSoup
from IPython.display import display, Markdown
import ollama
OLLAMA_API="http://localhost:11434/api/chat"
HEADERS={"Content-Type":"application/json"}
MODEL="llama3.2"

messages=[
    {"role":"user", "content":"Describe business application of Generative AI."},
]
#Calling ollama API directly
# payload={
#     "model":MODEL,
#     "messages":messages,
#     "stream":False
# }

# response=requests.post(OLLAMA_API, headers=HEADERS, json=payload)
# response=response.json()
# print(response['message']['content'])

#Using ollama package
 
# response=ollama.chat(messages=messages, model=MODEL, stream=False)
# print(response['message']['content'])

#scrap given website
title="No title found."
text="No text found."


def scrap_web(url):
    global title,text
    response=requests.get(url)
    soup=BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title found.'
    for irrelevant in soup.body(['script', 'style']):
            irrelevant.decompose()
    text=soup.body.get_text(separator='\n',strip=True)
    return response

response=scrap_web("https://dilipmaharjan.com").content

messages=[
    {"role":"system", "content":f"You are an assistant that analyzes the content of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown format."},
    {"role":"user", "content":f"You are  looking at the website titled {title}. The contens of this website are as follows; {text} please provide a short summary in 5 lines of this website in  markdown format. If it includes news or announcements, please include that as well.\n{text}"}
]
response=ollama.chat(messages=messages, model=MODEL, stream=False)
# print(response['message']['content'])
summary=response['message']['content']
print(summary)
display(Markdown(summary))
