import pygame
from math import cos, sin, pi, floor, sqrt
import colorsys

# pygame settings
background_color = (0, 0, 0) # black
tree_color = (0, 255, 0) # green
width, height = 1000, 800
thick = 6
color_gradient = 1

# fractal settings
length0 = width / 5
levels = 13


def gradient_line(win, color1, color2, pos1, pos2, width, split = 3):
    """
    Manually split a line from pos1 to pos2 into 'split' # of lines to add
    color gradient from color1 to color2 (linear interpolation)
    """
    # store useful calculation
    delta_color = color2[0] - color1[0], color2[1] - color1[1], color2[2] - color1[2]
    delta_pos = pos2[0] - pos1[0], pos2[1] - pos1[1]
    for i in range(split):
        weight = i / split

        # linearly interpolate the colors
        r = color1[0] + weight * delta_color[0]
        g = color1[1] + weight * delta_color[1]
        b = color1[2] + weight * delta_color[2]

        # compute 
        x1, y1 = pos1[0] + weight * delta_pos[0], pos1[1] + weight * delta_pos[1]
        x2, y2 = pos1[0] + (i+1) / split * delta_pos[0], pos1[1] + (i+1) / split * delta_pos[1]
        pygame.draw.line(win, (r, g, b), (x1, y1), (x2, y2), width=width)


def fractal(win, x, y, length, angle, ratio, delta_angle, level=levels):
    """
    Draw fractal tree recursively
    """
    # keep track of levels left to be drawn
    if level <= 0:
        return

    # NB y axis is pointing down
    x2 = x + length * cos(angle)
    y2 = y - length * sin(angle)

    # adjust width of branch according to level
    branch_width = floor(level / levels * thick)

    if color_gradient:
        # compute rainbow gradient color
        color1 = list(map(lambda x: 255 * x, colorsys.hsv_to_rgb(level/levels, 1.0, 1.0)))
        color2 = list(map(lambda x: 255 * x, colorsys.hsv_to_rgb((level - 1)/levels, 1.0, 1.0)))

        gradient_line(win, color1, color2, (x, y), (x2, y2), width=branch_width)
    else:
        pygame.draw.line(win, tree_color, (x, y), (x2, y2), width=branch_width)

    # right subtree
    fractal(win, x2, y2, length * ratio, angle - delta_angle, ratio, delta_angle, level-1)
    # left subtree
    fractal(win, x2, y2, length * ratio, angle + delta_angle, ratio, delta_angle, level-1)


def main():
    pygame.init() # serve?
    win = pygame.display.set_mode((width, height))

    run = True
    while run:
        win.fill(background_color)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # slide tree's shape (angle) with mouse horizontally
        delta_theta = pi * mouse_x / width
        # make tree grow with mouse vertically
        # use sqrt to make it grow faster at the beginning, not linearly
        ratio = sqrt((height - mouse_y) / height)

        # draw fractal. first line is vertical
        fractal(win, width / 2, height * 0.8, length0 * ratio, pi/2, ratio, delta_theta)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
            
if __name__ == '__main__':
    main()
