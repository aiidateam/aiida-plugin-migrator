import setuptools

setuptools.setup(
    name="aiida-plugin-migrator",
    license="MIT",
    version="0.1.0",
    description="Formatter for AiiDA plugins",
    author="The AiiDA team",
    author_email="developers@aiida.net",
    url="https://github.com/aiidateam/aiida-plugin-migrator",
    scripts = [ "aiida-plugin-migrator.py" ],
    install_requires= [
        'bowler',
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
