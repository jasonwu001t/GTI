from setuptools import setup, find_packages

setup(
    name="GTI",
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A unified library for data analytics, broker APIs, and GenAI",
    # long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/GTI",
    packages=find_packages(include=["GTI", "GTI.*"]),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "statsmodels",
        "plotly",
        "requests",
        "psycopg2-binary",
        "mysql-connector-python",
        "boto3",
        "ib_insync",
        "alpaca-py",
        "fredapi",
        "flask"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['*.ini'],
    },
    python_requires=">=3.6",
)



"""
After code update, update setup.py version, and install_required

Build the package: 
python setup.py sdist bdist_wheel

Install/reinstall the package locally: 
pip install .

update the package use: 
pip install -e .
or pip install --upgrade .

"""