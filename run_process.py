import subprocess, sys, time, os, pytz
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

BOT_SCRIPT_PATH = os.getenv("BOT_SCRIPT_PATH")


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
    time.sleep(2)
    start_bot()


def status_bot():
    if is_bot_running():
        print("Bot is already running.")
        return

    print("Bot is not running.")


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

    now = datetime.now()
    vietnam_timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    vietnam_time = now.astimezone(vietnam_timezone)
    time_start = vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(CURRENT_DIR, "/log/bcdn.log")
    file_size = os.stat(path).st_size if os.path.exists(path) else 0
    if file_size >= 5000000:
        os.remove(path)

    print(f"Starting the bot at {time_start} - size log {file_size}...")

    if action == "start":

        start_bot()
    elif action == "restart":
        restart_bot()
    elif action == "stop":
        stop_bot()
    elif action == "status":
        status_bot()
    else:
        print("Invalid action. Please use 'start', 'restart', or 'stop' or status.")
        sys.exit(1)
