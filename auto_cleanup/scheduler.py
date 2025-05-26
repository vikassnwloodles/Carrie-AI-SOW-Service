from apscheduler.schedulers.background import BackgroundScheduler
from .cleanup import delete_old_files



scheduler = BackgroundScheduler()

def start_auto_cleanup_scheduler():
    scheduler.add_job(
        func=lambda: delete_old_files(),
        trigger="interval",
        days=1,
        id="old_files_cleanup_job",
        replace_existing=True,
    )

    scheduler.start()


def shutdown_auto_cleanup_scheduler():
    scheduler.shutdown(wait=True)
