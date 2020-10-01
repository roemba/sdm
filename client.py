

class Client:
    """
    A Client can only access their own information in the StorageServer.
    """

    def __init__(self):
        self._public_key = None
        self._secret_key = None
