import itertools

def generate_base_wordlist():
    """
    Returns a list of common base words often found in passwords.
    In a real scenario, this might come from 'rockyou.txt', but here we synthesize safe ones.
    """
    return [
        "password", "admin", "welcome", "summer", "winter", 
        "secure", "company", "login", "student", "qwerty"
    ]

def apply_mutations(base_words):
    """
    Applies common password mutation patterns (leetspeak, appending years/symbols).
    """
    mutated_list = set(base_words) # Use set to avoid duplicates
    
    # 1. Leet Speak Map
    leet_map = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5']
    }
    
    print(f"[+] Applying mutations to {len(base_words)} base words...")
    
    for word in base_words:
        # Strategy A: Simple Append (Common years 2020-2026)
        for year in range(2020, 2027):
            mutated_list.add(f"{word}{year}")
            mutated_list.add(f"{word.capitalize()}{year}")
            
        # Strategy B: Simple Leet Speak (Single char replacement)
        # Replacing just the first occurrence for simulation speed
        for char, replacements in leet_map.items():
            if char in word:
                for rep in replacements:
                    mutated_list.add(word.replace(char, rep))
                    mutated_list.add(word.replace(char, rep).capitalize())

        # Strategy C: Complex Leet Speak (Replace ALL occurrences)
        # E.g. "password" -> "p@ssw0rd"
        temp_word = word
        for char, replacements in leet_map.items():
            if char in temp_word:
                temp_word = temp_word.replace(char, replacements[0])
        mutated_list.add(temp_word)
        mutated_list.add(temp_word + "123") # Common pattern
        
    return sorted(list(mutated_list))

if __name__ == "__main__":
    base = generate_base_wordlist()
    final_list = apply_mutations(base)
    print(f"Generated {len(final_list)} variations from {len(base)} base words.")
    print("Sample (first 10):", final_list[:10])
