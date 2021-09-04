from setuptools import setup
from fake_traffic import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fake_traffic",
    version=__version__,
    author="deedy5",
    author_email="deedy-ru@ya.ru",
    description="Imitating an Internet user by mimicking popular web traffic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deedy5/fake_traffic",
    license="MIT",
    py_modules=["fake_traffic"],
    install_requires=["requests>=2.26.0",
                      "lxml>=4.6.3",
                      "google_trends>=1.0",
                      "duckduckgo_search>=0.6",
                      "google_searching>=0.2"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
