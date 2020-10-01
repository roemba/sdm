

class Member:
    """
    A regular Member can only access their own information in the StorageServer.
    """

    def __init__(self):
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
        This is the method DatEnc(R, PK_s, SK_g[, I_R]) defined in the paper.
        :param raw_data:
        :return:
        """
        pass

    def prepare_decryption_request(self):
        pass
