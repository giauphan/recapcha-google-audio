import subprocess
import sys

def run_migration():
    migrations = [
       "migrations/create_table.py",
    ]

    for migration in migrations:
        try:
            subprocess.run(["python3",  migration])
            print(f"Migration successful: {migration}")
        except subprocess.CalledProcessError as e:
            print(f"Migration failed for {migration}. Error: {e}")

if __name__ == "__main__":
    run_migration()