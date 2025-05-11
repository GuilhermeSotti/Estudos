from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from config.logging_config import setup_logging
from processing.etl_job import run_aws_glue_job

setup_logging()
logger = logging.getLogger("scheduler")

def scheduled_etl():
    logger.info("Iniciando job ETL agendado")
    run_aws_glue_job()

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="America/Sao_Paulo")
    # Agenda para rodar todo dia às 2h da manhã
    scheduler.add_job(scheduled_etl, 'cron', hour=2, minute=0)
    logger.info("Scheduler iniciado. ETL rodará diariamente às 02:00 BRT")
    scheduler.start()
