import re

def identify_hash_type(hash_string):
    """
    Analyzes a hash string to identify the likely algorithm.
    Scope 4.B: Identify hashing algorithms used.
    """
    hash_string = hash_string.strip()
    
    # Linux Crypt Signatures
    if hash_string.startswith("$6$"):
        return "SHA-512 (Linux crypt)"
    if hash_string.startswith("$5$"):
        return "SHA-256 (Linux crypt)"
    if hash_string.startswith("$1$"):
        return "MD5 (Linux crypt)"
    if hash_string.startswith("$2a$") or hash_string.startswith("$2b$") or hash_string.startswith("$2y$"):
        return "Bcrypt"
        
    # Windows NTLM/LM (Hex based)
    # NTLM is 32 hex chars (128 bit)
    if len(hash_string) == 32 and re.fullmatch(r"[0-9a-fA-F]+", hash_string):
        return "NTLM / MD5 (Windows)"
        
    return "Unknown Format"
