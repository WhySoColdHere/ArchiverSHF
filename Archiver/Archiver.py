from .EncodeSHF import EncodeSHF
from .DecodeSHF import DecodeSHF


class Archiver:

    @staticmethod
    def encode_shf(filename):
        encode_shf = EncodeSHF(filename)
        return encode_shf.get_texts()

    @staticmethod
    def decode_shf(filename):
        decode_shf = DecodeSHF(filename)
        return decode_shf.get_texts()


