from setuptools import setup, find_packages
import os
import shutil

# Create package data directories if they don't exist
os.makedirs('clients/python/tanzo_schema/schema', exist_ok=True)

# Copy schema files to the package data directory
shutil.copy('spec/tanzo-schema.json', 'clients/python/tanzo_schema/schema/tanzo-schema.json')

# Copy example profiles to tests directory for test discovery
os.makedirs('tests/test_data', exist_ok=True)
for example_file in ['examples/Kai_profile.yaml', 'examples/digital_archetype_only.yaml', 'examples/Hermit_profile.yaml']:
    if os.path.exists(example_file):
        shutil.copy(example_file, f"tests/test_data/{os.path.basename(example_file)}")

setup(
    name="tanzo-schema",
    version="0.1.0",
    description="TanzoLang - Schema specification and tools for the Tomodaichi Tanzo ecosystem",
    author="Onalius Team",
    author_email="info@onalius.com",
    url="https://github.com/onalius/tanzo-lang-core",
    packages=find_packages(include=["tanzo_schema", "tanzo_schema.*", "cli", "cli.*"]),
    package_dir={
        "tanzo_schema": "clients/python/tanzo_schema",
        "cli": "cli"
    },
    package_data={
        "tanzo_schema": ["schema/*.json", "schema/*.yaml"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tanzo-cli=cli.tanzo_cli:cli",
            "tanzo_cli=cli.tanzo_cli:cli",
        ],
    },
    python_requires=">=3.11",
    install_requires=[
        "pydantic>=1.10,<2.0",  # Pin to <2.0 to avoid API changes
        "jsonschema>=4.19.0",
        "pyyaml>=6.0.1",
        "numpy>=1.25.0",
        "click>=8.1.6",
        "annotated-types>=0.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
            "ruff>=0.0.285",
            "pre-commit>=3.4",
            "mkdocs-material>=9.1.21",
            "mkdocstrings>=0.22.0",
            "mkdocstrings-python>=1.1.2",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
)