from setuptools import setup, find_packages

setup(
    name="openai-sdk",
    version="0.1",
    packages=["agents", "my_agents", "my_config", "my_tools"],
    install_requires=[
        "streamlit",
        "requests",
        "beautifulsoup4",
        # any other packages you use
    ],
)
