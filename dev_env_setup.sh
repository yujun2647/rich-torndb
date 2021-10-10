#!/bin/bash

function init_dev_python_env() {
  if [ ! -d "./venv" ]; then
    python3 -m venv ./venv
  fi
  ./venv/bin/python -m pip install -U pip
  ./venv/bin/python -m pip install -U -r requirements.txt \
      --index-url=http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
}


function init_mysql_db_env(){
  echo "destroy all container in docker-compose"
  docker-compose -f dev_env/docker-compose.yml down
  
  echo "rebuild all images in docker-compose"
  docker-compose -f dev_env/docker-compose.yml build
  
  echo "restart all container in docker-compose"
  docker-compose -f dev_env/docker-compose.yml up &
}

init_dev_python_env
init_mysql_db_env