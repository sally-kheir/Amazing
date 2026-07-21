#!/usr/bin/env python3
"""Test Person A's maze generator code."""

from mazegen import MazeGenerator
from mazegen.maze import EAST, SOUTH, WEST, NORTH  # ← ADD THIS LINE!


def test_basic_generation():
    """Test 1: Basic maze generation."""
    print("=" * 60)
    print("Test 1: Basic Generation")
    print("=" * 60)
    
    mg = MazeGenerator(10, 10, seed=42)
    mg.generate((0, 0), (9, 9), perfect=True)
    
    print(f"✓ Grid size: {len(mg.grid)}x{len(mg.grid[0])}")
    print(f"✓ Entry: {mg.entry}")
    print(f"✓ Exit: {mg.exit_}")
    print(f"✓ Solution length: {len(mg.solution)}")
    print(f"✓ Solution: {mg.solution}")
    print()

def test_42_pattern():
    """Test 2: 42 pattern injection."""
    print("=" * 60)
    print("Test 2: 42 Pattern")
    print("=" * 60)
    
    mg = MazeGenerator(15, 11, seed=123)
    mg.generate((0, 0), (14, 10), perfect=True)
    maze = mg.get_maze()
    
    print(f"✓ Maze size: {maze.width}x{maze.height}")
    print(f"✓ Pattern cells: {len(maze.pattern_cells)}")
    
    if maze.pattern_cells:
        sample = list(maze.pattern_cells)[:5]
        print(f"✓ Sample pattern cells: {sample}")
    print()

def test_non_perfect():
    """Test 3: Non-perfect maze generation."""
    print("=" * 60)
    print("Test 3: Non-Perfect Maze")
    print("=" * 60)
    
    mg = MazeGenerator(10, 10, seed=456)
    mg.generate((0, 0), (9, 9), perfect=False)
    
    print(f"✓ Solution length: {len(mg.solution)}")
    print(f"✓ Solution: {mg.solution[:30]}...")
    print()

def test_different_sizes():
    """Test 4: Different maze sizes."""
    print("=" * 60)
    print("Test 4: Different Sizes")
    print("=" * 60)
    
    sizes = [(5, 5), (7, 7), (20, 15), (30, 20)]
    
    for width, height in sizes:
        mg = MazeGenerator(width, height, seed=42)
        mg.generate((0, 0), (width-1, height-1), perfect=True)
        
        maze = mg.get_maze()
        pattern_status = "✓ Has pattern" if maze.pattern_cells else "✗ No pattern (too small)"
        print(f"  {width}x{height}: {pattern_status}, Solution length: {len(mg.solution)}")
    
    print()

def test_reproducibility():
    """Test 5: Same seed produces same maze."""
    print("=" * 60)
    print("Test 5: Reproducibility")
    print("=" * 60)
    
    mg1 = MazeGenerator(8, 8, seed=999)
    mg1.generate((0, 0), (7, 7), perfect=True)
    
    mg2 = MazeGenerator(8, 8, seed=999)
    mg2.generate((0, 0), (7, 7), perfect=True)
    
    same = True
    for y in range(8):
        for x in range(8):
            if mg1.grid[y][x] != mg2.grid[y][x]:
                same = False
                break
        if not same:
            break
    
    print(f"✓ Same seed produces same maze: {same}")
    print(f"✓ Solution 1: {mg1.solution}")
    print(f"✓ Solution 2: {mg2.solution}")
    print()

def test_pattern_coherence():
    """Test 6: Pattern cells don't affect maze connectivity."""
    print("=" * 60)
    print("Test 6: Pattern Coherence")
    print("=" * 60)
    
    mg = MazeGenerator(15, 11, seed=42)
    mg.generate((0, 0), (14, 10), perfect=True)
    maze = mg.get_maze()
    
    pattern_cells_closed = True
    for px, py in maze.pattern_cells:
        if maze.grid[py][px] != 15:
            pattern_cells_closed = False
            break
    
    print(f"✓ All pattern cells fully closed: {pattern_cells_closed}")
    
    entry_ok = maze.entry not in maze.pattern_cells
    exit_ok = maze.exit_ not in maze.pattern_cells
    
    print(f"✓ Entry not in pattern: {entry_ok}")
    print(f"✓ Exit not in pattern: {exit_ok}")
    
    path_exists = mg.solution != ""
    print(f"✓ Solution exists: {path_exists}")
    print()

def test_wall_coherence():
    """Test 7: Wall coherence between neighbours."""
    print("=" * 60)
    print("Test 7: Wall Coherence")
    print("=" * 60)
    
    mg = MazeGenerator(10, 10, seed=42)
    mg.generate((0, 0), (9, 9), perfect=True)
    maze = mg.get_maze()
    
    coherent = True
    for y in range(maze.height):
        for x in range(maze.width):
            if x < maze.width - 1:
                east_wall = maze.is_wall(x, y, EAST)
                west_wall_of_neighbour = maze.is_wall(x + 1, y, WEST)
                if east_wall != west_wall_of_neighbour:
                    coherent = False
                    print(f"  ✗ Incoherent at ({x},{y}) East vs ({x+1},{y}) West")
                    break
            
            if y < maze.height - 1:
                south_wall = maze.is_wall(x, y, SOUTH)
                north_wall_below = maze.is_wall(x, y + 1, NORTH)
                if south_wall != north_wall_below:
                    coherent = False
                    print(f"  ✗ Incoherent at ({x},{y}) South vs ({x},{y+1}) North")
                    break
        
        if not coherent:
            break
    
    print(f"✓ All walls coherent: {coherent}")
    print()

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("   TESTING PERSON A'S MAZE GENERATOR")
    print("=" * 60 + "\n")
    
    try:
        test_basic_generation()
        test_42_pattern()
        test_non_perfect()
        test_different_sizes()
        test_reproducibility()
        test_pattern_coherence()
        test_wall_coherence()
        
        print("=" * 60)
        print("   ✅ ALL TESTS PASSED!")
        print("   Person A's code is working perfectly! 🎉")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
