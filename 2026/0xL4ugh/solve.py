import pwn
from Crypto.Util.number import bytes_to_long, getPrime
import math
import numpy as np
import string
import sys

# --- CẤU HÌNH ---
HOST = '124.197.22.141'  # Thay IP
PORT = 6665         # Thay Port
FLAG_LEN = 25
KNOWN_PREFIX = "VSL{"
KNOWN_SUFFIX = "}"
CHARSET = string.ascii_letters + string.digits + "_!@"

# --- THAM SỐ NÂNG CAO ---
# Tăng s lên 24 để p ngẫu nhiên hơn, giảm tỉ lệ trùng lặp
S_BIT = 24 

# Số mẫu tối thiểu để bắt đầu so sánh
MIN_SAMPLES = 800
# Số mẫu lấy thêm mỗi lần nếu chưa chắc chắn
STEP_SAMPLES = 400
# Ngưỡng tin cậy (Diff giữa Top 1 và Top 2 phải lớn hơn con số này)
CONFIDENCE_THRESHOLD = 0.05 

def get_server_batch(r, count):
    """Lấy một batch dữ liệu từ server"""
    hws = []
    try:
        for _ in range(count):
            r.sendlineafter(b"size > ", str(S_BIT).encode())
            r.recvline() # length
            hw = int(r.recvline().strip())
            r.recvline() # y
            hws.append(hw)
    except Exception as e:
        print(f"Error receiving: {e}")
    return hws

def simulate_mean(candidate_val, n_sims):
    """Tính Mean HW local bằng numpy cho nhanh"""
    # Tạo danh sách Prime ngẫu nhiên
    primes = [getPrime(S_BIT) for _ in range(n_sims)]
    
    # Tính toán vector hóa (nhanh hơn loop thường)
    # Lưu ý: Python int lớn không support numpy trực tiếp tốt, ta dùng list comprehension
    hws = [bin(candidate_val // p).count('1') for p in primes]
    
    return np.mean(hws)

def solve():
    # r = pwn.process(["python3", "chall.py"]) 
    r = pwn.remote(HOST, PORT)

    print(f"[*] Starting statistical attack (Precision Mode)...")
    
    # 1. Thu thập dữ liệu nền (Ground Truth) của Flag thật
    # Lấy thật nhiều mẫu ban đầu để làm chuẩn
    print(f"[*] Collecting initial Ground Truth ({MIN_SAMPLES*2} samples)...")
    real_samples = get_server_batch(r, MIN_SAMPLES * 2)
    real_mean = np.mean(real_samples)
    print(f"[+] Global Server Mean: {real_mean:.4f}")
    
    current_flag = KNOWN_PREFIX
    
    # 2. Vòng lặp đoán từng ký tự
    for i in range(len(KNOWN_PREFIX), FLAG_LEN - 1):
        print(f"\n[{i}/{FLAG_LEN}] Crack char '{current_flag}?'...")
        
        # Danh sách ứng viên tiềm năng
        candidates_scores = {} # char: diff
        
        # Tính toán padding
        pad_len_char = 1 + math.ceil(S_BIT / 8) # Padding 'a' của server
        suffix_pad_len = FLAG_LEN - len(current_flag) - 1 - len(KNOWN_SUFFIX)
        
        # --- Lượt quét 1: Quét nhanh tất cả ký tự ---
        for char in CHARSET:
            # Giả lập Flag: Known + Char + Null Padding + Known Suffix + 'a'*padding
            # Dùng \x00 làm padding giúp giảm nhiễu bit thấp
            guess_str = current_flag + char + ("\x00" * suffix_pad_len) + KNOWN_SUFFIX + ("a" * pad_len_char)
            val = bytes_to_long(guess_str.encode())
            
            # Mô phỏng (số lượng vừa phải để lọc bớt rác)
            sim_mean = simulate_mean(val, 800)
            diff = abs(real_mean - sim_mean)
            candidates_scores[char] = diff
        
        # --- Lượt quét 2: Adaptive - Kiểm tra kỹ các ứng viên Top đầu ---
        while True:
            # Sắp xếp theo độ lệch tăng dần (càng nhỏ càng đúng)
            sorted_candidates = sorted(candidates_scores.items(), key=lambda x: x[1])
            top1_char, top1_diff = sorted_candidates[0]
            top2_char, top2_diff = sorted_candidates[1]
            
            # Tính độ tự tin: Khoảng cách giữa Top 1 và Top 2
            margin = top2_diff - top1_diff
            
            print(f"   > Top 1: '{top1_char}' ({top1_diff:.4f}) | Top 2: '{top2_char}' ({top2_diff:.4f}) | Margin: {margin:.4f}")
            
            # Nếu margin đủ lớn -> Chốt luôn
            if margin > CONFIDENCE_THRESHOLD:
                print(f"   [+] Confirmed '{top1_char}' with high confidence.")
                current_flag += top1_char
                break
            else:
                # Nếu margin quá nhỏ -> Dữ liệu server đang nhiễu hoặc chưa đủ mẫu
                # Lấy thêm dữ liệu từ server để cập nhật Global Mean
                print(f"   [!] Margin too low. Fetching {STEP_SAMPLES} more samples from server...")
                new_samples = get_server_batch(r, STEP_SAMPLES)
                real_samples.extend(new_samples)
                real_mean = np.mean(real_samples)
                print(f"   [i] New Global Mean: {real_mean:.4f}")
                
                # Tính lại Score cho Top 5 ứng viên (không cần tính lại hết)
                print("   [i] Re-simulating top candidates...")
                top_k_chars = [x[0] for x in sorted_candidates[:5]]
                
                for char in top_k_chars:
                    # Tăng số lượng mô phỏng local lên để khớp với độ chính xác mới
                    guess_str = current_flag + char + ("\x00" * suffix_pad_len) + KNOWN_SUFFIX + ("a" * pad_len_char)
                    val = bytes_to_long(guess_str.encode())
                    # Tăng sample mô phỏng
                    sim_mean = simulate_mean(val, len(real_samples)) 
                    candidates_scores[char] = abs(real_mean - sim_mean)

    final_flag = current_flag + KNOWN_SUFFIX
    print(f"\n[SUCCESS] FLAG: {final_flag}")
    r.close()

if __name__ == "__main__":
    solve()