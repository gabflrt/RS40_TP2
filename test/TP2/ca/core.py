from tools.core import Configuration, generate_private_key, generate_public_key, sign_csr

# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""


class CertificateAuthority:

    def __init__(self, config: Configuration, password: str, private_key_filename: str, public_key_filename: str):
        self._config = config
        self._private_key = generate_private_key(private_key_filename, password)
        self._public_key = generate_public_key(self._private_key, public_key_filename, config)
        self._private_key_filename = private_key_filename
        self._public_key_filename = public_key_filename
        self._password = password

    def sign(self, csr, certificate_filename: str):
        sign_csr(csr, self._public_key, self._private_key, certificate_filename)
