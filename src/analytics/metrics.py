import math

def calculate_entropy(password):
    """
    Calculates the Shannon entropy (in bits) of a password.
    Entropy = log2(Possible_Combinations)
    Possible_Combinations = Charset_Size ^ Password_Length
    """
    if not password:
        return 0
        
    charset_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_symbol: charset_size += 32 # Approximation for common special chars
    
    # E = L * log2(R)
    entropy = len(password) * math.log2(max(charset_size, 1))
    return round(entropy, 2)

def estimate_crack_time(entropy, hashrate=10_000_000_000):
    """
    Estimates time to crack based on entropy and a modern GPU cluster hashrate.
    Default hashrate: 10 GH/s for standard hashes (e.g., NTLM on single high-end GPU)
    Returns a human-readable string.
    """
    if entropy == 0:
        return "Instant"
        
    combinations = 2 ** entropy
    seconds = combinations / hashrate
    
    if seconds < 60:
        return f"{seconds:.4f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{days:.2f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"

def check_policy_compliance(password):
    """
    Checks if password meets standard corporate policy.
    Scope 4.D: Check complexity requirements.
    Rules: Length >= 8, mixed case, digits.
    """
    failures = []
    if len(password) < 8:
        failures.append("Too Short (<8)")
    if password.islower() or password.isupper():
        failures.append("No Mixed Case")
    if not any(c.isdigit() for c in password):
        failures.append("No Digits")
        
    return failures if failures else ["PASS"]

def evaluate_strength(entropy):
    """
    Classifies password strength based on entropy bits (NIST/Industry rules of thumb).
    """
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"
