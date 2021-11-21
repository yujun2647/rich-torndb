#!/bin/sh
FEED_NAME="pypi"
REPOSITORY="https://upload.pypi.org/legacy/"
TOKEN=$(sed -n 1p ./pypi_token)

if [ ! -d "./venv" ]; then
  python3 -m venv ./venv
fi

./venv/bin/python -m pip install -U pip
./venv/bin/python -m pip install -U build twine \
    --index-url=http://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com

# 清理本地历史版本缓存
if [ -d "./dist" ]; then
  rm -r ./dist
fi
# 打包
./venv/bin/python -m build

# 准备上传配置
(
cat << EOF
[distutils]
Index-servers=
  $FEED_NAME

[$FEED_NAME]
Repository = $REPOSITORY
username = __token__
password = $TOKEN
EOF
) > ~/.pypirc

# 上传
python -m twine upload -r "$FEED_NAME" ./dist/*
