import requests
import time
import sys
import os
import random

# Path to your NASB file
BIBLE_PATH = os.path.expanduser("~/Documents/nasb.txt")

def typewriter_print(text):
    """Prints with slight speed variance for a mechanical feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # The 'jitter' - subtle variation in typing speed
        time.sleep(random.uniform(0.02, 0.08))
    print("\n")

def get_true_entropy(max_val):
    """Fetches 1 true random number from random.org based on atmospheric noise."""
    url = f"https://www.random.org/integers/?num=1&min=0&max={max_val}&col=1&base=10&format=plain&rnd=new"
    try:
        response = requests.get(url, timeout=5)
        return int(response.text.strip())
    except Exception as e:
        # Fallback to local entropy if the connection is interrupted
        return random.randint(0, max_val)

def main():
    if not os.path.exists(BIBLE_PATH):
        print(f"File not found: {BIBLE_PATH}")
        return

    # Load and filter for lines that actually contain text
    with open(BIBLE_PATH, 'r', encoding='utf-8') as f:
        valid_verses = [line.strip() for line in f.readlines() if len(line.strip()) > 5]
    
    total_valid = len(valid_verses)
    
    print("--- true rng ---")
    
    # Get our one 'True' index
    verse_idx = get_true_entropy(total_valid - 1)
    
    if verse_idx is not None:
        verse = valid_verses[verse_idx]
        
        print(f"[Entropy Index: {verse_idx}]\n")
        typewriter_print(verse)
    
    print("------------------------------------------")

if __name__ == "__main__":
    main()
