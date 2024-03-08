# Most important TODO: Organize this code!
# More stuff todo: Draw electrons and make the nucleus look better

# To learn how to use this goto https://www.pygame.org/docs/
import pygame
import csv
import math
import random

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
            
elements = load_elements('pte.csv')

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
    def return_jitter(self, x, y, intensity):
        """
        Returns a jittered coordinate.

        Parameters:
        - x (int): The x-coordinate of the point to jitter.
        - y (int): The y-coordinate of the point to jitter.
        - intensity (int): The intensity of the jitter.
        """
        return (x+random.randrange(-intensity,intensity), y+random.randrange(-intensity,intensity))
    def generate_points(self, n, cx, cy, r):
        """
        Generate equally spaced points around a central point.
        
        - n (int): The number of points to generate.
        - cx (float/int): The x-coordinate of the central point.
        - cy (float/int): The y-coordinate of the central point.
        - r (float/int): The radius of the circle on which the points will be generated.
        """
        points = []
        if n == 1:
            points.append((cx, cy))
        else:
            for i in range(n):
                angle = math.pi * 2 * i / n
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                points.append((x, y))
        return points

class Atom:
    def __init__(self, element, screen, utils, x, y, z = 0):
        """
        Create an Atom object.
        
        Parameters:
        - element (str): The chemical symbol of the element.
        - x (float/int): The centered x-coordinate of the atom.
        - y (float/int): The centered y-coordinate of the atom.
        - z (float/int): The centered z-coordinate of the atom.
        """
        self.elementdata = elements[element]
        self.screen = screen
        self.utils = utils
        self.x = x
        self.y = y
        self.z = z
        self.protons = int(self.elementdata["NumberofProtons"])
        self.neutrons = int(self.elementdata["NumberofNeutrons"])
        self.elecrtons = int(self.elementdata["NumberofElectrons"])
        self.pointcols = []
        
        for i in range(self.protons):
            self.pointcols.append((255,0,0))
            
        for i in range(self.neutrons):
            self.pointcols.append((255,255,255))
            
        print(self.pointcols)
        random.shuffle(self.pointcols)
        print(self.pointcols)
        # pregen points
        # Draw the nucleus
        self.points = []
        k = 0
        for j in range((self.protons+self.neutrons)//8+1):
            print("ran" + str(j))
            for i in range(8+j):
                self.points.append(self.utils.generate_points(8+j, self.x, self.y, ((self.protons+self.neutrons)//8-((j+1)**1.7+3))*0.9)[i])
                if k == self.protons+self.neutrons:
                    break
                k += 1
    def draw(self, jitter = 0):
        """
        Draw the atom on the screen.
        
        - x (float/int): The x-coordinate of the atom.
        - y (float/int): The y-coordinate of the atom.
        - jitter (int, optional): The intensity of the jitter. Defaults to 0.
        """
            
        # Draw everything in points
        self.newpoints = []
        for i in range(len(self.pointcols)):
            self.newpoints.append(self.utils.return_jitter(self.points[i][0], self.points[i][1], jitter))
            self.utils.draw_centered_circle(self.newpoints[i][0], self.newpoints[i][1], 10, self.pointcols[i])

utils = Utils(screen)

hydrogen = Atom("Hydrogen", screen, utils, 0, 0)

# Test this
running = True
i = 0
while running:
    # fill screen
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            utils.refresh()
            print(str(utils.width)+" "+str(utils.height))
    hydrogen.draw(1)
    pygame.display.flip()

pygame.quit()