from utils import *
from functionality import apply_kernel

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Drawing Program")

def init_grid(rows, cols, color):
    grid = [[color for _ in range(cols)] for i in range(rows)]
    return grid

def init_kernel(rows, cols, color):
    kernel = [[color for _ in range(cols)] for i in range(rows)]

    return kernel

def init_output(rows, cols, color):
    output = [[color for _ in range(cols)] for i in range(rows)]

    return output

def draw_kernel(win, kernel):
    for i, row in enumerate(kernel):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * KERNEL_PIXEL_SIZE + KERNEL_START_X, i *
                                          KERNEL_PIXEL_SIZE + KERNEL_START_Y, KERNEL_PIXEL_SIZE, KERNEL_PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(KERNEL_SIZE + 1):
            pygame.draw.line(win, BLACK, (KERNEL_START_X, i * KERNEL_PIXEL_SIZE + KERNEL_START_Y),
                             (KERNEL_WIDTH + KERNEL_START_X, i * KERNEL_PIXEL_SIZE + KERNEL_START_Y))

        for i in range(KERNEL_SIZE + 1):
            pygame.draw.line(win, BLACK, (KERNEL_START_X + i * KERNEL_PIXEL_SIZE, KERNEL_START_Y),
                             (KERNEL_START_X + (KERNEL_PIXEL_SIZE * i), KERNEL_START_Y + (KERNEL_PIXEL_SIZE * KERNEL_SIZE)))


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * MAT_PIXEL_SIZE, i *
                                          MAT_PIXEL_SIZE, MAT_PIXEL_SIZE, MAT_PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(MAT_ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * MAT_PIXEL_SIZE),
                             (MAT_WIDTH, i * MAT_PIXEL_SIZE))

        for i in range(MAT_COLS + 1):
            pygame.draw.line(win, BLACK, (i * MAT_PIXEL_SIZE, 0),
                             (i * MAT_PIXEL_SIZE, MAT_HEIGHT - TOOLBAR_HEIGHT))

def draw_output(win, output):
    for i, row in enumerate(output):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * OUTPUT_PIXEL_SIZE + OUTPUT_START_X, i *
                                          OUTPUT_PIXEL_SIZE + OUTPUT_START_Y, OUTPUT_PIXEL_SIZE, OUTPUT_PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(OUTPUT_SIZE + 1):
            pygame.draw.line(win, BLACK, (OUTPUT_START_X, i * OUTPUT_PIXEL_SIZE + OUTPUT_START_Y),
                             (OUTPUT_WIDTH + OUTPUT_START_X, i * OUTPUT_PIXEL_SIZE + OUTPUT_START_Y))

        for i in range(OUTPUT_SIZE + 1):
            pygame.draw.line(win, BLACK, (OUTPUT_START_X + i * OUTPUT_PIXEL_SIZE, OUTPUT_START_Y),
                             (OUTPUT_START_X + (OUTPUT_PIXEL_SIZE * i), OUTPUT_START_Y + (OUTPUT_PIXEL_SIZE * OUTPUT_SIZE)))


def draw(win, grid, kernel, output, mat_buttons, kernel_buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    draw_kernel(win, kernel)

    draw_output(win, output)

    for button in mat_buttons + kernel_buttons:
        button.draw(win)

    pygame.display.update()


def mat_coords_from_pos(pos):
    x, y = pos
    row = y // MAT_PIXEL_SIZE
    col = x // MAT_PIXEL_SIZE

    if row >= MAT_ROWS:
        raise IndexError

    return row, col

def kernel_coords_from_pos(pos):
    x, y = pos
    row = (y - KERNEL_PAD) // KERNEL_PIXEL_SIZE
    col = (x - 300 - KERNEL_PAD) // KERNEL_PIXEL_SIZE

    if row >= MAT_ROWS:
        raise IndexError

    return row, col


run = True
clock = pygame.time.Clock()
grid = init_grid(MAT_ROWS, MAT_COLS, BG_COLOR)
kernel = init_kernel(KERNEL_SIZE, KERNEL_SIZE, BG_COLOR)
output = init_output(OUTPUT_SIZE, OUTPUT_SIZE, BG_COLOR)
drawing_color = BLACK

button_y = MAT_HEIGHT - TOOLBAR_HEIGHT / 2 - 25
mat_buttons = [
    Button(10, button_y, 50, 50, BLACK, "Draw", BLACK),
    Button(70, button_y, 50, 50, WHITE, "Erase", BLACK),
    Button(130, button_y, 50, 50, WHITE, "Clear", BLACK),
    Button(190, button_y, 50, 50, WHITE, "Save", BLACK)
]

kernel_buttons = [
    Button(10 + 325, button_y - 50, 50, 50, BLACK, "Draw", BLACK),
    Button(70 + 325, button_y - 50, 50, 50, WHITE, "Erase", BLACK),
    Button(130 + 325, button_y - 50, 50, 50, WHITE, "Clear", BLACK),
    Button(190 + 325, button_y - 50, 50, 50, WHITE, "Save", BLACK)
]

misc_buttons = [
    Button(275, 325, 50, 50, WHITE, "Apply", "BLACK")
]

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                if pos[0] > 300:
                    row, col = kernel_coords_from_pos(pos)
                    kernel[row][col] = drawing_color
                else:
                    row, col = mat_coords_from_pos(pos)
                    grid[row][col] = drawing_color
            except IndexError:
                for button in mat_buttons:
                    if not button.clicked(pos):
                        continue

                    if button.text == "Draw":
                        drawing_color = BLACK
                    if button.text == "Save":
                        MAT = [[i[0] for i in j] for j in grid]
                    if button.text == "Clear":
                        grid = init_grid(MAT_ROWS, MAT_COLS, BG_COLOR)
                    if button.text == "Erase":
                        drawing_color = WHITE

                for button in kernel_buttons:
                    if not button.clicked(pos):
                        continue

                    if button.text == "Draw":
                        drawing_color = BLACK
                    if button.text == "Save":
                        KERNEL = [[(abs(i[0] - 255)) for i in j] for j in kernel]
                    if button.text == "Clear":
                        kernel = init_kernel(KERNEL_SIZE, KERNEL_SIZE, BG_COLOR)
                    if button.text == "Erase":
                        drawing_color = WHITE

                for button in misc_buttons:
                    if not button.clicked(pos):
                        continue

                    if button.text == 'Apply':
                        try:
                            output = apply_kernel(MAT, KERNEL)
                            print(output)
                        except TypeError as e:
                            print(e)
                            print('save your matrices!')

    draw(WIN, grid, kernel, output, mat_buttons, kernel_buttons + misc_buttons)

pygame.quit()
