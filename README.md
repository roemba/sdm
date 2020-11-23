# Encrypted Search in a Cloud Database for Financial Consulting
This is an implementation and demonstration of a searchable encryption that prioritizes speed over hiding some
properties, such as the size of the documents and the number of search results.

**This is a proof of concept and should not be used in actual production environments.**

## Installation
It is generally recommended installing your Python packages in a Virtual Environment (`venv`).

### Ubuntu
The following packages are necessary to install `petlib`.
- Install python-dev: `sudo apt-get install python3.8-dev`
- Install libssl-dev: `sudo apt-get install libssl-dev`
- Install libffi-dev: `sudo apt-get install libffi-dev`

## Structure
The methods are logically divided over `client.py`, `consultant.py` and `storage.py`.
Common cryptographic functions and data representations are in `models.py`.
Finally, protocols for setup, uploading and searching are in `protocols.py`

## Demonstration
The file `demo.py` is a Python script that starts a Graphical User Interface to play around with the implementation.
In the `/examples` folder there are some simple text files that can be used for this purpose.
It is important to note that keywords are now extracted automatically from the files, but of course for an image file it
would make more sense to insert custom keywords.
