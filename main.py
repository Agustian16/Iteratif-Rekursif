import time
import matplotlib.pyplot as plt
import random
import string
import pandas as pd

def create_grid(size, word=None):
    """
    Membuat grid dengan ukuran tertentu dan menyisipkan kata jika diberikan
    """
    # Membuat grid kosong
    grid = [[random.choice(string.ascii_lowercase) for _ in range(size)] 
            for _ in range(size)]
    
    # - random position horizontal
    if word:
        if len(word) <= size:
            row = random.randint(0, size-1)
            col = random.randint(0, size-len(word))
            for i, letter in enumerate(word):
                grid[row][col+i] = letter
    
    return grid

def print_grid(grid):
    """
    Mencetak grid dengan format yang rapi
    """
    for row in grid:
        print(' '.join(row))

def search_iterative(grid, word):
    """
    Implementasi pencarian kata secara iteratif
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Def 8 arah pencarian
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # find first character
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == word[0]:
                # Mencoba setiap arah
                for dx, dy in directions:
                    x, y = i, j
                    found = True
                    # find next character
                    for k in range(len(word)):
                        if (x < 0 or x >= rows or 
                            y < 0 or y >= cols or 
                            grid[x][y] != word[k]):
                            found = False
                            break
                        x += dx
                        y += dy
                    if found:
                        return True, (i, j)
    return False, None

def search_recursive(grid, word):
    """
    Implementasi pencarian kata secara rekursif
    """
    def search_from_position(x, y, word_index):
        # Base case - find the character
        if word_index == len(word):
            return True
            
        # worst case: character tidak match
        if (x < 0 or x >= len(grid) or 
            y < 0 or y >= len(grid[0]) or 
            grid[x][y] != word[word_index]):
            return False
            
    
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        # retry setiap arah
        for dx, dy in directions:
            if search_from_position(x + dx, y + dy, word_index + 1):
                return True
        return False
    

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == word[0]:
                if search_from_position(i, j, 0):
                    return True, (i, j)
    return False, None

def measure_performance(sizes, word, num_tests=3):
    """
    Mengukur performa kedua algoritma dengan berbagai ukuran input
    """
    results = []
    
    for size in sizes:
        iter_times = []
        rec_times = []
        
        for _ in range(num_tests):
            # inserting the word
            grid = create_grid(size, word)
            
            # menghitung waktu algoritma iteratif
            start = time.time()
            found_iter, _ = search_iterative(grid, word)
            iter_time = time.time() - start
            iter_times.append(iter_time)
            
            # menghitung waktu algoritma rekursif
            start = time.time()
            found_rec, _ = search_recursive(grid, word)
            rec_time = time.time() - start
            rec_times.append(rec_time)
            
            # Verifying output memberikan hasil yang sama
            assert found_iter == found_rec, f"Inconsistent results for size {size}"
        
        results.append({
            'size': size,
            'iterative_time': sum(iter_times) / num_tests,
            'recursive_time': sum(rec_times) / num_tests
        })
    
    return pd.DataFrame(results)

def plot_performance(results):
    """
    Membuat plot perbandingan performa
    """
    plt.figure(figsize=(10, 6))
    plt.plot(results['size'], results['iterative_time'], 'b-', label='Iterative')
    plt.plot(results['size'], results['recursive_time'], 'r-', label='Recursive')
    plt.xlabel('Grid Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison: Iterative vs Recursive Word Search')
    plt.legend()
    plt.grid(True)
    plt.savefig('performance_comparison.png')
    plt.close()

def main():
    # test#1
    word = "python"
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # sample grid kecil
    print("sample finding grid 5x5:")
    small_grid = create_grid(5, word)
    print("\nGrid:")
    print_grid(small_grid)
    
    found_iter, pos_iter = search_iterative(small_grid, word)
    print(f"\nHasil finding iteratif: {'found' if found_iter else 'not found'}")
    if found_iter:
        print(f"Posisi awal: {pos_iter}")
    
    # hitung memplot performa
    print("\nMengukur performa...")
    results = measure_performance(sizes, word)
    
    # export CSV
    results.to_csv('performance_results.csv', index=False)
    print("\nHasil pengukuran:")
    print(results)
    
    # create plot
    plot_performance(results)
    print("\nPlot performa telah tersimpan'performance_comparison.png'")

if __name__ == "__main__":
    main()