#use to create a proper package for this project.
from setuptools import find_packages,setup
from typing import List
#defining the function reponsible for install requirement file
def get_requirement_file()->List[str]:
    '''
        Responsible to read all library names from txt file
    '''
    with open("requirements.txt","r") as f:
        return f.readlines().remove('-e .')




setup(
    name="sensor",
    version="0.0.2",
    author="Tanmay",
    author_email="chakrabortytanmay326@gmail.com",
    packages=find_packages(),
    install_requires=get_requirement_file(),
)








