import time
import sys
import math

# ANSI colors
RED = "\033[91m"
PINK = "\033[95m"
MAGENTA = "\033[35m"
BRIGHT_RED = "\033[1;91m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"


def clear():
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def is_heart(x, y, size=1):
    """Perfect heart shape formula"""
    x = x / (size * 10)
    y = y / (size * 10)
    equation = (x**2 + y**2 - 1)**3 - x**2 * y**3
    return equation < 0


def get_heart_outline_points(size, num_points=200):
    """Generate points along the heart outline in drawing order"""
    points = []
    
    # Parametric heart curve
    for i in range(num_points):
        t = (i / num_points) * 2 * math.pi
        
        # Parametric equations for heart
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        # Scale and adjust
        x = x * size * 1.5
        y = -y * size * 1.2
        
        points.append((x, y))
    
    return points


def draw_growing_hearts():
    """Draw hearts growing from center outward like a snake"""
    width = 80
    height = 40
    center_x = width // 2
    center_y = height // 2
    
    # Heart sizes (from small to large for growing effect)
    sizes = [0.6, 1.0, 1.4, 1.8, 2.2]
    colors = [PINK, MAGENTA, PINK, BRIGHT_RED, RED]
    
    # Store all drawn points for persistence
    all_drawn_points = []
    
    # Draw each heart one by one
    for heart_idx, size in enumerate(sizes):
        outline_points = get_heart_outline_points(size, num_points=300)
        current_heart_points = []
        
        # Animate this heart growing
        for point_idx in range(len(outline_points)):
            clear()
            print("\n" * 2)
            
            # Add new point
            current_heart_points.append(outline_points[point_idx])
            
            # Create display grid
            grid = {}
            
            # Draw all previously completed hearts
            for prev_points, prev_color, prev_size in all_drawn_points:
                for px, py in prev_points:
                    col = int(center_x + px / 0.5)
                    row = int(center_y - py / 0.8)
                    if 0 <= row < height and 0 <= col < width:
                        grid[(row, col)] = (prev_color, "●")
            
            # Draw current growing heart with trailing effect
            for i, (px, py) in enumerate(current_heart_points):
                col = int(center_x + px / 0.5)
                row = int(center_y - py / 0.8)
                
                if 0 <= row < height and 0 <= col < width:
                    # Trailing effect: recent points are brighter
                    trail_length = 20
                    if i >= len(current_heart_points) - trail_length:
                        distance_from_head = len(current_heart_points) - 1 - i
                        if distance_from_head < 5:
                            grid[(row, col)] = (colors[heart_idx], "●")
                        elif distance_from_head < 12:
                            grid[(row, col)] = (colors[heart_idx], "•")
                        else:
                            grid[(row, col)] = (colors[heart_idx], ".")
                    else:
                        grid[(row, col)] = (colors[heart_idx], "●")
            
            # Render the grid
            for row in range(height):
                line = ""
                for col in range(width):
                    if (row, col) in grid:
                        color, char = grid[(row, col)]
                        line += color + char + RESET
                    else:
                        line += " "
                print(line)
            
            time.sleep(0.01)
        
        # Store this completed heart
        all_drawn_points.append((current_heart_points, colors[heart_idx], size))
        time.sleep(0.3)
    
    # Final display - fill in the hearts completely
    time.sleep(0.5)
    clear()
    print("\n" * 2)
    
    for row in range(height):
        line = ""
        y = (center_y - row) * 0.8
        
        for col in range(width):
            x = (col - center_x) * 0.5
            
            drawn = False
    
            for i in range(len(sizes) - 1, -1, -1):
                if is_heart(x, y, sizes[i]):
                    line += colors[i] + "●" + RESET
                    drawn = True
                    break
            
            if not drawn:
                line += " "
        
        print(line)


def love_text():
    """Animated love text"""
    text = "♥ I LOVE YOU ♥"
    colors = [RED, PINK, MAGENTA, BRIGHT_RED]
    
    for _ in range(3):
        for color in colors:
            sys.stdout.write("\r" + " " * 15 + color + text + RESET)
            sys.stdout.flush()
            time.sleep(0.2)
    print()


if __name__ == "__main__":
    draw_growing_hearts()
    print("\n")
    love_text()
    time.sleep(2)