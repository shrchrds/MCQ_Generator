from setuptools import find_packages, setup

setup(
    name='MCQ_Gen',
    version='1.0.0',
    author='Shivanand Ekatpure',
    author_email='datasnekatpure@gmail.com',
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages()
)