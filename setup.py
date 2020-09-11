from setuptools import setup
from distutils.sysconfig import get_python_lib

SITE_PACKAGES_PATH = get_python_lib()

setup(
    name="horror",
    version="0.0.36",
    packages=["horror"],
    description="Effortlessly segfault",
    author="Kaylynn Morgan",
    author_email="mkaylynn7@gmail.com",
    data_files=[(SITE_PACKAGES_PATH, ["horror.pth"])],
    install_requires=["parso"],
)
