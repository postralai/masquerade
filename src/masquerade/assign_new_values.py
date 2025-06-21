import requests
import random
import re

def generate_random_numbers(value):
    new_value = ''
    for char in value:
        if char.isdigit():
            new_value += str(random.randint(0, 9))
        else:
            new_value += char
    return new_value

def assign_new_value_with_llm(current_value, tinfoil_llm):
    # Check if the value contains only numbers, spaces and dashes
    if re.match(r'^[\d\s\-\+]+$', current_value):
        return generate_random_numbers(current_value)
    else:
        num_words = len(current_value.split())
        prompt = f"""You will be given a value.
Your task is to generate a new value of the same type:
— If it is a name, generate a different, realistic name, shorter than the original.
— If it is an address, generate a different, realistic address, shorter than the original.
The new value must have the same number of words.

Return only the new value. No extra words. No formatting.

Input: {current_value}
Output:"""
        max_trials = 20
        for i in range(max_trials):
            print(f"Assigning new value for {current_value}: Trial {i+1}/{max_trials}")
            new_value = tinfoil_llm.get_tinfoil_response(prompt, model="mistral")
            if len(new_value.split()) == len(current_value.split()):
                return new_value
        return "Error: Could not generate new value"

if __name__ == "__main__":
    print(assign_new_value_with_llm("09834058-32-34535-345422-3"))
    print(assign_new_value_with_llm("Koulupolku 8"))
    print(assign_new_value_with_llm("Kuljetus Testeri Oy"))
    print(assign_new_value_with_llm("0213 0225"))
