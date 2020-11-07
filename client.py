from petlib.bn import Bn


class Client:

    def __init__(self, id: Bn):
        """
        Should call user key setup to create a key pair of the user
        """
        self._id = id

        self._e = None
        self._d = None

    @property
    def id(self):
        return self._id

    def assign_partial_key(self, partial_key: (Bn, Bn)):
        self._e, self._d = partial_key

    def data_encryption(self, plaintext, search_keywords):
        """
        input: plaintext to be encrypted and a set of searching keyword for that document
        output: success maybe?
        
        The  encryption is done using a symmetric encryption algorithm  E.
        The user chooses a key K_x (for each plaintext) uniformally randomly 
        from the key space ef E to encrypt the plaintext.
        c_1 = E_{k_x}(plaintext_x) - plaintext encrypted under k_x using E
        c_2 = (K_x)^e_i1 - key chosen encrypted under RSA

        The user computes a hash value for each search keyword w_m and sigma_wm = H(W_m)
        c_wm = (sigma_wm)^e_i1 hash encrypted under RSA encryption and sends to the server
        """

    def data_decrypt(self, ciphertext):
        """
        input is the ciphertext extracted from the server for every plaintext item 
              after proxy re-decryption c_1, c_2'
        output: plaintext

        User computs (c_2')^d_i1 ) = (K_x)^{ed} = K_x. Using K_x the user can decrypt the document
        plaintext = {E_{k_x}}^-1(c_1) (because encryption is symmetric so it needs to have an inverse function)
        """

    def user_keyword_search(self, keyword):
        """
        intput: keyword the user wants to search for
        output: Encrypted documents which containt the keyword

        user computes the Hash of the keyword sigma = H(W) an encryptes Q = sigma^{e_j2}. User sends Q to server
        """
