# README

## Requirements

* Python 3
* pip
* virtualenvwrapper (optional)

## Configuration

See the `config.py` file

## Setup

Initialize the test environment. A `tokens` table was added
to the original DB schema so an existing environment won't do.
See [this issue](https://github.com/code-check/sample-test/issues/1)

Optionally, create the virtual environment
```sh
mkvirtualenv -p `which python3` gitech
```
Install requirements
```sh
pip install -r requirements.txt
```
Start up server
```sh
python server.py
```