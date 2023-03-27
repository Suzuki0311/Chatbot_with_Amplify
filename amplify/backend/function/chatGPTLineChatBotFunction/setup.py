# from distutils.core import setup

# setup(name='src', version='1.0')

from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1",
    packages=find_packages(where='amplify/backend/function/chatGPTLineChatBotFunction/src'),
    package_dir={'': 'amplify/backend/function/chatGPTLineChatBotFunction/src'},
)
