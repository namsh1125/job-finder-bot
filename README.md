# job-finder-bot
사람인에 오늘 올라온 따끈따끈한 채용 공고를 슬랙 채널에서 받아보세요.

## 사전 준비 사항
서비스를 사용하기 위해 아래의 사항이 필요합니다.
- AWS 계정 및 `Python Requests 라이브러리`를 사용할 수 있는 `Lambda layer`
- 사람인 API Key
- Slack Webhook URL

## 사용 방법

### 1. AWS Lambda 함수 생성하기
- AWS Console에서 Lambda 서비스로 이동합니다.
- 함수 생성을 클릭합니다.
- 런타임으로 `Python 3.12`를 선택합니다.


### 2. 코드 업로드
- [code](./code) 폴더의 내용을 zip 파일로 압축합니다.
- 생성된 Lambda 함수에 zip 파일을 업로드합니다.


### 3. AWS Secret Manager 설정
다음 정보를 Secret Manager에 JSON 형식으로 저장합니다:
- 사람인 API Key
- 관심 있는 채용 공고 정보 (직무 코드, 직무 명, Slack Webhook URL)


#### Secret JSON 예시:
```json
{
   "saramin_api_key":"{YOUR_SARAMIN_API_KEY}",
   "job_info": {
      "84": {
        "name": "백엔드/서버개발",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      },
      "92": {
        "name": "프론트엔드",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      },
      "127": {
        "name": "인프라",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      },
      "146": {
        "name": "DevOps",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      },
      "277": {
        "name": "React",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      },
      "292": {
        "name": "SpringBoot",
        "webhook_url": "{YOUR_SLACK_WEBHOOK_URL}"
      }
   }
}
```
참고) [사람인 IT개발·데이터 코드표](https://oapi.saramin.co.kr/guide/code-table5?mcode=2)

### 4. Lambda 함수 설정
- 위에서 생성한 Secret Manager 정보를 아래 `환경 변수`로 추가합니다:
  - `REGION_NAME`: Secret Manager AWS 리전 (예: ap-northeast-2)
  - `SECRET_NAME`: Secret Manager에 저장한 시크릿 이름


- Lambda 함수의 실행 역할에 다음 `권한`을 추가합니다:
  - `SecretsManagerReadWrite`: Secret Manager에서 정보를 읽기 위한 권한


- Python Requests 라이브러리를 사용할 수 있는 `Lambda Layer`를 추가합니다.


- 함수의 `실행 시간`을 적절히 설정합니다.
  - 권장 설정: 최소 `15`초 이상
  - 참고) 6개 직무 정보 작업 시 약 10초가 소요됩니다.


### 5. Lambda 함수 트리거 설정
- 트리거 유형으로 `CloudWatch Events/EventBridge`를 선택합니다.
- 새 규칙을 생성합니다:
   - 규칙 유형: 스케줄 표현식
   - 스케줄 표현식: `cron(0 15 * * ? *)`
      - 의미: 매일 UTC 15:00 (한국 시간 00:00) 에 실행

> 참고: 시간대 설정에 주의하세요. AWS Lambda는 기본적으로 UTC 시간을 사용합니다.
