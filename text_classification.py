from openai import OpenAI
import pandas as pd
import csv
import os 
from dotenv import load_dotenv
load_dotenv()
import json

# load environmental variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

persona = "greedy"
# 最後通牒，独裁者，匿名独裁者ゲームの時に変更する
experiment_set = 1
# 提案者が2通りの最後通牒ゲームの時に変更する
proposal_amount = 0
program_or_human = "program"


# csvファイルの読み込み
# 最後通牒ゲーム
df = pd.read_csv(f"ultimatum_result/{persona}/ultimatum_{experiment_set}.csv")
tags = ["To benefit both players", "To maximize their own benefit"]
dir_path = f"text_classification_result/ultimatum_result/{persona}"
file_path = os.path.join(dir_path, f"ultimatum_{experiment_set}.csv")

# 独裁者ゲーム
# df = pd.read_csv(f"dictator_game_result/{persona}/dictator_{experiment_set}.csv")
# tags = ["That the other party has no right of refusal", "To encourage acceptance", "To create a sence of fairness"]
# tags = ["To benefit both players", "To maximize their own benefit", "That the other party has no right of refusal"]
# dir_path = f"text_classification_result/dictator_game_result/{persona}"
# file_path = os.path.join(dir_path, f"dictator_{experiment_set}.csv")


# 匿名独裁者ゲーム
# df = pd.read_csv(f"dictator_game_anonymous_result/{persona}/dictator_anomymous_{experiment_set}.csv")
# tags = ["That the other party has no right of refusal", "To create a sence of fairness", "That your actions are not known to the other party."]
# tags = ["To benefit both players", "To maximize their own benefit", "That the other party has no right of refusal", "That your actions are not known to the other party."]
# dir_path = f"text_classification_result/dictator_game_anonymous/{persona}"
# file_path = os.path.join(dir_path, f"dictator_anonymous_{experiment_set}.csv")



# 提案者が2通りの最後通牒ゲーム
# df = pd.read_csv(f"unfair_receiver_{program_or_human}_results/{persona}/unfair_receiver_{program_or_human}_results_{proposal_amount}_{100-proposal_amount}.csv")
# dir_path = f"text_classification_result/unfair_receiver_{program_or_human}_results/{persona}"
# file_path = os.path.join(dir_path, f"unfair_receiver_{program_or_human}_results_{proposal_amount}_{100-proposal_amount}.csv")

# 提案者がエージェントの時
# tags = ["The deal is unfair, but it can't be helped"]
# 提案者がコンピュータの時
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
for reason in df["reason"]:
    classifier = TextClassifier(api_key=OPENAI_API_KEY)
    result = classifier.classify_text(reason, tags)
    print(json.loads(result.content))
    data.append(json.loads(result.content))
    
    


os.makedirs(dir_path, exist_ok=True)



keys = data[0].keys()

with open(file_path, "w", newline="") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    
    
    