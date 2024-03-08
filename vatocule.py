# To learn how to use this goto https://www.pygame.org/docs/
import pygame
import csv
import math

def generate_points(n, cx, cy, r):
    """
    Generate equally spaced points around a central point.
    
    - n (int): The number of points to generate.
    - cx (float/int): The x-coordinate of the central point.
    - cy (float/int): The y-coordinate of the central point.
    - r (float/int): The radius of the circle on which the points will be generated.
    """
    points = []
    for i in range(n):
        angle = math.pi * 2 * i / n
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    return points

# Load elements from csv table, return a dictionary (hopefully)

def load_elements(filename):
    # We have to make our own because its being difficult
    """
    Load the elements from a csv file and return a dictionary.
    
    - filename (str): The path to the csv file containing the elements.
    """
    file = open(filename)
    tempdict = {}
    tempdict2 = {}
    csvreader = csv.reader(file)
    tempdict["Header"] = next(csvreader)
    for row in csvreader:
        i = 0
        tempdict2 = {}
        for item in row:
            tempdict2[tempdict["Header"][i]] = item
            i += 1
        tempdict[row[1]] = tempdict2
    return tempdict
            
elements = load_elements('Downloads\pte.csv')

# Default config variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a window, make resizable
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE)

# Set the title of the window to "Vatocule"
pygame.display.set_caption("Vatocule")
# It is named "Vatocule" because it is a combination of 3 words, 
# "View", "Atom", and "Molecule." It is because it can view atoms and
# molecules in 2D and 3D (TODO: implement 3D)


class Utils():
    def __init__(self, inpscreen):
        self.screen = inpscreen
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
    def refresh(self): 
        """
        Updates the width and height attributes of the Utils instance.

        This method retrieves the current size of the pygame screen and 
        updates the width and height attributes accordingly. It is typically 
        called when the pygame window is resized to ensure that the Utils 
        instance always has the correct dimensions of the screen.
        """
        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]
    def draw_centered_circle(self, xoff, yoff, rad, color=(255,255,255)):
        """
        Draw a centered circle on the screen.

        Parameters:
        - xoff (int): The x-offset from the center of the screen.
        - yoff (int): The y-offset from the center of the screen.
        - rad (int): The radius of the circle.
        - color (tuple, optional): The color of the circle in RGB format. Defaults to white (255, 255, 255).
        """
        pygame.draw.circle(self.screen, color, (self.width//2+xoff, self.height//2+yoff), rad)

utils = Utils(screen)

# Test this
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            utils.refresh()
            print(str(utils.width)+" "+str(utils.height))
    for point in generate_points(10, 0, 0, 25):
            utils.draw_centered_circle(point[0],point[1],10)
    pygame.display.flip()

pygame.quit()