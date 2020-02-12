"""tug-overlap-checker - setup.py"""
import setuptools

LONG_DESC = open('README.md').read()

setuptools.setup(
    name="tug-overlap-checker",
    version="0.1.2",
    author="Lorenz Leitner",
    author_email="lrnz.ltnr@gmail.com",
    description="Check for course overlaps at Graz University of Technology",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    url="https://github.com/lolei/tug-overlap-checker",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["tug_overlap_checker"],
    entry_points={"console_scripts": ["tug-overlap-checker=tug_overlap_checker.tug_overlap_checker:main"]},
    python_requires=">=3",
    install_requires=[
        'bs4',
        'selenium'
    ]
    )
