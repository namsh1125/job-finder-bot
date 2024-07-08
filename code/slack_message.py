import requests

from saramin_utils import filter_and_format_location
from datetime import datetime, timezone, timedelta


def create_slack_message(date, jobs, job_info, job_cd):
    job_category = job_info.get(job_cd, {}).get('name', "기타")
    
    attachments = [{
        "color": "#36a64f",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{date} 올라온 {job_category} 채용 공고",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*총 {len(jobs)}개의 채용 공고가 있습니다.*"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }]

    for job in jobs:
        job_attachment = create_job_attachment(job)
        attachments.append(job_attachment)

    return {
        "attachments": attachments
    }


def create_job_attachment(job):
    company = job['company']['detail']
    company_name = company['name']
    company_url = company['href']
    
    job_url = job['url']
    job_type = job['position']['job-type']['name'].replace(',', ', ')
    salary = job['salary']['name']
    education = job['position']['required-education-level']['name']
    
    # Unix timestamp를 datetime 객체로 변환하고 한국 시간대로 조정
    expiration_timestamp = job['expiration-timestamp']
    expiration_date = datetime.fromtimestamp(int(expiration_timestamp), tz=timezone(timedelta(hours=9)))
    formatted_expiration_date = expiration_date.strftime('%Y-%m-%d %H:%M:%S')

    position = job['position']['title']
    job_code = job['position']['job-code']['name'].replace(',', ', ')
    location = filter_and_format_location(job['position']['location']['name'])

    return {
        "color": "#36a64f",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{position}*"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "공고 상세보기",
                        "emoji": True
                    },
                    "url": job_url
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*회사*\n<{company_url}|{company_name}>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*근무 위치*\n{location}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*근무 형태*\n{job_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*연봉*\n{salary}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*요구 학력*\n{education}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*마감일*\n{formatted_expiration_date}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*직무*\n{job_code}"
                }
            }
        ]
    }

def send_slack_message(webhook_url, message):
    response = requests.post(webhook_url, json=message)
    response.raise_for_status()