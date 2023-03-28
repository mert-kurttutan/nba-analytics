# Predicting NBA Match Results

This project consists of 3 main parts:

1. ETL
2. ML Model & Training
3. Web Application

Tech Stack:

- Pytorch
- Apache Airflow (Workflow Automation)
- AWS (ECS, Lambda, S3, Dynamo DB)
- Github Actions (for CI)
- FastAPI



# TODO List:
- Complete the User component
- Write a more secure way to verify api_key, using the principles here: https://www.reddit.com/r/FastAPI/comments/zid4rj/fastapi_api_authentication_key_security/



# How to run:

```bash
sudo docker compose --env-file confidential.env --profile frontend-dev up --build --attach-dependencies
```