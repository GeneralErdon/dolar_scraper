import subprocess
import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def run_scrapy():
    subprocess.run(["scrapy", "crawl", "BCV"])
    subprocess.run(["scrapy", "crawl", "MONITOR"])


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scrapy, "cron", hour=9, minute=30)
    scheduler.add_job(run_scrapy, "cron", hour=13, minute=30)
    # scheduler.add_job(run_scrapy, "cron", minute="*")
    
    print("Scheduler started at %s" % datetime.now().strftime("%d-%m-%Y  %H:%M:%S"))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting scheduler.... Bye!")