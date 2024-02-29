import subprocess

def run_seed():
    seeds = [
       "migrations/ChatSeed.py",
    ]

    for seed in seeds:
        try:
            subprocess.run(["python3",  seed])
            print(f"seed successful: {seed}")
        except subprocess.CalledProcessError as e:
            print(f"seed failed for {seed}. Error: {e}")

if __name__ == "__main__":
    run_seed()