import random
import time
import os
import nltk
from nltk.corpus import wordnet as wn
import requests

# Ensure the NLTK WordNet data is downloaded
nltk.download('wordnet')

# Set the path to the WordNet data directory
wordnet_path = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop', 'Dictionary project', 'WNdb-3.0')
nltk.data.path.append(wordnet_path)


def binary_search_wordnet(word):
    for pos in ['noun', 'verb', 'adj', 'adv']:
        index_file = os.path.join(wordnet_path, 'dict', f'index.{pos}')
        print(f"Checking file: {index_file}")
        if os.path.exists(index_file):
            with open(index_file, 'r') as file:
                lines = file.readlines()
                low, high = 0, len(lines) - 1
                while low <= high:
                    mid = (low + high) // 2
                    line = lines[mid].strip()
                    if line.startswith(word):
                        return line
                    elif word < line:
                        high = mid - 1
                    else:
                        low = mid + 1
        else:
            print(f"File not found: {index_file}")
    return None


def get_wordnet_definition(word):
    line = binary_search_wordnet(word)
    if line:
        synsets = wn.synsets(word)
        if synsets:
            definition = synsets[0].definition()
            related_words = [lemma.name() for lemma in synsets[0].lemmas()]
            return definition, related_words
    return None, None


def get_api_definition(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        related_words = [synonym for synonym in data[0]['meanings'][0]['definitions'][0].get('synonyms', [])]
        return definition, related_words
    return None, None


def lookup_word(word):
    start_time = time.time()
    definition, related_words = get_wordnet_definition(word)
    if not definition:
        definition, related_words = get_api_definition(word)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if definition:
        print(f"Definition of {word}: {definition}")
        if related_words:
            print(f"Related words: {', '.join(related_words)}")
    else:
        print(f"No definition found for {word}.")
    print(f"Search and output time: {elapsed_time:.4f} seconds")


def find_random_word():
    words = list(wn.words())
    word = random.choice(words)
    lookup_word(word)


def main():
    while True:
        print("\nDictionary Menu:")
        print("1. Look up a word")
        print("2. Find a random word")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            word = input("Enter the word to look up: ")
            lookup_word(word)
        elif choice == '2':
            find_random_word()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()