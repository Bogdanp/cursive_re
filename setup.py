import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel("README.md")) as f:
    long_description = f.read()


with open(rel("cursive_re", "__init__.py"), "r") as f:
    version_marker = "__version__ = "
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip('"')
            break
    else:
        raise RuntimeError("Version marker not found.")


dependencies = []
extra_dependencies = {}
extra_dependencies["dev"] = [
    # Linting
    "flake8",
    "flake8-bugbear",
    "flake8-quotes",
    "isort",

    # Misc
    "bumpversion",
    "mypy",
    "twine",

    # Testing
    "pytest",
    "pytest-cov",
]

setup(
    name="cursive_re",
    version=version,
    author="Bogdan Popa",
    author_email="bogdan@defn.io",
    description="Beautiful regular expressions for Python 3.6 and up.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["cursive_re"],
    include_package_data=True,
    install_requires=dependencies,
    python_requires=">=3.6",
    extras_require=extra_dependencies,
)
