from flask import Flask
from termcolor import colored
import pandas as pd
import markovify

app = Flask(__name__)

print(colored("##########################################################################", "yellow"))
print(colored("############### POC CADEIA DE MARKOV PARA ANÁLISE DE TEXTO ###############", "yellow"))
print(colored("##########################################################################\n", "yellow"))

print(colored("Entre aqui o caminho para o arquivo que deverá ser analisado:", "blue"), end =" ")

data_file = input()

df = pd.read_csv(data_file)

print("Dados carregados com sucesso!\n")

df.dropna(subset=['Star Rating'], inplace = True)
df.dropna(subset=['Review Text'], inplace = True)
df.drop_duplicates(inplace = True)

print("Dados limpos com sucesso!\n")

for x in df.index:
  if df.loc[x, "Star Rating"] == 5 or df.loc[x, "Star Rating"] == 4:
    f = open("entusiastas_playstore.txt", "a")
    f.write(df.loc[x, "Review Text"] + ". ")
    f.close
    print(colored("+", "green"), end ="")
  else:
    f = open("detratores_playstore.txt", "a")
    f.write(df.loc[x, "Review Text"] + ". ")
    f.close    
    print(colored("-", "red"), end ="")

print("\nDados filtrados com sucesso!\n")

with open("entusiastas_playstore.txt") as f:
    entusiastas = f.read()

positive_text_model = markovify.Text(entusiastas, state_size=2)

print(colored("Condensação de experiências positivas:", "green"))
for i in range(5):
    print(positive_text_model.make_sentence(tries=100) + "\n")

with open("detratores_playstore.txt") as f:
    detratores = f.read()

negative_text_model = markovify.Text(detratores, state_size=2)

print(colored("\nCondensação de experiências negativas:", "red"))

for i in range(5):
    print(negative_text_model.make_sentence(tries=100) + "\n")
