import ollama
OLLAMA_API="http://localhost:11434/api/chat"
MODEL="llama3.2"

messages1=[
    {"role":"system","content":"You are expert assistant that can translate into Spanish."},
    {"role":"user","content":"Please translate 'My name is Dilip' into Spanish."}
]


response=ollama.chat(messages=messages1, model=MODEL, stream=False)
spanish=response['message']['content']
print(spanish)
messages2=[
    {"role":"system","content":"You are expert assistant that has ability  to translate into any language."},
    {"role":"user","content":f"Please translate {spanish} into Nepali and 5 other Neplai dialetc"}
]
# print(messages)
response_stream=ollama.chat(messages=messages2, model=MODEL, stream=False)
print(f"{response_stream['message']['content']}")


