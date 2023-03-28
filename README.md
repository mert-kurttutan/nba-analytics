# Predicting NBA Match Results

This project consists of 3 main parts:

1. ETL
2. ML Model & Training
3. Web Application

Tech Stack:

- Pytorch
- FastAPI (Backend)
- Apache Airflow (Workflow Automation)
- Postgresql
- AWS (ECS, Lambda, S3)
- Github Actions (for CI)


## ETL
The etl pipeline uses apache airflow and AWS S3, ECS, proxy rotation.

The endpoint from which the data is extracted `nbastats.com`, which is banned for IPs that belong the Cloud providers, e.g. AWS. To overcome this obstacle, I used the around 5-10 different proxies from a Russia-based proxy provider, (other us or europe based ones did not work for my case.)

This is beneficial for 2 reasons
1. Without proxy, endpoint is not reachalbe at all due to above reasons
2. Having multiple proxies with proxy rotation prevents from getting rate-limited


Workings of ETL project
Apache airflow dag, and how it is used with ECS fargate



## Training
For training, I use pytorch, and XGBoost. For logging and version control, I use wandb. Logs of experiments will be soon made public

More model details

## Web app
Web app consists of 2 parts: Backend and Frontend

Through webapp, one can collect various stat, and get inference on match results

### Backend
The backend is written with FASTAPI

Documentation of Backend


### Frontend
To be written in Next.js


# How to run:

```bash
sudo docker compose --env-file confidential.env --profile frontend-dev up --build --attach-dependencies
```


# TODO List:
- Complete the User component
- Write a more secure way to verify api_key, using the principles here: https://www.reddit.com/r/FastAPI/comments/zid4rj/fastapi_api_authentication_key_security/



