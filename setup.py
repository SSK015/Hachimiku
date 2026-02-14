import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hachimiku",
    version="1.0.0",
    author="ssk015",
    author_email="yenwenshare@gmail.com",
    description="An academic-first Python plotting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssk015/hachimiku",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
    ],
)
