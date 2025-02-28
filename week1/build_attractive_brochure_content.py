import ollama
OLLAMA_API="http://localhost:11434/api/chat"
MODEL="llama3.2"

messages1=[
    {"role":"system","content":"You are expert assistant that provides treding content ideas"},
    {"role":"user","content":"Provide me list of 3 trending content ideas"}
]


response=ollama.chat(messages=messages1, model=MODEL, stream=False)
# print(response['message']['content'])
list = response['message']['content']
print(list)
messages2=[
    {"role":"system","content":"You are expert assistant that has ability to pick one treding idea from the provided list and generate instragram reel"},
    {"role":"user","content":f"Pick one trending content idea from this list {list}, be precise and to the point."}
]
# print(messages)
response=ollama.chat(messages=messages2, model=MODEL, stream=False)
print(f"Picked : {response['message']['content']}")
