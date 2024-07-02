import pygame
from src.linked_list import LinkedList
import math

# Initialize
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Linked List Visualization Tool @triswetaDas")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NODE_COLOR = (206, 245, 220)
TITLE_COLOR = (70, 46, 71)

# Fonts
font_size = 24
font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
small_font = pygame.font.Font(pygame.font.match_font('arial'), int(font_size * 0.6))
title_font = pygame.font.Font(pygame.font.match_font('arial'), 36)
subtitle_font = pygame.font.Font(pygame.font.match_font('arial'), 20)

# List of Linked Lists and selected index
linked_lists = [LinkedList()]
selected_index = 0

def draw_arrow(screen, start, end, color, arrow_size=10):
    pygame.draw.aaline(screen, color, start, end)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left_arrow = (end[0] - arrow_size * math.cos(angle - math.pi / 6), 
                  end[1] - arrow_size * math.sin(angle - math.pi / 6))
    right_arrow = (end[0] - arrow_size * math.cos(angle + math.pi / 6), 
                   end[1] - arrow_size * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(screen, color, [end, left_arrow, right_arrow])


def draw_linked_lists():
    screen.fill(WHITE)

    title_text = title_font.render('Singly Linked List Visualizer', True, TITLE_COLOR)
    subtitle_text = subtitle_font.render('https://github.com/trisweta', True, TITLE_COLOR)
    instructions_text = [
        "Press 'A' to Add a node                                         Press 'M' to Merge All Lists into One",
        "Press 'D' to Delete a node by index                      Press 'Page Up' to Sort Ascending",
        "Press 'R' to Reverse the list                                  Press 'Page Down' to Sort Descending",
        "Press 'N' to Start a New Linked List                     Press 'C' to Clear All Linked Lists",
        "Click on a linked list to select it!                           Press 'Esc' to quit visualizer     ",
    ]
    
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 20))
    screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, 60))
    
    for i, line in enumerate(instructions_text):
        instr_text = small_font.render(line, True, BLACK)
        screen.blit(instr_text, (20, 100 + i * 30))

    #each LL 
    start_y = 270  
    list_spacing = 100
    for index, linked_list in enumerate(linked_lists):
        current = linked_list.head
        x, y = 100, start_y
        node_positions = []
        max_x = x
        min_y = y
        while current:
            #nodes
            pygame.draw.circle(screen, NODE_COLOR, (x, y), 25)
            pygame.draw.circle(screen, BLACK, (x, y), 25, 2)  # Border for the circle

            #add the number
            text = font.render(str(current.value), True, BLACK)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

            node_positions.append((x, y))
            if current.next:
                next_x = x + 80
                pygame.draw.aaline(screen, BLACK, (x + 25, y), (next_x - 25, y))
                draw_arrow(screen, (x + 25, y), (next_x - 25, y), BLACK)
            current = current.next
            x += 80
            max_x = max(max_x, x)
        min_y = y

        #null node
        if node_positions:
            last_node_x = node_positions[-1][0] + 80
            null_circle_center = (last_node_x, y)
            pygame.draw.circle(screen, NODE_COLOR, null_circle_center, 25)
            pygame.draw.circle(screen, BLACK, null_circle_center, 25, 2) 
            null_text = small_font.render("X", True, BLACK)
            screen.blit(null_text, (last_node_x - null_text.get_width() // 2, y - null_text.get_height() // 2))

            #arrow
            pygame.draw.aaline(screen, BLACK, (node_positions[-1][0] + 25, y), (null_circle_center[0] - 25, y))
            draw_arrow(screen, (node_positions[-1][0] + 25, y), (null_circle_center[0] - 25, y), BLACK)

        #selection box
        if index == selected_index:
            padding = 30 
            pygame.draw.rect(screen, BLACK, 
                (100 - padding, start_y - padding, max_x - 100 + 2 * padding, min_y - start_y + padding+30), 2)

        start_y += list_spacing 

    pygame.display.flip()

def handle_input():
    global linked_lists, selected_index
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False  #exit
            elif event.key == pygame.K_a:
                #add node
                value = input("Enter value to add: ")
                try:
                    value = int(value)
                    linked_lists[selected_index].add_node(value)
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            elif event.key == pygame.K_d:
                #delete node
                index = input("Enter index to delete: ")
                try:
                    index = int(index)
                    linked_lists[selected_index].delete_node_by_index(index)
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            elif event.key == pygame.K_r:
                #reverse
                animate_reverse()
            elif event.key == pygame.K_n:
                #create new
                linked_lists.append(LinkedList())
                selected_index = len(linked_lists) - 1
            elif event.key == pygame.K_c:
                # clear
                linked_lists = [LinkedList()]
                selected_index = 0
            elif event.key == pygame.K_m:
                #merfe 
                merged_list = LinkedList.merge(*linked_lists)
                linked_lists = [merged_list]
                selected_index = 0
            elif event.key == pygame.K_PAGEUP:
                #ascending order
                linked_lists[selected_index].sort(order='asc')
            elif event.key == pygame.K_PAGEDOWN:
                #descending order
                linked_lists[selected_index].sort(order='desc')

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            start_y = 250
            list_spacing = 250
            for index in range(len(linked_lists)):
                if start_y <= mouse_y <= start_y + 250:
                    selected_index = index
                    break
                start_y += list_spacing

    return True

def animate_reverse():
    global linked_lists

    if not linked_lists:
        return

    linked_lists[selected_index].reverse()
    screen.fill(WHITE)
    draw_linked_lists()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        running = handle_input()
        draw_linked_lists()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
