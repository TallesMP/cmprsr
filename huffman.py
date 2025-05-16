import pickle


class Node:
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index].freq < self.heap[parent].freq:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
            smallest = left
        if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)


class HuffmanCompressor:
    def __init__(self, filename=None, compressed_filename="compressed.bin"):
        self.filename = filename
        self.compressed_filename = compressed_filename
        self.text = self._read_file() if filename else None
        self.root = None
        self.code_map = {}
        self.compressed_data = None

    def _read_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            return file.read()

    def _count_chars(self):
        freq = {}
        for char in self.text:
            freq[char] = freq.get(char, 0) + 1
        return freq

    def build_huffman_tree(self):
        freq_map = self._count_chars()
        heap = MinHeap()

        for char, freq in freq_map.items():
            heap.insert(Node(char=char, freq=freq))

        while len(heap.heap) > 1:
            left = heap.pop()
            right = heap.pop()
            heap.insert(Node(left=left, right=right,
                        freq=left.freq + right.freq))

        self.root = heap.pop()

    def generate_codes(self, node=None, prefix=""):
        if node is None:
            node = self.root

        if node.is_leaf():
            self.code_map[node.char] = prefix
        else:
            self.generate_codes(node.left, prefix + "0")
            self.generate_codes(node.right, prefix + "1")

    def encode_text(self):
        return "".join(self.code_map[char] for char in self.text)

    def save_compressed_file(self):
        encoded_text = self.encode_text()

        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte_segment = encoded_text[i:i+8]
            byte_array.append(int(byte_segment.ljust(8, "0"), 2))

        with open(self.compressed_filename, "wb") as file:
            pickle.dump({"code_map": self.code_map,
                        "compressed_data": bytes(byte_array)}, file)

        print(f"Arquivo compactado salvo em '{self.compressed_filename}'")

    def compress(self):
        self.build_huffman_tree()
        self.generate_codes()
        self.save_compressed_file()
        print("Compressão concluída!")

    def load_compressed_file(self):
        with open(self.compressed_filename, "rb") as file:
            data = pickle.load(file)
            self.code_map = data["code_map"]
            self.compressed_data = data["compressed_data"]
        print(f"Arquivo compactado '{self.compressed_filename}' carregado")

    def decode_text(self):
        binary_string = "".join(f"{byte:08b}" for byte in self.compressed_data)

        reverse_code_map = {v: k for k, v in self.code_map.items()}

        decoded_text = ""
        temp_code = ""

        for bit in binary_string:
            temp_code += bit
            if temp_code in reverse_code_map:
                decoded_text += reverse_code_map[temp_code]
                temp_code = ""

        return decoded_text

    def decompress(self, output_filename="decompressed.txt"):
        self.load_compressed_file()
        original_text = self.decode_text()

        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(original_text)

        print(f"Arquivo descompactado salvo como '{output_filename}'")
