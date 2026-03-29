import pandas as pd
#import requests
import json
import os
from dotenv import load_dotenv
import requests
load_dotenv()



df = pd.read_csv("userId.csv")


with open("user.json","r",encoding="utf-8") as f:
    user_json = json.load(f)


user_id = df["userId"].tolist()

def get_user(id):
   ## response = requests.get(f"{base_url}/{id}")
   ##return response.json() if response.status_code == 200 else None
   
    for u in user_json :
        if u["id"] == id:
            return u
    return None



def generate_ai_news(user):
    prompt = f"""
    Responda APENAS com uma frase.
    Máximo 100 caracteres.
    Sem explicações.

    Mensagem para {user['name']} sobre investimentos.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        text = response.json().get("response", "").strip()

        # 🔥 limpa quebra de linha e corta
        text = text.split("\n")[0]
        return text[:100]

    except Exception as e:
        return f"Erro: {e}"

    
#compreensao de lista
users = [user for id in user_id if (user := get_user(id)) is not None]

#identação
print(json.dumps(users,indent=2))



for user in users:
    new = generate_ai_news(user)
    print(new)
    if "news" not in user:
        user["news"] = []
        
    user["news"].append({
        "id": len(user["news"]) + 1,
        "description":new
    })
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user_json, f, indent=2, ensure_ascii=False)