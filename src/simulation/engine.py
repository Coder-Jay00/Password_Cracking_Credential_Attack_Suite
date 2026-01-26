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
