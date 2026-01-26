import time
import hashlib
import statistics

class BruteForceSimulator:
    def __init__(self, mode="BENCHMARK"):
        self.mode = mode
        self.results = []
        
    def _simulate_linux_hash(self, password, salt):
        """Replicates the SHA-512 mock hash logic for verification."""
        target = f"{salt}{password}".encode('utf-8')
        return hashlib.sha512(target).hexdigest()[:86]

    def _simulate_ntlm_hash(self, password):
        """Replicates the NTLM mock hash logic for verification."""
        try:
            hash_obj = hashlib.new('md4', password.encode('utf-16le'))
        except ValueError:
            # Fallback for systems without MD4 (e.g., FIPS compliant)
            hash_obj = hashlib.md5(password.encode('utf-16le'))
        return hash_obj.hexdigest().upper()

    def crack_linux(self, target_entry, wordlist):
        """
        Simulates cracking a Linux shadow entry.
        Entry format: username:$6$salt$hash...
        """
        parts = target_entry.split(':')
        username = parts[0]
        hash_field = parts[1]
        
        # Parse $6$salt$hash
        if not hash_field.startswith("$6$"):
            return None
            
        _, _, salt, target_hash = hash_field.split('$')[:4]
        
        start_time = time.time()
        attempts = 0
        
        for word in wordlist:
            attempts += 1
            # The "attack": Hash the guess and compare
            guess_hash = self._simulate_linux_hash(word, salt)
            
            if guess_hash == target_hash:
                elapsed = time.time() - start_time
                return {
                    "user": username,
                    "password": word,
                    "attempts": attempts,
                    "time_taken": elapsed,
                    "type": "Linux (SHA-512 Mock)"
                }
        
        return None # Failed to crack

    def crack_windows(self, target_entry, wordlist):
        """
        Simulates cracking a Windows SAM entry.
        Entry format: User:RID:LM:NTLM:::
        """
        parts = target_entry.split(':')
        username = parts[0]
        target_ntlm = parts[3]
        
        start_time = time.time()
        attempts = 0
        
        for word in wordlist:
            attempts += 1
            guess_hash = self._simulate_ntlm_hash(word)
            
            if guess_hash == target_ntlm:
                elapsed = time.time() - start_time
                return {
                    "user": username,
                    "password": word,
                    "attempts": attempts,
                    "time_taken": elapsed,
                    "type": "Windows (NTLM Mock)"
                }
                
        return None

    def crack_incremental(self, target_entry, max_length=4):
        """
        Simulates an INCREMENTAL brute-force attack (a-z, 0-9).
        Scope 4.C: Support incremental mode.
        WARNING: Restrained to max_length=4 for demonstration safety and speed.
        """
        import itertools
        import string
        
        chars = string.ascii_lowercase + string.digits # 'a-z0-9'
        attempts = 0
        
        # Determine target hash (simplified wrapper)
        target_hash = ""
        is_linux = False
        salt = ""
        
        if "$6$" in target_entry:
            parts = target_entry.split(':')
            if len(parts) > 1:
                _, _, salt, target_hash = parts[1].split('$')[:4]
                is_linux = True
        elif ":" in target_entry:
             target_hash = target_entry.split(':')[3]
        
        print(f"       [Incremental] Scanning 1-{max_length} chars for {target_entry[:15]}...")
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            for guess_tuple in itertools.product(chars, repeat=length):
                attempts += 1
                guess = "".join(guess_tuple)
                
                # Check
                if is_linux:
                    h = self._simulate_linux_hash(guess, salt)
                else:
                    h = self._simulate_ntlm_hash(guess)
                    
                if h == target_hash:
                    elapsed = time.time() - start_time
                    return {
                        "user": "Unknown",
                        "password": guess,
                        "attempts": attempts,
                        "time_taken": elapsed,
                        "type": "Incremental Force"
                    }
                    
                # Timeout safety (stop after 2 seconds for demo)
                if time.time() - start_time > 2.0:
                    return {"password": None, "attempts": attempts, "time_taken": 2.0, "type": "TIMEOUT"}
                    
        return None

    def run_benchmark(self, mock_data, wordlist):
        """
        Runs the full simulation against a list of mock entries.
        """
        print(f"[*] Starting Brute-Force Simulation on {len(mock_data)} targets with {len(wordlist)} dictionary words...")
        
        simulation_stats = []
        
        for entry in mock_data:
            result = None
            if entry.startswith("mock_user") or "$6$" in entry:
                result = self.crack_linux(entry, wordlist)
            elif ":" in entry: # Simple heuristic for SAM
                result = self.crack_windows(entry, wordlist)
            
            if result:
                print(f"   [CRACKED] {result['user']} : {result['password']} ({result['attempts']} attempts, {result['time_taken']:.4f}s)")
                simulation_stats.append(result)
            else:
                print(f"   [FAILED] Could not crack user in supplied list.")
                
        return simulation_stats

if __name__ == "__main__":
    # Test stub
    sim = BruteForceSimulator()
    print("Simulator ready.")
