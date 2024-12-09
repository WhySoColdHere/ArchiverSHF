from Archiver.Archiver import Archiver
from os import path


class EncoderSHF(Archiver):
    def __init__(self, filename: str):
        super().__init__(filename)

        self._output_filename = ''.join(self._input_filename.split('.')[:-1]) + ".bin"
        self._original_text = self._get_text_from_file(self._input_filename)
        self._symbols_codes, self._encoded_text = self._encode_text()

        self._write_binary_file(self._output_filename, self._symbols_codes, self._encoded_text)

    def get_texts(self):
        return self._original_text, self._encoded_text

    def get_filenames(self):
        return ''.join(self._input_filename.split('/')[-1]), ''.join(self._output_filename.split('/')[-1])

    def get_file_sizes(self):
        return path.getsize(self._input_filename), path.getsize(self._output_filename)

    def _shannon_fano(self, symbols):
        if len(symbols) == 1:
            return {symbols[0][0]: "0"}

        total = sum(weight for _, weight in symbols)
        cumulative_weight = 0
        split_point = 0
        for i in range(len(symbols)):
            cumulative_weight += symbols[i][1]
            if cumulative_weight >= total / 2:
                split_point = i
                break

        left = symbols[:split_point + 1]
        right = symbols[split_point + 1:]

        left_codes = self._shannon_fano(left)
        right_codes = self._shannon_fano(right)

        codes = {}
        for symbol in left_codes:
            codes[symbol] = '0' + left_codes[symbol]
        for symbol in right_codes:
            codes[symbol] = '1' + right_codes[symbol]

        return codes

    def _encode_text(self):
        # Подсчитаем частоту символов
        freq = {}
        for char in self._original_text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1

        # Сортируем символы по убыванию частоты
        symbols = sorted(freq.items(), key=lambda x: x[1], reverse=True)

        # Строим словарь кодов
        codes = self._shannon_fano(symbols)

        # Кодируем текст
        encoded_text = ''.join(codes[char] for char in self._original_text)

        return codes, encoded_text

    @staticmethod
    def _write_binary_file(filename, codes, encoded_text):
        with open(filename, "wb") as f:
            import json
            f.write(json.dumps(codes).encode() + b'\n')

            # Запись длины закодированного текста
            f.write(len(encoded_text).to_bytes(4, byteorder='big'))

            # Запись закодированного текста (улучшенная)
            num_bytes = (len(encoded_text) + 7) // 8
            binary_data = int(encoded_text, 2).to_bytes(num_bytes, byteorder='big')
            f.write(binary_data)

    @staticmethod
    def _get_text_from_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
