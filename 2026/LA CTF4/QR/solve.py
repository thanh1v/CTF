from PIL import Image
import numpy as np
import segno
from pyzbar.pyzbar import decode
from itertools import product

# Load the scrambled QR code
img = Image.open('chall.png')
img_array = np.array(img)

# The image is 450x450, divided into 5x5 grid of 90x90 pixel chunks
chunk_pixel_size = 90

# Extract the 25 chunks
chunks = []
for y in range(5):
    for x in range(5):
        chunk = img_array[y*chunk_pixel_size:(y+1)*chunk_pixel_size, 
                         x*chunk_pixel_size:(x+1)*chunk_pixel_size]
        chunks.append(chunk)

print(f"Extracted {len(chunks)} chunks of size {chunk_pixel_size}x{chunk_pixel_size}")

def reconstruct_qr(chunk_order):
    """Reconstruct QR code from chunk order (list of 25 indices)"""
    reconstructed = np.zeros((450, 450), dtype=np.uint8)
    for i, chunk_idx in enumerate(chunk_order):
        y = i // 5
        x = i % 5
        reconstructed[y*chunk_pixel_size:(y+1)*chunk_pixel_size, 
                     x*chunk_pixel_size:(x+1)*chunk_pixel_size] = chunks[chunk_idx]
    return reconstructed

def try_decode(img_array):
    """Try to decode QR code"""
    img = Image.fromarray(img_array)
    try:
        decoded = decode(img)
        if decoded:
            return decoded[0].data.decode()
    except:
        pass
    return None

# QR code version 7 is 45x45 modules
# With 5x5 chunks, each chunk is 9x9 modules
# At 10 pixels per module, each chunk is 90x90 pixels ✓

# Key insight: QR codes have position detection patterns at three corners
# These are 7x7 module patterns that are very distinctive
# They should be at: (0,0), (38,0), (0,38) for a 45x45 QR code

def downsample_chunk(chunk):
    """Downsample 90x90 pixel chunk to 9x9 modules"""
    # Take every 10th pixel
    return chunk[::10, ::10]

def count_dark_modules(region):
    """Count dark modules in a region"""
    return np.sum(region < 128)

def has_finder_pattern_tl(modules):
    """Check if 9x9 module chunk has finder pattern in top-left"""
    if modules.shape != (9, 9):
        return False
    # Finder pattern is 7x7, should be in top-left corner
    pattern = modules[:7, :7]
    dark_count = count_dark_modules(pattern)
    # Finder pattern has ~25 dark modules out of 49
    return 20 <= dark_count <= 30

def has_finder_pattern_tr(modules):
    """Check if 9x9 module chunk has finder pattern in top-right"""
    if modules.shape != (9, 9):
        return False
    pattern = modules[:7, 2:]  # Top-right of the chunk
    dark_count = count_dark_modules(pattern)
    return 20 <= dark_count <= 30

def has_finder_pattern_bl(modules):
    """Check if 9x9 module chunk has finder pattern in bottom-left"""
    if modules.shape != (9, 9):
        return False
    pattern = modules[2:, :7]  # Bottom-left of the chunk
    dark_count = count_dark_modules(pattern)
    return 20 <= dark_count <= 30

# Downsample all chunks
chunk_modules = [downsample_chunk(chunk) for chunk in chunks]

# Find candidates for corner positions
tl_candidates = [i for i, m in enumerate(chunk_modules) if has_finder_pattern_tl(m)]
tr_candidates = [i for i, m in enumerate(chunk_modules) if has_finder_pattern_tr(m)]
bl_candidates = [i for i, m in enumerate(chunk_modules) if has_finder_pattern_bl(m)]

print(f"\nTop-left corner candidates: {tl_candidates}")
print(f"Top-right corner candidates: {tr_candidates}")
print(f"Bottom-left corner candidates: {bl_candidates}")

# The finder patterns span multiple chunks:
# Top-left: chunks at positions (0,0), (0,1), (1,0)
# Top-right: chunks at positions (0,3), (0,4), (1,4)
# Bottom-left: chunks at positions (3,0), (4,0), (4,1)

# Let's try all combinations of corner candidates
print("\nTrying combinations of corner chunks...")

found = False
attempts = 0

# Try brute force with constraints
# We'll fix the corners and try permutations of the rest
for tl in tl_candidates if tl_candidates else range(25):
    for tr in tr_candidates if tr_candidates else range(25):
        if tr == tl:
            continue
        for bl in bl_candidates if bl_candidates else range(25):
            if bl == tl or bl == tr:
                continue
            
            # Fix these three corners
            # Position 0 (top-left): tl
            # Position 4 (top-right): tr  
            # Position 20 (bottom-left): bl
            
            # Try random permutations for the rest
            import random
            remaining = [i for i in range(25) if i not in [tl, tr, bl]]
            
            for _ in range(1000):
                random.shuffle(remaining)
                
                # Build the permutation
                perm = [None] * 25
                perm[0] = tl
                perm[4] = tr
                perm[20] = bl
                
                # Fill in the rest
                remaining_idx = 0
                for i in range(25):
                    if perm[i] is None:
                        perm[i] = remaining[remaining_idx]
                        remaining_idx += 1
                
                reconstructed = reconstruct_qr(perm)
                result = try_decode(reconstructed)
                
                attempts += 1
                if result and result.startswith('lactf{'):
                    print(f"\n🎉 Found flag after {attempts} attempts: {result}")
                    # Save the successful reconstruction
                    Image.fromarray(reconstructed).save('solved.png')
                    found = True
                    break
                
                if attempts % 10000 == 0:
                    print(f"Tried {attempts} permutations...")
            
            if found:
                break
        if found:
            break
    if found:
        break

if not found:
    print(f"\nDidn't find flag after {attempts} attempts.")
    print("Trying pure random search...")
    
    import random
    for attempt in range(100000):
        perm = list(range(25))
        random.shuffle(perm)
        
        reconstructed = reconstruct_qr(perm)
        result = try_decode(reconstructed)
        
        if result and result.startswith('lactf{'):
            print(f"\n🎉 Found flag: {result}")
            Image.fromarray(reconstructed).save('solved.png')
            break
        
        if attempt % 10000 == 0:
            print(f"Tried {attempt} permutations...")
