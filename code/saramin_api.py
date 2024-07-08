import requests
import logging

logger = logging.getLogger()

def request_saramin_job_data(access_key, job_cd, published, count, start=0):
    url = "https://oapi.saramin.co.kr/job-search"
    
    headers = {
        "Accept": "application/json"
    }
    
    params = {
        "access-key": access_key,
        "job_cd": job_cd,
        "fields": "expiration-date,count",
        "published": published,
        "start": start,
        "count": count,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e


def get_entry_level_job_data(access_key, job_cd, published):
    entry_level_jobs  = []
    start = 0
    count = 110

    while True:
        data = request_saramin_job_data(access_key, job_cd, published, count, start)
        jobs = data['jobs']['job']
        
        filtered_jobs = [job for job in jobs if job['position']['experience-level']['code'] in [1, 3]]
        entry_level_jobs.extend(filtered_jobs)
        
        total = int(data['jobs']['total'])
        if start + count >= total:
            break
        
        start += count

    return entry_level_jobs