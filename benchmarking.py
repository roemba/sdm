from typing import Union
from bplib.bp import G1Elem, G2Elem


class BandwidthCounter:

    def __init__(self):
        self._http_bits = 0
        self._https_bits = 0

    supported_types = Union[G1Elem, G2Elem]

    def _extract_bandwidth(self, data: supported_types):
        if isinstance(data, (G1Elem, G2Elem)):
            return len(data.export()) * 8

        raise Exception(f"There is no implementation yet to extract the bandwidth for type {type(data)}")

    def send_http(self, data: supported_types):
        self._http_bits += self._extract_bandwidth(data)

    def send_https(self, data: supported_types):
        self._https_bits += self._extract_bandwidth(data)

    @property
    def http_bits(self) -> int:
        return self._http_bits

    @property
    def https_bits(self) -> int:
        return self._https_bits
