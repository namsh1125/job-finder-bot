import json
import logging

from datetime import datetime, timedelta
from config import SECRET_NAME, REGION_NAME
from secrets_manager import get_secret_values
from saramin_api import get_entry_level_job_data
from slack_message import create_slack_message, send_slack_message
from zoneinfo import ZoneInfo


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        saramin_api_key, job_info = get_secret_values(SECRET_NAME, REGION_NAME)
        yesterday = (datetime.now(ZoneInfo("Asia/Seoul")) - timedelta(days=1)).strftime('%Y-%m-%d')
        
        all_jobs = {}
        for job_cd, info in job_info.items():
            entry_level_jobs = get_entry_level_job_data(saramin_api_key, job_cd, yesterday)
            logger.info(f"Total filtered jobs for {job_cd}: {len(entry_level_jobs)}")
            
            message = create_slack_message(yesterday, entry_level_jobs, job_info, job_cd)
            send_slack_message(info['webhook_url'], message)
            
            all_jobs[job_cd] = entry_level_jobs

        return {
            'statusCode': 200,
            'body': json.dumps({
                'job_count': sum(len(jobs) for jobs in all_jobs.values()),
                'job_info': all_jobs
            }, ensure_ascii=False).encode('utf8')
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }