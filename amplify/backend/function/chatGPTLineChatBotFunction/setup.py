# from distutils.core import setup

# setup(name='src', version='1.0')

from setuptools import setup, find_packages
from setuptools import setup, find_namespace_packages

# setup(
#     name="my_package",
#     version="0.1",
#     packages=find_packages(where='amplify/backend/function/chatGPTLineChatBotFunction/src'),
#     package_dir={'': 'amplify/backend/function/chatGPTLineChatBotFunction/src'},
# )
# setup(
#     # ...
#     packages=find_namespace_packages(where='src'),
#     package_dir={"": "src"}
#     # ...
# )

setup(
    # ...
    packages=find_packages(
        where='src',
        include=['my_package*'],  # alternatively: `exclude=['additional*']`
    ),
    package_dir={"": "src"}
    # ...
)