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

def remove_unchanged_words(value):
    for word in unchanged_words:
        if word in value:
            parts = value.split(word)
            value = ''.join(parts).strip()
    return value


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
    for value in values:
        print(remove_unchanged_words(value))
