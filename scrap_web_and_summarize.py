from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
import requests
from IPython.display import display, Markdown

"""
    create a .env file in the root directory of the project and add the following line
    OPENAI_API_KEY="your_api_key"
"""

#load env variables
load_dotenv()

#get key
api_key=os.getenv("OPEN_API_KEY")

if not api_key:
    raise ValueError("API key not found")
elif api_key.strip() != api_key:
    raise ValueError("API key is invalid")
else:
    print("API key is found and valid")
    
openai=OpenAI(api_key=api_key)

class Website:
    url:str
    title:str
    text:str
    
    def __init__(self, url):
        self.url = url
        response=requests.get(url)
        soup=BeautifulSoup(response.text, 'html.parser')
        self.title=soup.title.string if soup.title else 'No title found.'
        for irrelevant in soup.body(['script', 'style']):
            irrelevant.decompose()
        self.text=soup.body.get_text(separator='\n',strip=True)

scrapped_website=Website("https://dilipmaharjan.com/")
# print(scrapped_website.title)
# print(scrapped_website.text)

#System prompt 
system_prompt="""
    You are an assistant that analyzes the content of a website and provides a short summary,
    ignoring text that might be navigation related. Respond in markdown format.
"""

def user_prompt_for(website):
    user_prompt=f"""
        You are  looking at the website titled {website.title}.
    """
    user_prompt+="""
    The contens of this website are as follows;
    please provide a short summary of this website in  markdown format. If it includes news or announcements, please include that as well.
    """
    user_prompt+=website.text
    return user_prompt
    
# print(system_prompt)
# print(user_prompt_for(scrapped_website))

def messages_for(website):
    return [
        {"role":"system", "content":system_prompt},
        {"role":"user", "content":user_prompt_for(website)}
    ]
        
# print(messages_for(scrapped_website))
        
def summarize(url):
    website=Website(url)
    response=openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website),
        )
    return response.choices[0].message.content
print(summarize("https://dilipmaharjan.com/"))
def display_summary(url):
    summary=summarize(url)
    display(Markdown(summary))
    
display_summary("https://dilipmaharjan.com/")
