# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-logger",
    version="0.0.1",
    description="python 日志包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 仓库地址
    url="http://maven.abc.com/repository/pypi-group/",
    # repository = '',
    # project_urls={
    #     "Bug Tracker": "",
    # },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    package_dir={"py-logger": "src"},
    packages=setuptools.find_packages(where="src", include = ['src']),
    python_requires=">=3.11",
    install_requires=[
        # "nacos-sdk-python==0.1.12"
    ],
)