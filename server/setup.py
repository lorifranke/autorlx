from setuptools import setup, find_packages


setup(
    name='AutoRL X Server',
    version='0.1.0',
    author="Loraine Franke",
    description="REST API for AutoRL X",
    url="",
    python_requires='>=3.8',
    packages=find_packages(
        where='.'
    ),
    install_requires=[
        "fastapi==0.92.0",
        "websockets==10.4",
        "fastparquet==2023.2.0",
        "uvicorn==0.19.0",
        "pydantic==1.10.12",
        "requests==2.28.1",
        "email-validator==2.0.0.post2",
        "pymysql==1.1.0",
        "cryptography==41.0.4",
        "arlo"
    ]
)
