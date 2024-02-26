import subprocess, sys, time, os
from dotenv import load_dotenv

load_dotenv()

BOT_SCRIPT_PATH = os.getenv('BOT_SCRIPT_PATH')

def is_bot_running():
    try:
        subprocess.run(["pgrep", "-f", BOT_SCRIPT_PATH], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_bot():
    if is_bot_running():
        print("Bot is already running.")
        return
    print("Starting the bot...")
    subprocess.Popen(["python3", BOT_SCRIPT_PATH])

def restart_bot():
    stop_bot()
    time.sleep(2)  # Wait for the bot to stop
    start_bot()

def stop_bot():
    if not is_bot_running():
        print("Bot is not running.")
        return
    print("Stopping the bot...")
    subprocess.run(["pkill", "-f", BOT_SCRIPT_PATH])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_bot.py [start|restart|stop]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "start":
        start_bot()
    elif action == "restart":
        restart_bot()
    elif action == "stop":
        stop_bot()
    else:
        print("Invalid action. Please use 'start', 'restart', or 'stop'.")
        sys.exit(1)