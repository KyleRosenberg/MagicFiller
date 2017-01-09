import pygame
import random
import sys
import time

size = [400, 400]
brushsize = 1

class Canvas:

    def __init__(self):
        self.screen = pygame.display.set_mode(size)

    def stroke_pixel(self, pos, color, brushsize):
        for x in range(pos[0] - int(brushsize/2)-1, pos[0] + int(brushsize/2)):
            for y in range(pos[1] - int(brushsize/2)-1, pos[1] + int(brushsize/2)):
                if self.distance(pos, (x, y)) <= int(brushsize/2-1):
                    self.screen.set_at((x, y), color)

    def get_pixel_color(self, pos):
        return self.screen.get_at(pos)

    def connect_points(self, pos1, pos2, color):
        pygame.draw.line(self.screen, color, pos1, pos2, brushsize)

    def distance(self, p1, p2):
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)

    def scan(self):
        for x in range(size[0]):
            for y in range(size[1]):
                if self.get_pixel_color((x, y)) == (255, 255, 255, 255):
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
                    self.flood_fill((x, y), color)

    def get_valid_neighbors(self, pos, dist=1):
        ret = []
        if pos[0]-dist >= 0 and (self.get_pixel_color((pos[0]-dist, pos[1])) == (255, 255, 255, 255)):
            ret.append((pos[0]-dist, pos[1]))
        if pos[0]+dist < size[0] and (self.get_pixel_color((pos[0]+dist, pos[1])) == (255, 255, 255, 255)):
            ret.append((pos[0]+dist, pos[1]))
        if pos[1]+dist < size[0] and (self.get_pixel_color((pos[0], pos[1]+dist)) == (255, 255, 255, 255)):
            ret.append((pos[0], pos[1]+dist))
        if pos[1]-dist >= 0 and (self.get_pixel_color((pos[0], pos[1]-dist)) == (255, 255, 255, 255)):
            ret.append((pos[0], pos[1]-dist))
        return ret

    def flood_fill(self, pos, color):
        unvis = []
        vis = []
        currpos = pos
        while currpos is not None:
            vis.append(currpos)
            stsz = 2
            self.stroke_pixel(currpos, color, stsz)
            neigh = self.get_valid_neighbors(currpos)
            unvis += neigh
            if len(unvis) > 0:
                currpos = unvis.pop()
            else:
                currpos = None

    def draw(self):
        pygame.display.flip()


def main():
    pygame.init()
    c = Canvas()
    c.screen.fill((255, 255, 255))
    done = False
    drawing = False
    lastmouse = pygame.mouse.get_pos()
    lastenter = pygame.key.get_pressed()[pygame.K_RETURN]
    while not done:
        currmouse = pygame.mouse.get_pos()
        currenter = pygame.key.get_pressed()[pygame.K_RETURN]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if not drawing:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                c.stroke_pixel(pos, (0, 0, 0), brushsize)
                c.connect_points(lastmouse, currmouse, (0, 0, 0, 255))

            if lastenter and not currenter:
                drawing = True
                start = time.time()
                c.scan()
                end = time.time()
                print("Finished in %s seconds" % (end-start))
                c.draw()

        c.draw()
        lastmouse = currmouse
        lastenter = currenter

if __name__ == "__main__":
    main()