import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="structor",
    version="1.0.3",
    author="Mayas Nova",
    author_email="test@test.com",
    description="Simple package that allow you to create templates of folders/files structure and generate them from a cli (like done in angular, django, react...)",
    install_requires=[
        "click>=8.1.3",
        "colorama>=0.4.6",
        "commonmark>=0.9.1",
        "Pygments>=2.14.0",
        "PyYAML>=6.0",
        "rich>=12.6.0",
        "shellingham>=1.5.0.post1",
        "typer>=0.7.0"
    ],
    keywords=["structor", "file generator"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MayasMess/structor",
    project_urls={
        "Bug Tracker": "https://github.com/MayasMess/structor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['structor=structor.structor:main'],
    }
)
