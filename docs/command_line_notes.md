# Shell commands used frequently

Built docker image

```Bash
 sudo docker build --tag nba-mlflow-dag:latest .
```

For interactive runtime of docker container, through bash

```Bash
 sudo docker run -it ${CONTAINER_IMAGE_NAME} /bin/bash
```


Authenticate for ecr public access

```Bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

```

Push image to public ecr repository

```Bash

docker tag nba-mlflow-dag:latest public.ecr.aws/w6w5s2w4/nba-ml

docker push public.ecr.aws/w6w5s2w4/nba-ml
```


Aws copy
```Bash

# Settings for bucket
BUCKET_NAME="mert-kurttutan-nba-ml-project-raw-data"
RAW_DATA_DIR="./raw_data"

aws s3 cp s3://$BUCKET_NAME/ $RAW_DATA_DIR --recursive

```



# Cheat Sheet for Imporant Bash Commands

In WSL, use this to start docker

```Bash
sudo service docker start
```

```Bash
sudo docker build --tag speech2text-azure:latest .
```

```Bash
sudo docker-compose up
```


pytest captures the stdout from individual tests and displays them only on certain conditions, along with the summary of the tests it prints by default.

Extra summary info can be shown using the '-r' option:

```Bash

pytest -rP
```

shows the captured output of passed tests.

```Bash
pytest -rx
```
shows the captured output of failed tests (default behaviour).

The formatting of the output is prettier with -r than with -s.