from src.generators.mock_data import generate_linux_shadow_entries, generate_windows_sam_entries
from src.generators.wordlist import generate_base_wordlist, apply_mutations
from src.simulation.engine import BruteForceSimulator

def main():
    print("=== CREDENTIAL AUDIT SIMULATOR (ETHICAL/SAFE MODE) ===")
    print("Initializing environment...\n")
    
    # 1. Generate Mock Data (The "Targets")
    # We purposefully inject known "base" words to verify the simulation works
    weak_passwords = ["summer2025", "admin", "secure"]
    linux_targets = generate_linux_shadow_entries(3, safe_passwords=weak_passwords)
    windows_targets = generate_windows_sam_entries(3, safe_passwords=weak_passwords)
    
    all_targets = linux_targets + windows_targets
    
    # 2. Generate Dictionary (The "Attack")
    print(f"\n[+] Generating Attack Dictionary...")
    base_words = generate_base_wordlist() # ["summer", "admin", etc]
    # We need to make sure our dictionary actually covers the patterns used above
    # The 'apply_mutations' handles 'summer' -> 'summer2025'
    full_wordlist = apply_mutations(base_words)
    print(f"    - Base words: {len(base_words)}")
    print(f"    - Mutated list size: {len(full_wordlist)}")
    
    # 3. Run Simulation
    print(f"\n[+] initializing Simulation Engine...")
    engine = BruteForceSimulator()
    results = engine.run_benchmark(all_targets, full_wordlist)
    
    # 4. Summary & Analytics
    print(f"\n=== SIMULATION RESULTS & ANALYTICS ===")
    from src.analytics.metrics import calculate_entropy, estimate_crack_time, evaluate_strength
    
    print(f"{'User':<15} | {'Password':<15} | {'Entropy':<8} | {'Strength':<10} | {'Est. Time (10GH/s)'}")
    print("-" * 85)
    
    for res in results:
        pw = res['password']
        ent = calculate_entropy(pw)
        strength = evaluate_strength(ent)
        time_est = estimate_crack_time(ent)
        print(f"{res['user']:<15} | {pw:<15} | {ent:<8} | {strength:<10} | {time_est}")

    print(f"\nTotal Success Rate: {len(results)}/{len(all_targets)}")
    
    # 5. Generate Professional Report
    print(f"\n[+] Generating Audit Report...")
    from src.reporting.report_generator import ReportGenerator
    reporter = ReportGenerator()
    reporter.generate_markdown_report(results, "Final_Security_Report.md")
    
if __name__ == "__main__":
    main()
