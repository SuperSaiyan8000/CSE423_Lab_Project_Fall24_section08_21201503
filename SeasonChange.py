import time
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class SeasonalCycle:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.season = 0  # 0: Spring, 1: Summer, 2: Fall, 3: Winter
        self.day_time = 0  # 0 to 1 representing time of day
        self.sky_state = 2  # 0: Night, 1: Dawn, 2: Day, 3: Dusk
        self.last_update = time.time()
        self.raindrops = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]
        self.snowflakes = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]
        self.leaves = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(50)] 

    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glPointSize(2.0)
        gluOrtho2D(0, self.width, 0, self.height)

    def plot_point(self, x, y):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def midpoint_line(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.plot_point(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def midpoint_circle(self, center_x, center_y, radius):
        x = radius
        y = 0
        decision = 1 - radius

        while y <= x:
            self.plot_point(center_x + x, center_y + y)
            self.plot_point(center_x + y, center_y + x)
            self.plot_point(center_x - y, center_y + x)
            self.plot_point(center_x - x, center_y + y)
            self.plot_point(center_x - x, center_y - y)
            self.plot_point(center_x - y, center_y - x)
            self.plot_point(center_x + y, center_y - x)
            self.plot_point(center_x + x, center_y - y)

            y += 1
            if decision <= 0:
                decision += 2 * y + 1
            else:
                x -= 1
                decision += 2 * (y - x) + 1

    def draw_sun(self, x, y):
        if (self.sky_state == 2 or self.sky_state == 1) and self.season != 0:
            glColor3f(1.0, 1.0, 0.0)
            self.midpoint_circle(x, y, 30)

    def draw_moon(self, x, y):
        if self.sky_state == 0:
            glColor3f(0.9, 0.9, 0.9)
            self.midpoint_circle(x, y, 20)

    def draw_ground(self):
        season_colors = {
            0: (0.1, 0.5, 0.1),
            1: (0.2, 0.8, 0.2),
            2: (0.8, 0.4, 0.2),
            3: (1.0, 1.0, 1.0),
        }
        
        glColor3f(*season_colors[self.season])
        for y in range(0, int(self.height / 3)):
            for x in range(0, self.width, 2):
                self.plot_point(x, y)

    def draw_sky(self):
        sky_colors = {
            0: (0.0, 0.0, 0.1),
            1: (0.9, 0.6, 0.8),
            2: (0.4, 0.6, 1.0),
            3: (0.5, 0.3, 0.4),
        }
        
        glColor3f(*sky_colors[self.sky_state])
        for y in range(int(self.height / 3), self.height, 2):
            for x in range(0, self.width, 2):
                self.plot_point(x, y)

    def draw_stars(self):
        if self.sky_state == 0 or self.sky_state == 3:
            glColor3f(1.0, 1.0, 1.0)
            for _ in range(100):
                x = (hash(str(_ * 123)) % self.width)
                y = (hash(str(_ * 456)) % (self.height - self.height // 3)) + self.height // 3
                self.plot_point(x, y)

    def draw_rain(self):
        if self.season == 0:
            glColor3f(0.0, 0.0, 1.0)
            speed = 30
            for i in range(len(self.raindrops)):
                x, y = self.raindrops[i]
                for offset in range(5):
                    self.plot_point(x, y - offset)
                y -= speed
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                self.raindrops[i] = (x, y)

    def draw_snow(self):
        if self.season == 3:
            glColor3f(1.0, 1.0, 1.0)
            for i in range(len(self.snowflakes)):
                x, y = self.snowflakes[i]
                x += random.randint(-1, 1)
                y -= 2
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                self.snowflakes[i] = (x, y)
                self.plot_point(x, y)
                
    def draw_leaves(self):
        if self.season == 2:  # Fall
            glColor3f(0.8, 0.4, 0.2)  
            for i in range(len(self.leaves)):
                x, y = self.leaves[i]
                x += random.randint(-2, 2)  
                y -= random.randint(1, 3)   
                
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                    
                self.leaves[i] = (x, y)
                
                self.plot_point(x, y)        
                self.plot_point(x, y + 2)    
                self.plot_point(x - 2, y)    
                self.plot_point(x, y - 2)    
                self.plot_point(x + 2, y)     

    def draw_house(self):
       
        glColor3f(1.0, 1.0, 0.0) 
       
        self.midpoint_line(300, 200, 500, 200)  
        self.midpoint_line(300, 200, 300, 350) 
        self.midpoint_line(500, 200, 500, 350) 
        self.midpoint_line(300, 350, 500, 350)  

       
        glColor3f(1.0, 0.0, 0.0) 
       
        self.midpoint_line(280, 350, 520, 350) 
        self.midpoint_line(280, 350, 400, 450) 
        self.midpoint_line(520, 350, 400, 450)  

       
        glColor3f(0.4, 0.2, 0.1) 
     
        self.midpoint_line(370, 200, 370, 275) 
        self.midpoint_line(430, 200, 430, 275) 
        self.midpoint_line(370, 275, 430, 275) 

    def draw_tree(self):
      
        glColor3f(0.55, 0.27, 0.07)
       
        self.midpoint_line(700, 200, 700, 400) 
        self.midpoint_line(720, 200, 720, 400) 
        self.midpoint_line(700, 400, 720, 400) 

       
        branch_points = [
          
            (710, 400, 660, 450),  
            (710, 400, 760, 450), 
            (710, 450, 670, 500),  
            (710, 450, 750, 500), 
            (710, 500, 680, 550), 
            (710, 500, 740, 550), 
         
            (660, 450, 640, 500), (760, 450, 780, 500), 
            (670, 500, 650, 550), (750, 500, 770, 550),  
            (680, 550, 660, 600), (740, 550, 760, 600),  
            (710, 550, 710, 650) 
        ]

        for start_x, start_y, end_x, end_y in branch_points:
            self.midpoint_line(start_x, start_y, end_x, end_y)

       
        if self.season == 2: 
            glColor3f(1.0, 0.647, 0.0)  
        elif self.season == 3: r
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.1, 0.5, 0.1) 
       
        leaf_positions = [
            (660, 450), (760, 450), (670, 500), (750, 500),
            (680, 550), (740, 550), (710, 550),
          
            (640, 500), (780, 500), (650, 550), (770, 550),
            (660, 600), (760, 600), (710, 650)
        ]

      
        for center_x, center_y in leaf_positions:
            for dx in range(-15, 16, 5):
                for dy in range(-15, 16, 5):
                    if dx**2 + dy**2 <= 225: 
                        self.midpoint_circle(center_x + dx, center_y + dy, random.randint(2, 5))

       
        for _ in range(100):
            random_x = random.randint(640, 780)
            random_y = random.randint(500, 650)
            self.midpoint_circle(random_x, random_y, random.randint(2, 5))







    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_sky()
        self.draw_stars()
        sun_x = int(self.width * self.day_time)
        sun_y = int(self.height / 2 + math.sin(self.day_time * math.pi) * 200)
        self.draw_sun(sun_x, sun_y)
        self.draw_moon(sun_x, sun_y)
        self.draw_ground()
        self.draw_rain()
        self.draw_snow()
        self.draw_leaves()
        self.draw_house()
        self.draw_tree() 
        glutSwapBuffers()





    def update(self, value):
        current_time = time.time()
        elapsed = current_time - self.last_update
        self.day_time += elapsed * 0.1
        if self.day_time >= 1.0:
            self.day_time = 0.0
        self.last_update = current_time
        self.display()
        glutTimerFunc(16, self.update, 0)

    def handle_keypress(self, key, x, y):
        if key == b's':  
            self.season = (self.season + 1) % 4
        elif key == b't':  
            self.sky_state = (self.sky_state + 1) % 4

def main():
    cycle = SeasonalCycle()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(cycle.width, cycle.height)
    glutCreateWindow(b"Seasonal Cycle with House")
    cycle.init_gl()
    glutDisplayFunc(cycle.display)
    glutKeyboardFunc(cycle.handle_keypress)
    glutTimerFunc(0, cycle.update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()

