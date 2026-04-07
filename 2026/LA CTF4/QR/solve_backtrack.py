from PIL import Image
import numpy as np
from itertools import permutations
import multiprocessing as mp
from functools import partial

# Load the scrambled QR code
img = Image.open('chall.png')
img_array = np.array(img)

# Extract the 25 chunks (5x5 grid, each chunk is 90x90 pixels)
chunk_size = 90
chunks = []
for y in range(5):
    for x in range(5):
        chunk = img_array[y*chunk_size:(y+1)*chunk_size, 
                         x*chunk_size:(x+1)*chunk_size]
        chunks.append(chunk)

print(f"Extracted {len(chunks)} chunks")

# Downsample chunks to 9x9 modules (each module is 10x10 pixels)
def downsample_chunk(chunk):
    return chunk[::10, ::10]

chunk_modules = [downsample_chunk(chunk) for chunk in chunks]

# Analyze chunk patterns to find edges
def analyze_edges(modules):
    """Analyze the edges of a 9x9 module chunk"""
    top = tuple(modules[0, :].tolist())
    bottom = tuple(modules[8, :].tolist())
    left = tuple(modules[:, 0].tolist())
    right = tuple(modules[:, 8].tolist())
    return {'top': top, 'bottom': bottom, 'left': left, 'right': right}

# Get edge patterns for all chunks
chunk_edges = [analyze_edges(m) for m in chunk_modules]

print("Analyzing chunk edges for compatibility...")

# Find compatible neighbors
def are_compatible(chunk1_idx, chunk2_idx, direction):
    """Check if two chunks are compatible in given direction"""
    # direction: 'right' means chunk2 is to the right of chunk1
    if direction == 'right':
        return chunk_edges[chunk1_idx]['right'] == chunk_edges[chunk2_idx]['left']
    elif direction == 'bottom':
        return chunk_edges[chunk1_idx]['bottom'] == chunk_edges[chunk2_idx]['top']
    return False

# Build compatibility matrix
print("Building compatibility matrix...")
right_compat = {}
bottom_compat = {}

for i in range(25):
    right_compat[i] = [j for j in range(25) if i != j and are_compatible(i, j, 'right')]
    bottom_compat[i] = [j for j in range(25) if i != j and are_compatible(i, j, 'bottom')]

print("Compatibility matrix built")
print(f"Average right neighbors per chunk: {sum(len(v) for v in right_compat.values()) / 25:.1f}")
print(f"Average bottom neighbors per chunk: {sum(len(v) for v in bottom_compat.values()) / 25:.1f}")

# Use backtracking to solve the puzzle
def solve_puzzle():
    """Use backtracking with constraints to solve the puzzle"""
    grid = [None] * 25
    used = set()
    
    def backtrack(pos):
        if pos == 25:
            return True
        
        row = pos // 5
        col = pos % 5
        
        # Get candidates
        candidates = list(range(25))
        
        # Filter by left neighbor constraint
        if col > 0:
            left_chunk = grid[pos - 1]
            candidates = [c for c in candidates if c in right_compat[left_chunk] and c not in used]
        else:
            candidates = [c for c in candidates if c not in used]
        
        # Filter by top neighbor constraint
        if row > 0:
            top_chunk = grid[pos - 5]
            candidates = [c for c in candidates if c in bottom_compat[top_chunk] and c not in used]
        
        for candidate in candidates:
            grid[pos] = candidate
            used.add(candidate)
            
            if backtrack(pos + 1):
                return True
            
            grid[pos] = None
            used.remove(candidate)
        
        return False
    
    if backtrack(0):
        return grid
    return None

print("\nSolving puzzle using backtracking with edge constraints...")
solution = solve_puzzle()

if solution:
    print(f"\n🎉 Found solution!")
    print(f"Solution: {solution}")
    
    # Reconstruct the QR code
    reconstructed = np.zeros((450, 450), dtype=np.uint8)
    for i, chunk_idx in enumerate(solution):
        y = i // 5
        x = i % 5
        reconstructed[y*chunk_size:(y+1)*chunk_size, 
                     x*chunk_size:(x+1)*chunk_size] = chunks[chunk_idx]
    
    # Save the solved QR code
    Image.fromarray(reconstructed).save('solved.png')
    print("Saved solved QR code to solved.png")
    
    # Try to decode it
    try:
        from pyzbar.pyzbar import decode
        decoded = decode(Image.fromarray(reconstructed))
        if decoded:
            flag = decoded[0].data.decode()
            print(f"\n🎉🎉🎉 FLAG: {flag}")
        else:
            print("\nCouldn't decode QR code automatically. Check solved.png manually.")
    except Exception as e:
        print(f"\nError decoding: {e}")
        print("Check solved.png manually.")
else:
    print("\nNo solution found with current constraints.")
    print("This might mean the edge matching approach needs refinement.")
