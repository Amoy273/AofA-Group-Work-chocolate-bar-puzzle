import pygame
import sys 
from bar import Bar

pygame.init()

# Window Configuration
Width = 1000
Height = 1000

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Chocolate Bar Simulation")
clock = pygame.time.Clock()

# Specifying Colors For Simulation
background = (219, 210, 179)
dark_brown = (110, 74, 48)
chocolate = (120, 65, 35)
chocolate_light = (160, 100, 35) 
gold = (218, 170, 100)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (191, 191, 191)

# Specifying Fonts For Simulation
title_font = pygame.font.SysFont("times new roman", 40, bold=True)
heading_font = pygame.font.SysFont("times new roman", 24, bold=True)
reg_font = pygame.font.SysFont("times new roman", 20)
small_font = pygame.font.SysFont("times new roman", 18)

# Placeholder Simulation Variables
rows = 3
columns = 3
orientation = "H"
offset_text = '1'

# Dimension Input Values
rows_text = "3"
columns_text = "3"
active_input = None
status_message = ""

# Dimentional Input Buttons
rows_input = pygame.Rect(160, 570, 150, 40)
columns_input = pygame.Rect(520, 570, 150, 40)

# Main Buttons
create_button = pygame.Rect(160, 625, 200, 40)
reset_button = pygame.Rect(520, 625, 150, 40)
break_button = pygame.Rect(700, 755, 150, 50)

# Orientation Buttons
horizontal_button = pygame.Rect(160, 755, 140, 40)
vertical_button = pygame.Rect(320, 755, 140, 40)

# Offset Input Box
offset_input = pygame.Rect(520, 755, 150, 40)

bar = Bar(rows, columns)

selected_piece = None
orientation = "H"
offset = 1

# Specifing Screen Positions
bar_area = pygame.Rect(100, 130, 800, 340)
bar_controls = pygame.Rect(100, 500, 800, 450)

# Simulation Functions
def Draw_text (text, font, color, x, y, center=False):
    rendered = font.render(text, True, color)

    if center:
        rect = rendered.get_rect(center=(x, y))
    else:
        rect = rendered.get_rect(topleft=(x, y))

    screen.blit(rendered, rect)

def Draw_chocolate_bar(rows=4, columns=6):  # Displays the "Chocolate Bar"
    pygame.draw.rect(screen, dark_brown, bar_area, border_radius=10)
    cell_width = bar_area.width / bar.n
    cell_height = bar_area.height / bar.m

    # Get the current state of the chocolate bar
    grid = bar.grid()

    # Draw each square individually
    for row in range (bar.m):
        for col in range (bar.n):

            piece_id = grid[row][col]

            x = bar_area.x + col * cell_width
            y = bar_area.y + row * cell_height

            cell = pygame.Rect(int(x), int(y), int(cell_width), int(cell_height))

            # Highlight the selected piece of the chocolate bar
            if piece_id == selected_piece:
                color = gold
            else:
                color = chocolate_light

            pygame.draw.rect(screen, color, cell)
            pygame.draw.rect(screen, dark_brown, cell, 3)


def Draw_controls():    # Displays the user controls
    pygame.draw.rect(screen, white, bar_controls, border_radius=15)
    pygame.draw.rect(screen, gray, bar_controls, 2, border_radius=15)

    Draw_text("Simulation Controls", heading_font, dark_brown, bar_controls.centerx, 525, center=True)
    Draw_text("Rows (m):", reg_font, black, 160, 545)
    Draw_text("Columns (n)", reg_font, black, 520, 545)

    # Input Box for Rows
    pygame.draw.rect(screen, white, rows_input, border_radius=5)
    row_border = dark_brown if active_input == "rows" else gray
    pygame.draw.rect(screen, row_border, rows_input, 2, border_radius=5)
    Draw_text(rows_text, reg_font, black, 175, 580)

    # Input Box for Columns
    pygame.draw.rect(screen, white, columns_input, border_radius=5)
    col_border = dark_brown if active_input == "columns" else gray
    pygame.draw.rect(screen, col_border, columns_input, 2, border_radius=5)
    Draw_text(columns_text, reg_font, black, 535, 580)

    # Create Bar Button
    pygame.draw.rect(screen, chocolate, create_button, border_radius=8)
    Draw_text("Create Chocolate Bar", small_font, white, create_button.centerx, create_button.centery, center=True)

    # Reset Button
    pygame.draw.rect(screen, chocolate, reset_button, border_radius=8)
    Draw_text("Reset", reg_font, white, reset_button.centerx, reset_button.centery, center=True)

    # Break Control Label
    Draw_text("Break Controls", heading_font, dark_brown, bar_controls.centerx, 700, center=True)

    # Orientation Label
    Draw_text("Orientation", small_font, black, 160, 730)

    # Horizontal Break Button
    horizontal_color = chocolate if orientation == "H" else gray

    pygame.draw.rect(screen, horizontal_color, horizontal_button, border_radius=5)
    Draw_text("Horizontal", small_font, white if orientation == "H" else black, horizontal_button.centerx, horizontal_button.centery, center=True)

    # Vertical Break Button
    vertical_color = chocolate if orientation == "V" else gray

    pygame.draw.rect(screen,vertical_color, vertical_button, border_radius=5)
    Draw_text("Vertical", small_font, white if orientation == "V" else black, vertical_button.centerx, vertical_button.centery, center=True)

    # Offset Label
    Draw_text("Cut Offset:", small_font, black, 520, 730)

    # Offset Button
    pygame.draw.rect(screen, white, offset_input, border_radius=5)
    pygame.draw.rect(screen, chocolate if active_input == "offset" else gray, offset_input, 2, border_radius=5)
    Draw_text(offset_text, reg_font, black, 535, 765)

    # Break Button
    pygame.draw.rect(screen, chocolate, break_button, border_radius=8)
    Draw_text("Break Piece", small_font, white, break_button.centerx, break_button.centery, center=True)

    # Selected Piece of Chocolate Bar
    if selected_piece is not None and selected_piece in bar.pieces:
        piece = bar.pieces[selected_piece]

        piece_info = (f"Selected: Piece {piece.id} "
                      f"({piece.height} x {piece.width})")

    else:
        piece_info = "No piece selected"

    Draw_text(piece_info, small_font, dark_brown, bar_controls.centerx, 810, center=True)   

def Draw_statistics():
    pieces = len(bar.pieces)
    breaks = bar.breaks
    expected_breaks = (bar.m * bar.n) - 1
    solved = bar.is_solved()

    # Statistics Heading 
    Draw_text("Simulation Statistics", heading_font, dark_brown, bar_controls.centerx, 840, center=True)

    # Statistics 
    stats_text = (
        f"Pieces: {pieces}      "
        f"Breaks: {breaks}      "
        f"Required: {expected_breaks}       "
    )

    Draw_text(stats_text, small_font, dark_brown, bar_controls.centerx, 875, center=True)

    # Completion Status
    if solved:
        completion_text = "Completed!"
        completion_color = (40, 130, 70)
    else:
        completion_text = "In Progress"
        completion_color = dark_brown

    Draw_text(completion_text, small_font, completion_color, bar_controls.centerx, 910, center=True)

# Main Loop
running = True

while running: 
    for event in pygame.event.get():

        # Exit logic 
        if event.type == pygame.QUIT:
            running = False

        # Handing Mouse Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if rows_input.collidepoint(event.pos):
                active_input = "rows"

            elif columns_input.collidepoint(event.pos):
                active_input = "columns"

            elif create_button.collidepoint(event.pos):
                active_input = None

                try:
                    new_rows = int(rows_text)
                    new_columns = int(columns_text)

                    if new_rows > 10 or new_columns > 10:
                        raise ValueError("Maximum dimensions are 10 x 10.")

                    # Create A New Chocolate Bar
                    bar = Bar(new_rows, new_columns)

                    # Update Dimensions
                    rows = new_rows
                    columns = new_columns

                    # Reset Selection
                    selected_piece = None

                    status_message = f"{rows} x {columns} Chocolate Bar has been successfully created!"

                except ValueError as error:
                    status_message = str(error)

            elif reset_button.collidepoint(event.pos):
                active_input = None

                # Recreate the Chocolate Bar
                bar = Bar(bar.m, bar.n)

                # Clear the selected piece
                selected_piece = None

                # Restore Default Settings
                orientation = "H"
                offset_text = "1"

                # Clear Status Message
                status_message = "Simulation was reset successfully!"

            elif bar_area.collidepoint(event.pos):
                active_input = None

                # Determine Which Square Was Clicked
                cell_width = bar_area.width / bar.n
                cell_height = bar_area.height / bar.m

                col = int((event.pos[0] - bar_area.x) / cell_width)
                row = int((event.pos[1] - bar_area.y) / cell_height)

                # Get ID Of Selected Piece
                grid = bar.grid()
                selected_piece = grid[row][col]

                status_message = f"Piece {selected_piece} has been selected!"

            elif horizontal_button.collidepoint(event.pos):
                orientation = "H"
                active_input = None

            elif vertical_button.collidepoint(event.pos):
                orientation = "V"
                active_input = None

            elif offset_input.collidepoint(event.pos):
                active_input = "offset"

            elif break_button.collidepoint(event.pos):
                active_input = None

                # Check if a piece has been selected
                try:
                    if selected_piece is None:
                        raise ValueError("Please select a piece first.")

                    # Convert the offset to an integer
                    cut_offset = int(offset_text)

                    # Execute Break
                    bar.break_piece(selected_piece, orientation, cut_offset)
                    selected_piece = None
                    status_message = "Piece successfully broken!"

                except ValueError as error:
                    status_message = str(error)
            
            else: 
                active_input = None

        # Handling Keyboard Input
        if event.type == pygame.KEYDOWN:

            if active_input == "rows":
                if event.key == pygame.K_BACKSPACE:
                    rows_text = rows_text[:-1]

                elif event.unicode.isdigit():
                    rows_text += event.unicode 

            elif active_input == "columns":
                if event.key == pygame.K_BACKSPACE:
                    columns_text = columns_text[:-1]
                
                elif event.unicode.isdigit():
                        columns_text += event.unicode 

            elif active_input == "offset":
                if event.key == pygame.K_BACKSPACE:
                    offset_text = offset_text[:-1]

                elif event.unicode.isdigit():
                    offset_text += event.unicode


    screen.fill(background)

    Draw_text("Chocolate Bar Simulation", title_font, dark_brown, Width // 2, 55, center=True)
    Draw_text("Click a bar to begin", heading_font, dark_brown, Width // 2, 95, center=True)
    Draw_chocolate_bar(bar, selected_piece)
    Draw_controls()
    Draw_statistics()

    if status_message:
        Draw_text(status_message, small_font, dark_brown, Width // 2, 485, center=True)

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit

