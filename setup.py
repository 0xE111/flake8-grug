import setuptools

requires = [
    "flake8 > 4.0.0",
]

flake8_entry_point = 'flake8.extension'

setuptools.setup(
    name="flake8_grug",
    license="MIT",
    version="0.1.0",
    description="Grug's extension to flake8",
    author="Grug",
    author_email="misterksn@gmail.com",
    url="https://github.com/c0ntribut0r/flake8-grug.git",
    packages=[
        "flake8_grug",
    ],
    install_requires=requires,
    entry_points={
        'flake8.extension': [
            'GRG = flake8_grug:Plugin',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)