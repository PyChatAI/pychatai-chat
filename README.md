# PyChatAI

![PyChatAI logo](assets/favicon.png)

PyChatAI is a Python package that allows you to create your own chat app, using different LLM models and plugins.

## Getting the code

To get the code, it is recommended to use [Git](https://git-scm.com/). You can then clone the repository with the following command:

```bash
git clone https://github.com/PyChatAI/pychatai-chat.git
```

## Installation

To use PyChatAI, you need Python 3.8 or higher.
First you will need to install packages. For this, you need to install [Poetry](https://python-poetry.org/).
Afterwards you can install the packages in the terminal with the following command in the root directory of the project (where the `pyproject.toml` file is located):

```bash
poetry install
```

(Alternatively, you can also install the packages with `pip install -r requirements.txt`).

## Usage

To start the app, you need to run the following command in the root directory of the project:

```bash
poetry run reflex run
```
