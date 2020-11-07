# Say hello to your Personal Privacy-Preserving Financial Consultant!
How can we be of service to you today?

## Installation
It is generally recommended installing your Python packages in a Virtual Environment (venv).

### Ubuntu
The following packages are necessary for `bplib` and thereby `petlib` to install.
- Install python-dev: `sudo apt-get install python3.8-dev`
- Install libssl-dev: `sudo apt-get install libssl-dev`
- Install libffi-dev: `sudo apt-get install libffi-dev`

I got an error installing the Python packages recursively (using `pip install -r requirements.txt`).
Instead you can install the packages separately:
- Make sure you are in your venv when running: `pip install petlib`
- Again in your venv: `pip install bplib`

## Methods defined in the paper
### Certificate
- MemChk: `verify`

### Member
- IndGen: `_build_index`
    - BuildIndex
- DatEnc: `_encrypt_data`
- MakTrp: `make_trapdoor`
    - Trapdoor
- DatAux: `prepare_decryption_request`
- MemDct: `decrypt_data`

### Consultant (also a Member)
- SysSet: `setup_system`
- GrpAut: `authenticate_group`
- GDcKey (uses MemChk): `request_decryption_keys`
- ~~MemJon~~
- ~~MemLev~~

### StorageServer
- SrhInd (uses MemChk): `search`
    - Test
