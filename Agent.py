import csv
from langchain_ollama import OllamaLLM
import re
path=r"C:\Users\aswin\Downloads\archive\Countries by continents.csv"
# we are gonna parse the csv data using csv module and im going to parse the csv manually by rows and colums
columns=[]
datas=[]
with open(path,encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for i in csv_reader:
        columns.append(i)
        break
    index=0
    for i in csv_reader:
        index+=1
        if index==1:
            continue
        datas.append(i)    
take_col=columns[0]
# Here we are the unwanted character that are pre
for i in take_col:
    i=list(i)
    while i and not i[0].isalnum():
        i.pop(0)
    i="".join(i)
    columns.append(i)   

columns.pop(0)

custom_data_frame=[]
for row in range(len(datas)):
    current={}
    for col in range(len(columns)):
        current[columns[col]]=datas[row][col]
    custom_data_frame.append(current)

model = OllamaLLM(model="mistral:latest")

example=custom_data_frame[0]

query="count the total no of countries in Africa"

prompt=f'''
You are a python expert and return  me a python code,for that you are given a list of dictionaries in this format {example} and use this list and perform the following operation {query} on the list and store the result in a variable called 
result in the code and return the python code in between the ''code" which will be suitable and use the custom_data_frame variable as it already stored the data in the list,
example i will pass the custom_data_frame in this form eval(code,brackets,custom_data_frame) and dont reinialize anything just use the custom_data_frames and i repeat give only the python code
not any other things,so that i can call do somehting like below one
response = model.invoke(prompt)
local_vars = {"csv_data to custom_data_frame"}
exec(response, brackets, local_vars)
res=local_vars["result"]
'''

response = model.invoke(prompt)
code_match = re.search(r"```(?:python)?\n(.*?)```", response, re.DOTALL)
# print(code_match)
code_to_run = code_match.group(1)
print(code_to_run)
local_vars = {"custom_data_frame": custom_data_frame}
exec(code_to_run, {}, local_vars)

# y=mx+c

# y=w1*x1+w2*x2+w3*x3+...+b

# Aswinnath 

