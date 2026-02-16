from setuptools import setup, find_packages

setup(
    name="lci-agent",
    version="0.1.0",
    description="Universal context infrastructure for AI applications",
    author="Rumiza Shaikh",
    author_email="your.email@example.com",
    url="https://github.com/rumiza-shaikh/lci-agent",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.39.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.32.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
