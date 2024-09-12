import nltk
import random
from nltk.corpus import wordnet as wn

# Ensure you have WordNet
nltk.download('wordnet')


# Function to perform binary search on the list of words
def binary_search(word_list, target_word):
    low, high = 0, len(word_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if word_list[mid] < target_word:
            low = mid + 1
        elif word_list[mid] > target_word:
            high = mid - 1
        else:
            return mid
    return -1  # Word not found


# Step 1: Read words from dictionary.txt
def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():  # Ignore empty lines
                words.append(line.strip())
    return sorted(words)  # Sort the words for binary search


# Step 2: Fetch definition and related words using WordNet
def fetch_definition_and_related_words(word):
    synsets = wn.synsets(word)
    if synsets:
        definition = synsets[0].definition()  # Get the first definition
        related_words = [lemma.name() for lemma in synsets[0].lemmas()]
        return definition, related_words
    return None, None


# Step 3: Main function to search for a word and get its definition
def get_word_definition(file_path, target_word):
    # Read the words from the file
    words = read_words_from_file(file_path)

    # Use binary search to find the word
    word_index = binary_search(words, target_word)

    if word_index != -1:
        word = words[word_index]
        # Fetch the definition and related words from WordNet
        definition, related_words = fetch_definition_and_related_words(word)
        if definition:
            print(f"Word: {word}")
            print(f"Definition: {definition}")
            print(f"Related words: {', '.join(related_words)}\n")
        else:
            print(f"Word '{word}' found, but no definition available in WordNet.")
    else:
        print(f"Word '{target_word}' not found in dictionary.")


# Step 4: Function to get a random word and its definition
def get_random_word(file_path):
    # Read the words from the file
    words = read_words_from_file(file_path)
    # Choose a random word
    random_word = random.choice(words)
    # Get the definition of the random word
    get_word_definition(file_path, random_word)


# Step 5: Console menu for user interaction
def console_menu(file_path):
    while True:
        print("Dictionary Menu:")
        print("1. Look up a word")
        print("2. Get a random word")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ").strip()

        if choice == '1':
            target_word = input("Enter the word you want to look up: ").strip().lower()
            get_word_definition(file_path, target_word)
        elif choice == '2':
            get_random_word(file_path)
        elif choice == '3':
            print("Exiting the dictionary. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Example usage:
file_path = "dictionary.txt"  # Path to your dictionary file
console_menu(file_path)
