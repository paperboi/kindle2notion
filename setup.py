from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

with open("requirements-dev.txt", "r", encoding="utf-8") as f:
    requirements_dev = f.read()

setup(
    name="kindle2notion",
    version="1.0.2",
    author="Jeffrey Jacob",
    author_email="jeffreysamjacob@gmail.com",
    description="Export all the clippings from your Kindle device to a database in Notion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paperboi/kindle2notion",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "kindle2notion = kindle2notion.__main__:main",
        ],
    },
)
