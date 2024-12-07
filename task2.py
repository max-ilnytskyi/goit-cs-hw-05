import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import matplotlib.pyplot as plt

import requests

URL = "https://gutenberg.net.au/ebooks01/0100021.txt"


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return reduced_values


def visualize_top_words(all_words, top_amount=10):
    top_words = sorted(all_words, key=lambda x: x[1], reverse=True)[:top_amount]

    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top {} Most Frequent Words".format(len(top_words)))
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    text = get_text(URL)
    if text:
        map_reduce_result = map_reduce(text)

        visualize_top_words(map_reduce_result, 10)
    else:
        print("Error: Can't read file.")
