from setuptools import find_packages,setup

setup(
    name='mcqgen',
    version='0.0.1',
    author='athira',
    author_email='athirapt998@gmail.com',
    install_requires=[
    "langchain==1.2.13",
    "langchain-community==0.4.1",
    "langchain-core==1.2.22",
    "langchain-groq==1.1.2",
    "streamlit",
    "python-dotenv",
    "PyPDF2"
],
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)