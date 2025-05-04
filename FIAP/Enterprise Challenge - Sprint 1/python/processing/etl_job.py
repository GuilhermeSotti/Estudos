import os
import logging
import boto3
from config.settings import AWS_REGION, GLUE_JOB_NAME
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("etl_job")

def run_aws_glue_job(job_name=GLUE_JOB_NAME, arguments=None):
    glue = boto3.client("glue", region_name=AWS_REGION)
    params = {"--JOB_NAME": job_name}
    if arguments:
        params.update(arguments)
    response = glue.start_job_run(JobName=job_name, Arguments=params)
    job_run_id = response.get("JobRunId")
    logger.info(f"Glue job iniciado: {job_name} (RunId: {job_run_id})")
    return job_run_id

def main():
    # Exemplo de argumentos adicionais caso queira parametrizar datas, paths, etc.
    extra_args = {
        "--s3_input_path": f"s3://{os.getenv('S3_BUCKET')}/raw/",
        "--s3_output_path": f"s3://{os.getenv('S3_BUCKET')}/processed/"
    }
    run_aws_glue_job(arguments=extra_args)

if __name__ == "__main__":
    main()
