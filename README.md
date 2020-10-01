## Methods defined in the paper
### Certificate
- MemChk: `verify`

### Member
- IndGen: `_build_index`
    - BuildIndex
- DatEnc: `_encrypt_data`
- MakTrp
    - Trapdoor
- MemDct
- DatAux: `prepare_decryption_request`

### Consultant (also a Member)
- SysSet: `setup_system`
- GrpAut: `authenticate_group`
- GDcKey (uses MemChk): `request_decryption_key`
- ~~MemJon~~
- ~~MemLev~~

### StorageServer
- SrhInd (uses MemChk): `search`
    - Test
