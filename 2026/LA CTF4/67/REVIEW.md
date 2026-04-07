# Review Bài Giải LA CTF4 - RSA Challenge

## Tổng Quan Thử Thách

Đây là một bài RSA với lỗ hổng bảo mật nghiêm trọng: các số nguyên tố `p` và `q` được tạo ra chỉ sử dụng các chữ số 6 và 7, và cả hai đều phải kết thúc bằng số 7.

### Phân Tích Lỗ Hổng

Xem xét hàm tạo số nguyên tố trong [chall.py](file:///d:/CTF/2026/LA%20CTF4/chall.py):

```python
def generate_67_prime(length: int) -> int:
    while True:
        digits = [secrets.choice("67") for _ in range(length - 1)]
        digits.append("7")
        test = int("".join(digits))
        if isPrime(test, false_positive_prob=1e-12):
            return test
```

**Vấn đề**: Mặc dù `p` và `q` dài 256 chữ số, nhưng mỗi chữ số chỉ có thể là 6 hoặc 7. Điều này giảm không gian tìm kiếm từ 10^256 xuống còn 2^256 khả năng - vẫn lớn nhưng có thể khai thác được bằng thuật toán thông minh.

## Các Phương Pháp Đã Thử

### 1. Meet-in-the-Middle Tham Lam (Thất Bại)
- **Ý tưởng**: Xây dựng `p` và `q` từng chữ số từ phải sang trái
- **Vấn đề**: Chọn sai ứng viên ở vị trí đầu → thất bại ở vị trí 14
- **Nguyên nhân**: Tại mỗi vị trí có thể có nhiều cặp (p, q) hợp lệ, chọn tham lam có thể dẫn vào ngõ cụt

### 2. Phân Tích Fermat (Quá Chậm)
- **Ý tưởng**: Tìm `a` và `b` sao cho `n = a² - b² = (a-b)(a+b)`
- **Vấn đề**: Phải duyệt quá nhiều số chỉ chứa 6 và 7 quanh sqrt(n)
- **Kết quả**: Không hoàn thành trong thời gian hợp lý

### 3. Breadth-First Search (Thành Công) ✓

## Giải Pháp Cuối Cùng: BFS

### Thuật Toán

```python
candidates = [(7, 7)]  # Bắt đầu với cả hai kết thúc bằng 7

for pos in range(1, 257):
    mod = 10 ** (pos + 1)
    new_candidates = []
    
    for p, q in candidates:
        for p_digit in [6, 7]:
            for q_digit in [6, 7]:
                test_p = p_digit * (10 ** pos) + p
                test_q = q_digit * (10 ** pos) + q
                
                # Kiểm tra (pos+1) chữ số cuối có khớp không
                if (test_p * test_q) % mod == n % mod:
                    new_candidates.append((test_p, test_q))
                    
                    if test_p * test_q == n:
                        # Tìm thấy!
                        return test_p, test_q
    
    candidates = new_candidates
```

### Điểm Mạnh

1. **Toàn diện**: Theo dõi TẤT CẢ các ứng viên hợp lệ, không bỏ sót
2. **Hiệu quả**: Sử dụng số học modular để kiểm tra nhanh
3. **Đúng đắn**: Đảm bảo tìm được nghiệm nếu nó tồn tại

### Độ Phức Tạp

- **Không gian**: Tối đa ~4 ứng viên tại mỗi vị trí (thực tế thường 2-4)
- **Thời gian**: O(256 × số_ứng viên × 4) ≈ O(256 × 4 × 4) = O(4096) phép toán chính
- **Thực tế**: Chạy trong ~30 giây

## Kết Quả

```
Found p and q at position 255!
p = 6666667677677776777767776667666667766767776676677776776677777776776777766676667677677676676666666767766766766777666776667677666767777767666777776777776677666666767766677776767766667777667766677676766667666677667667676776766666666677777777677776677767666767
q = 6667676767667677767667677767766766677766677766776767666677676776677777667676766676777766776777667677766666777677666766666766777776777777776766667767776677677767676767766666667667777767767666676767677676766677766767776676666767766766766676666666677777666777

Flag: lactf{wh4t_67s_15_blud_f4ct0r1ng_15_blud_31nst31n}
```

### Xác Minh

- ✓ Cả `p` và `q` đều là số nguyên tố 256 chữ số
- ✓ Chỉ chứa các chữ số 6 và 7
- ✓ Cả hai đều kết thúc bằng 7
- ✓ `p × q = n`

## Bài Học Rút Ra

### 1. Về Mật Mã Học
- **Không bao giờ** hạn chế không gian khóa một cách nhân tạo
- Entropy thấp trong việc tạo số nguyên tố = thảm họa bảo mật
- RSA an toàn khi `p` và `q` được chọn ngẫu nhiên hoàn toàn

### 2. Về Thuật Toán
- Tham lam không phải lúc nào cũng tối ưu
- BFS đảm bảo tìm được nghiệm tối ưu khi có nhiều đường đi
- Số học modular rất mạnh cho việc kiểm tra từng phần

### 3. Về Giải CTF
- Thử nhiều phương pháp khác nhau
- Phân tích tại sao một phương pháp thất bại
- Debug cẩn thận để hiểu vấn đề cốt lõi

## Đánh Giá

**Độ khó**: Trung bình - Khó  
**Kỹ năng cần thiết**: 
- Hiểu RSA cơ bản
- Tư duy thuật toán (BFS/DFS)
- Số học modular
- Kỹ năng debug

**Điểm hay**: Bài toán dạy được bài học quan trọng về entropy trong mật mã học và sự khác biệt giữa thuật toán tham lam vs. tìm kiếm toàn diện.

## Files

- [chall.py](file:///d:/CTF/2026/LA%20CTF4/chall.py) - Đề bài gốc
- [solve.py](file:///d:/CTF/2026/LA%20CTF4/solve.py) - Giải pháp BFS gọn gàng
- [solve_bfs.py](file:///d:/CTF/2026/LA%20CTF4/solve_bfs.py) - Phiên bản chi tiết với log tiến trình

---

**Flag**: `lactf{wh4t_67s_15_blud_f4ct0r1ng_15_blud_31nst31n}`
