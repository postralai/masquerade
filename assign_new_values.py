import requests
import random
import re

def generate_random_numbers_with_dashes(value):
    # Split the value by dashes
    parts = value.split('-')
    # Generate random numbers for each part, maintaining the same length
    new_parts = []
    for part in parts:
        if part.isdigit():
            # Generate a random number with the same number of digits
            new_number = ''.join(str(random.randint(0, 9)) for _ in range(len(part)))
            new_parts.append(new_number)
        else:
            new_parts.append(part)
    # Join the parts back together with dashes
    return '-'.join(new_parts)

def assign_new_value_with_llm(current_value):
    # Check if the value contains only numbers and dashes
    if re.match(r'^[\d-]+$', current_value):
        return generate_random_numbers_with_dashes(current_value)
    else:
        num_words = len(current_value.split())
        prompt = f"""You will be given a value.
Your task is to generate a new value of the same type:
— If it is a name, generate a different, realistic name.
— If it is an address, generate a different, realistic address.
The new value must have the same number of words.

Return only the new value. No extra words. No formatting.

Input: {current_value}
Output:"""
        max_trials = 20
        for i in range(max_trials):
            print(f"Assigning new value for {current_value}: Trial {i+1}/{max_trials}")
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                new_value = response.json()["response"].strip()
                if len(new_value.split()) == len(current_value.split()):
                    return new_value
            else:
                print(f"Error: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return new_value
        else:
            return f"Error: {response.status_code} - {response.text}"


if __name__ == "__main__":
    print(assign_new_value_with_llm("09834058-32-34535-345422-3"))
    print(assign_new_value_with_llm("Koulupolku 8"))
    print(assign_new_value_with_llm("Kuljetus Testeri Oy"))
    print(assign_new_value_with_llm("0213 0225"))