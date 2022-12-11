from setuptools import find_packages, setup

# Set the package metadata
setup(
    name="fastapi_jinja2_templates",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Shuaib Mohammad",
    author_email="smartexpert@users.noreply.github.com",
    description="A package for using Jinja2 templates with FastAPI",
    long_description="A convenient and intuitive way to use Jinja2 templates with FastAPI, with helpful debugging tools and the ability to globally inject custom functions.",
    long_description_content_type="text/markdown",
    url="https://github.com/smartexpert/fastapi_jinja2_templates",
    install_requires=["fastapi>=0.88.0", "jinja2>=3.1.2"],
)
