import requests
import time
import sys
import os
import random

BIBLE_PATH = os.path.expanduser("~/Documents/nasb.txt")

def typewriter_print(text):
    """Prints with slight speed variance for a more 'possessed' typewriter feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # Random jitter between 0.02 and 0.08 seconds
        time.sleep(random.uniform(0.02, 0.08))
    print("\n")

def get_true_entropy(count, max_val):
    """Fetches 'n' true random numbers from random.org."""
    url = f"https://www.random.org/integers/?num={count}&min=0&max={max_val}&col=1&base=10&format=plain&rnd=new"
    try:
        response = requests.get(url, timeout=5)
        nums = [int(n) for n in response.text.strip().split('\n')]
        return nums
    except:
        # Fallback to local pseudo-rng if internet/API fails
        return [random.randint(0, max_val) for _ in range(count)]

def main():
    if not os.path.exists(BIBLE_PATH):
        print(f"File not found: {BIBLE_PATH}")
        return

    with open(BIBLE_PATH, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    # Filter for content
    valid_verses = [line.strip() for line in all_lines if len(line.strip()) > 10]
    total_valid = len(valid_verses)
    
    print("--- COMMUNICATING WITH THE ORACLE ---")
    
    # We ask for 4 numbers: 1 for the verse, 3 for random 'God-Words'
    random_indices = get_true_entropy(4, total_valid - 1)
    
    if random_indices:
        # 1. The Verse
        verse_idx = random_indices[0]
        verse = valid_verses[verse_idx]
        
        # 2. The God-Words (extracting a single random word from 3 other verses)
        god_words = []
        for i in range(1, 4):
            other_verse = valid_verses[random_indices[i]].split()
            word = random.choice(other_verse).strip(".,;:?!()\"")
            god_words.append(word.upper())

        print(f"[Entropy Source: random.org | Index {verse_idx}]\n")
        
        typewriter_print(verse)
        
        # Output the 'God-Words' in a distinct block
        print("GOD SAYS:")
        typewriter_print(f"--- {' '.join(god_words)} ---")
    
    print("------------------------------------------")

if __name__ == "__main__":
    main()
