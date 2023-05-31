from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path):
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n",'') for req in requirements]
    
    return requirements


setup(
     
      name='Diamond_Price_Prediction',
      version='0.0.1',
      author='Aman_Vishwakarma',
      author_email="amansharma1729ds@gmail.com",
      install_requires=get_requirements(),
      packages=find_packages()

)