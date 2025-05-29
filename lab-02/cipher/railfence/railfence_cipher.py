class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 0:
            raise ValueError("Number of rails must be positive")
        if num_rails == 1:
            return plain_text

        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up

        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 0:
            raise ValueError("Number of rails must be positive")
        if num_rails == 1:
            return cipher_text

        # Bước 1: Tính độ dài của từng rail
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Bước 2: Phân chia cipher_text thành các rails
        rails = []  # Khởi tạo rails mà không có danh sách rỗng ban đầu
        start = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length

        # Bước 3: Đọc lại các ký tự theo thứ tự mã hóa
        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            if rails[rail_index]:  # Kiểm tra xem rails[rail_index] có rỗng không
                plain_text += rails[rail_index].pop(0)  # Lấy và xóa ký tự đầu tiên
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plain_text