from setuptools import find_packages, setup

# Set the package metadata
setup(
    name="FastJinja2Templates",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Shuaib Mohammad",
    author_email="smartexpert@users.noreply.github.com",
    description="A templating package for FastAPI using Jinja2 templates.",
    install_requires=["fastapi", "jinja2"],
)
