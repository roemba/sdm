from typing import List, Tuple


class Member:
    """
    A regular Member can only access their own information in the StorageServer.
    """

    def __init__(self):
        self.certificate = None
        self._public_key = None
        self._secret_key = None

    def build_data(self, raw_data: str):
        return self._encrypt_data(raw_data), self._build_index(raw_data)

    def _build_index(self, raw_data: str):
        """
        This is the method IndGen(R, PK_s, SK_g) defined in the paper.
        :param data:
        :return:
        """

    def _encrypt_data(self, raw_data: str):
        """
        This is the method DatEnc(R[, PK_s, SK_g, I_R]) defined in the paper.
        :param raw_data:
        :return:
        """
        pass

    def make_trapdoor(self, keywords: List[str]):
        """
        This is the MakTrp(L'[, PK_s, SK_g]) method defined in the paper.
        Creates a Trapdoor of the keyword list that represents a query.
        :param keywords: Keyword list
        """
        pass

    def prepare_decryption_request(self, data_count: int) -> List[Tuple]:
        """
        This is the DatAux(E(R)[, CT_i, PK_s]) method defined in the paper.
        Generates a number (data_count) of different one-time key pairs (auxiliary information) to send to the
        Consultant for a number of decryption keys.
        :param data_count: Number of pairs to generate
        :return: List of auxiliary information (U') and one-time secret keys (v)
        """
        pass

    def decrypt_data(self, data: List, decryption_keys: List, one_time_keys: List) -> List[str]:
        """
        This is the MemDct(E(R), D[, PK_s, SK_g], v) method defined in the paper.
        Decrypts a list of data items and returns the results (again as a list)
        :param data: Encrypted data received from the StorageServer
        :param decryption_keys: Decryption keys received from the Consultant
        :param one_time_keys: One-time secret keys (v) generated in `prepare_decryption_request`
        :return: List of decrypted (raw) data
        """
        results = []

        for ciphertext, decryption_key, one_time_key in zip(data, decryption_keys, one_time_keys):
            pass

        return results
