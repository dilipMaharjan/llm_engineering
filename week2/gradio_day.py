import ollama
import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI


LAMMA_MODEL="llama3.2"
GPT_MODEL="gpt-4o-mini"


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

# def message_gpt(user_prompt):
#     messages=[
#         {"role":"system", "content":"You are a helpful assistant that responds in the markdown."}, 
#         {"role":"user", "content":user_prompt}]
#     completions=ollama.chat(messages=messages, model=MODEL, stream=False)
#     return completions['message']['content']

# def message_gpt_stream(user_prompt):
#     messages=[
#         {"role":"system", "content":"You are a helpful assistant that responds in the markdown."}, 
#         {"role":"user", "content":user_prompt}]
#     completions_stream=ollama.chat(messages=messages, model=MODEL, stream=True)
#     result=""
#     for completion in completions_stream:
#         result+=completion['message']['content'] or ""
#         yield result
   
def stream_gpt(user_prompt):
    messages=[
        {"role":"system", "content":"You are a helpful assistant that responds in the markdown."}, 
        {"role":"user", "content":user_prompt}]
    completions_stream=openai.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        stream=True
        )
    result=""
    for completion in completions_stream:
        result+=completion.choices[0].delta.content or ""
        yield result

def stream_llama(user_prompt):
    messages=[
        {"role":"system", "content":"You are a helpful assistant that responds in the markdown."}, 
        {"role":"user", "content":user_prompt}]
    completions_stream=ollama.chat(messages=messages, model=LAMMA_MODEL, stream=True)
    result=""
    for completion in completions_stream:
        result+=completion['message']['content'] or ""
        yield result

#Title based on model selection
def choose_model(prompt,model_name):
    if model_name=="GPT":
        response= stream_gpt(prompt)
    elif model_name=="LLAMA":
        response= stream_llama(prompt)
    else:
        raise ValueError("Invalid model name")
    for chunk in response:
        yield chunk
    
 
# response=message_gpt("What is the capital of Nepal?")
# print(response)

# view=gr.Interface(fn=message_gpt, inputs="text", outputs="text", allow_flagging="never")
# view.launch(share=True)

#modifying default view
# view=gr.Interface(fn=message_gpt, 
#                   inputs=[gr.Textbox(lines=6, label="What would you like to know ..")], 
#                   outputs=[gr.Markdown(label="Here's what I found ..")],
#                   title="Chat with OLLAMA",
#                   description="OLLAMA is a conversational AI model that can help you with your questions.",
#                   theme="huggingface",
#                   allow_flagging="never"
#                 )
# view.launch(share=True)

view=gr.Interface(fn=choose_model, 
                  inputs=[gr.Textbox(label="What would you like to know .."),gr.Dropdown(["GPT","LLAMA"],label="Choose a model")],
                  outputs=[gr.Markdown(label="Here's what I found ..")],
                  title="Stream Chat with me",
                  description="I am a conversational AI model that can help you with your questions.",
                  theme="huggingface",
                  allow_flagging="never"
                )
view.launch(share=True)
