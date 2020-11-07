# Say hello to your Personal Privacy-Preserving Financial Consultant!
How can we be of service to you today?

## Installation
It is generally recommended installing your Python packages in a Virtual Environment (venv).

### Ubuntu
The following packages are necessary to install `petlib`.
- Install python-dev: `sudo apt-get install python3.8-dev`
- Install libssl-dev: `sudo apt-get install libssl-dev`
- Install libffi-dev: `sudo apt-get install libffi-dev`

### Proxy re-encryption
This implementation is based on a method outlined in *Shared and Searchable Encrypted Data for Untrusted Servers* by Changyu Dong, Giovanni Russello, and Naranker Dulay. It uses RSA as the encryption for a multi reader/multi writer sytem. For access control we define 
