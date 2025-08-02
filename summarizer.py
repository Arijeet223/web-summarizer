import os 
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import openai

# laod enviormental variables

load_dotenv(override=True)
api_key=os.getenv('OPENAI_API_KEY')

if not api_key:
    print("no keys were found")
elif not api_key.startswith("sk-proj-"):
    print("API key were found but they are different")
elif api_key.strip() != api_key:
    print("API key migght have some space or whitespaces left in them")
else:
    print("API keys were found in good condition")

class Website:

    #to represent class as website
    def __init__(self,url):
        "create website object from url using beatiful soup"
        self.url =url
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')
        self.title=soup.title.string if soup.title else ("no title found")
        for irrelevent in soup.body(["script","img","input","style"]):
            irrelevent.decompose()
        self.text =soup.body.get_text(separator="\n",strip =True)

sample =Website("https://cnn.com")
# print(sample.title)
# print(sample.text)

# Openai Prompts

#System Prompt tells what task they are performing and what tone should be used
#User - Sends conversation for response
#Assistant - chatbot

#system prompt

system_prompt ="You are an assistant who analyzes the content of a website and provides a short summary, ignoring some text\
that might be navigation related. Respond in Markdown."

#user

def user_prompt_web(website):
    user_prompt = f"You are looking a website titled {website.title}. The conten of this website is as follows: \
                  Provide a shot summary of the website in markdown."
    user_prompt += website.text

    return user_prompt

#message

def message_web(website):
    return [
        {'role':"system",'content':system_prompt},
        {'role':'user','content': user_prompt_web(website)}
    ]

message_web(sample)

#calling openai

def summarize(url):
    website = Website(url)
    response =openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_web(website)
    )
    return response.choices[0].message.content

summarize("https://cnn.com")

#presentation using markdown

def show_summary(url):
    summary = summarize(url)
    print(summary)


show_summary("https://instagram.com")
