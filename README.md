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
