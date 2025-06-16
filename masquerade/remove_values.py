unchanged_words = [
    "Y-tunnus",
    "Sopimusnumero",
    "Asiakasnumero",
    "puhelinnumero",
    "puhelin",
    "puh",
    "email",
    "sähköpostiosoite",
    "sähköposti",
]

def remove_unchanged_words(values):
    for i in range(len(values)):
        for word in unchanged_words:
            if word in values[i]:
                parts = values[i].split(word)
                values[i] = ''.join(parts).strip()
                break
    return values


if __name__ == "__main__":
    values = [
        "Y-tunnus 1234567-8",
        "Sopimusnumero 1234567890",
        "Asiakasnumero 1234567890",
        "puh: 1234567890",
        "puhelin 1234567890",
        "puhelinnumero 1234567890",
        "email 1234567890",
        "sähköposti 1234567890",
        "sähköpostiosoite 1234567890",
    ]
    print(remove_unchanged_words(value))
