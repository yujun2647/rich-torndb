from setuptools import setup

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
    install_requires=["tqdm~=4.62.2",
                      "pymysql~=1.0.2"]
)
