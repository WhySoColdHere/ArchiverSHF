from Archiver.Archiver import Archiver
from os import path


class DecoderSHF(Archiver):
    def __init__(self, filename: str):
        super().__init__(filename)

        self._output_filename = ''.join(self._input_filename.split('.')[:-1]) + "_decoded" + '.txt'
        self._encoded_text, self._decoded_text = self._decode_binary_file(self._input_filename)

        self._write_file(self._output_filename, self._decoded_text)

    def get_texts(self):
        return self._encoded_text, self._decoded_text

    def get_filenames(self):
        return ''.join(self._input_filename.split('/')[-1]), ''.join(self._output_filename.split('/')[-1])

    def get_file_sizes(self):
        return path.getsize(self._input_filename), path.getsize(self._output_filename)

    @staticmethod
    def _decode_binary_file(filename):
        with open(filename, "rb") as f:
            import json
            codes_json = f.readline().decode()
            codes = json.loads(codes_json)

            # Чтение длины закодированного текста
            length_bytes = f.read(4)
            n = int.from_bytes(length_bytes, byteorder='big')

            num_bytes = (n + 7) // 8
            binary_data = f.read(num_bytes)
            encoded_text = bin(int.from_bytes(binary_data, byteorder='big'))[2:].zfill(n)

            decoded_text = ""
            current_code = ""
            reverse_codes = {code: symbol for symbol, code in codes.items()}  # Создаем обратный словарь

            for bit in encoded_text:
                current_code += bit
                if current_code in reverse_codes:
                    decoded_text += reverse_codes[current_code]
                    current_code = ""

            return encoded_text, decoded_text

    @staticmethod
    def _write_file(filename, text):
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(text)
