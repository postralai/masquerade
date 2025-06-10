from tinfoil import TinfoilAI
import re
import os

with open("api_keys/tinfoil_api_key.txt", "r") as f:
    api_key = f.read().strip()

client = TinfoilAI(
    enclave="deepseek-r1-70b-p.model.tinfoil.sh",
    repo="tinfoilsh/confidential-deepseek-r1-70b-prod",
    api_key=api_key,
)

def get_tinfoil_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-70b",
    )
    cleaned_content = re.sub(
        r"<think>.*?</think>", "",
        chat_completion.choices[0].message.content,
        flags=re.DOTALL).strip()
    return cleaned_content


if __name__ == "__main__":
    while True:
        user_text = input("User: ")
        print("LLM:", get_tinfoil_response(user_text))
