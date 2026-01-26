import secrets
import string
import hashlib
import uuid

def _generate_salt(length=8):
    """Generates a random salt string."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def _mock_hash_sha512(password, salt):
    """
    Simulates a SHA-512 crypt hash. 
    Note: In a real audit, we'd extract this. Here we GENERATE it to simulate the target.
    Structure: $6$salt$hash_output
    """
    # Simply hashing the combo for visual simulation. 
    # Not using actual crypt.crypt for cross-platform compatibility and safety.
    target = f"{salt}{password}".encode('utf-8')
    return hashlib.sha512(target).hexdigest()[:86] # Truncate to resemble crypt output

def _mock_ntlm_hash(password):
    """
    Simulates an NTLM hash (MD4 of little-endian UTF-16 Unicode).
    """
    # Windows uses MD4. standard hashlib often includes MD4 (via 'new') but depends on OpenSSL.
    # If MD4 is unavailable (common in FIPS modes), we mock it with MD5 shortened.
    try:
        hash_obj = hashlib.new('md4', password.encode('utf-16le'))
    except ValueError:
        hash_obj = hashlib.md5(password.encode('utf-16le')) 
    
    return hash_obj.hexdigest().upper()

def generate_linux_shadow_entries(count=5, safe_passwords=None):
    """
    Generates synthetic /etc/shadow entries.
    entries are: username:$id$salt$encrypted:lastchange:min:max:warn:inact:expire
    """
    if safe_passwords is None:
        safe_passwords = ["password123", "qwerty", "admin", "welcome1", "summer2025"]
    
    entries = []
    print(f"[+] Generating {count} synthetic Linux shadow entries...")
    
    for i in range(count):
        user = f"mock_user_{1000+i}"
        salt = _generate_salt(16) # SHA-512 uses longer salts usually
        pw = safe_passwords[i % len(safe_passwords)]
        pw_hash = _mock_hash_sha512(pw, salt)
        
        # ID 6 is SHA-512
        shadow_line = f"{user}:$6${salt}${pw_hash}:19749:0:99999:7:::"
        entries.append(shadow_line)
    
    return entries

def generate_windows_sam_entries(count=5, safe_passwords=None):
    """
    Generates synthetic Windows SAM (PWDUMP format) entries.
    entries are: User:RID:LM:NTLM:::
    """
    if safe_passwords is None:
        safe_passwords = ["P@ssword!", "Admin@123", "LetsGo!", "Secure#2025", "Blank"]
        
    entries = []
    print(f"[+] Generating {count} synthetic Windows SAM entries...")
    
    for i in range(count):
        user = f"MockUser_{1000+i}"
        rid = 1000 + i
        
        pw = safe_passwords[i % len(safe_passwords)]
        ntlm = _mock_ntlm_hash(pw)
        lm = "AAD3B435B51404EEAAD3B435B51404EE" # Standard empty/dummy LM hash
        
        # PWDUMP format
        sam_line = f"{user}:{rid}:{lm}:{ntlm}:::"
        entries.append(sam_line)
        
    return entries

if __name__ == "__main__":
    # Self-test when run directly
    print("--- SYNTHETIC LINUX SHADOW ---")
    for line in generate_linux_shadow_entries(3):
        print(line)
        
    print("\n--- SYNTHETIC WINDOWS SAM ---")
    for line in generate_windows_sam_entries(3):
        print(line)
