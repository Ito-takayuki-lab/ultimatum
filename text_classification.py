from openai import OpenAI
import pandas as pd
import csv
import os 
from dotenv import load_dotenv
load_dotenv()
import json

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

persona = "not_strategic"
proposal_amount = 20
program_or_human = "program"
number = 3

# csvファイルの読み込み
# df = pd.read_csv(f"dictator_game_anonymous_result/{persona}/dictator_anomymous_{number}.csv")
# df = pd.read_csv("ultimatum_result/strategic/ultimatum_3.csv")
# df = pd.read_csv(f"dictator_game_result/{persona}/dictator_{number}.csv")
df = pd.read_csv(f"unfair_receiver_{program_or_human}_results/{persona}/unfair_receiver_{program_or_human}_results_{proposal_amount}_{100-proposal_amount}.csv")


# ultimatum gameの時のタグを追加する
# tags = ["To benefit both players", "To maximize their own benefit"]

# dictator gaeの時のタグを追加する

# tags = ["That the other party has no right of refusal", "To encourage acceptance", "To create a sence of fairness"]
# tags = ["To benefit both players", "To maximize their own benefit", "That the other party has no right of refusal"]

# dictator anomymous gameの時のタグを追加する
# tags = ["That the other party has no right of refusal", "To create a sence of fairness", "That your actions are not known to the other party."]
# tags = ["To benefit both players", "To maximize their own benefit", "That the other party has no right of refusal", "That your actions are not known to the other party."]


# unfair receiver gameの時のタグを追加する
# Agent
tags = ["The deal is unfair, but it can't be helped"]

# Computer
# tags =  ["the proposer is a computer program", "The deal is unfair, but it can't be helped"]



# TextClassifierクラスの実装
class TextClassifier:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def classify_text(self, text, tags):
        formatted_tags = {item : "<0 or 1>" for item in tags}
        # system_message
        system_message = f"""
        Output 1 if the following tags apply to the given text, 0 otherwise.
        {", ".join(tags)}
        Please provide your answer in a single-line JSON format.
        {formatted_tags}
        """   
        
        # usert_message
        user_message = text
        
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            print(f"classifing : {text}")
            return completion.choices[0].message
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}                                                  


data = []
# データフレームの各要素に対してテキスト分類
for reason in df["resaon"]:
    classifier = TextClassifier(api_key=OPENAI_API_KEY)
    result = classifier.classify_text(reason, tags)
    print(json.loads(result.content))
    data.append(json.loads(result.content))
    
dir_path = f"text_classification_result/unfair_receiver_{program_or_human}_results_2/{persona}"
# dir_path = f"text_classification_result/dictator_game_anonymous/{persona}"
os.makedirs(dir_path, exist_ok=True)

file_path = os.path.join(dir_path, f"unfair_receiver_{program_or_human}_results_{proposal_amount}_{100-proposal_amount}.csv")
# file_path = os.path.join(dir_path, f"dictator_anonymous_{number}.csv")
keys = data[0].keys()

with open(file_path, "w", newline="") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    
    
    