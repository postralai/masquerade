from tinfoil import TinfoilAI
import re
import os

class TinfoilLLM:
    def __init__(self):
        if os.getenv("TINFOIL_API_KEY") is None:
            raise ValueError("TINFOIL_API_KEY is not set")
        self.api_key = os.getenv("TINFOIL_API_KEY")

        # Initialize clients for different models
        self.deepseek_client = TinfoilAI(
            enclave="deepseek-r1-70b-p.model.tinfoil.sh",
            repo="tinfoilsh/confidential-deepseek-r1-70b-prod",
            api_key=self.api_key,
        )
        self.mistral_client = TinfoilAI(
            enclave="mistral-s-3-1-24b-p.model.tinfoil.sh",
            repo="tinfoilsh/confidential-mistral-small-3-1",
            api_key=self.api_key,
        )

    def get_tinfoil_response(self, prompt, model="deepseek"):
        if model == "deepseek":
            client = self.deepseek_client
            model_name = "deepseek-r1-70b"
        elif model == "mistral":
            client = self.mistral_client
            model_name = "mistral-small-3-1-24b"
        else:
            raise ValueError(f"Invalid model: {model}")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
        )
        cleaned_content = re.sub(
            r"<think>.*?</think>", "",
            chat_completion.choices[0].message.content,
            flags=re.DOTALL).strip()
        return cleaned_content


if __name__ == "__main__":
    tinfoil_llm = TinfoilLLM()
    while True:
        user_text = input("User: ")
        print("LLM:", tinfoil_llm.get_tinfoil_response(user_text))
