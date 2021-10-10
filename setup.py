from typing import *
from setuptools import setup


def get_requirements() -> List[str]:
    with open("requirements.txt") as fp:
        lines = fp.readlines()
        lines = list(filter(lambda l: not l.startswith("#"), lines))
        for i, line in enumerate(lines):
            if line.endswith("\n"):
                lines[i] = line[:-1]
        return lines


setup(
    name="rich-torndb",
    version="0.0.1",
    author="walkerjun",
    author_email="yujun2647@163.com",
    description='More wrapper base on torndb',
    license='MulanPSL-2.0',
    url='https://gitee.com/walkerjun/rich-torndb',

    python_requires='>=3.6',
    include_package_data=True,
    packages=["rich_torndb",
              "rich_torndb/utils"],
    install_requires=get_requirements()
)

if __name__ == "__main__":
    get_requirements()
