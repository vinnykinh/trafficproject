import pygame as pg
from pygame.math import Vector2
import random
import time



class Entity(pg.sprite.Sprite):

    def __init__(self, pos, waypoints):
        super().__init__()
        self.image = pg.Surface((30, 45))
        self.image.fill(pg.Color(random.choices(range(250,256), k=3)))
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.max_speed = 3
        self.pos = Vector2(pos)
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 100


    def update(self):
        # A vector pointing from self to the target.
        heading = self.target - self.pos
        distance = heading.length()  # Distance to the target.
        heading.normalize_ip()
        if distance <= 4:  # We're closer than 2 pixels.
            # Increment the waypoint index to swtich the target.
            # The modulo sets the index back to 0 if it's equal to the length.
            self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
            self.target = self.waypoints[self.waypoint_index]
        if distance <= self.target_radius:
            # If we're approaching the target, we slow down.
            self.vel = heading * (distance / self.target_radius * self.max_speed)
        else:  # Otherwise move with max_speed.
            self.vel = heading * self.max_speed

        self.pos += self.vel
        self.rect.center = self.pos


def main():
    pg.display.set_caption("WarehouseManagementRobots")

    # junction coordinates
    junction1 = (246, 156)
    junction2 = (761, 156)
    junction3 = (246, 490)
    junction4 = (761, 490)
    junction5 = (246, 819)
    junction6 = (761, 819)

    # robot home positions
    robot1loc = (39, 150)
    robot2loc = (968, 150)
    robot3loc = (968, 490)
    robot4loc = (39, 819)
    # stations
    station1 = (39, 150)
    station2 = (968, 150)
    station3 = (39, 490)
    station4 = (968, 490)
    station5 = (39, 819)
    station6 = (968, 819)

    screen = pg.display.set_mode((1020, 1008))
    clock = pg.time.Clock()

    forward11 = [junction1, junction2, junction4,junction6, station6]
    forward12 = [junction1, junction3, junction4, junction6, station6]
    forward13 = [junction1, junction5, junction6, station6]
    back11 = [junction6, junction4,junction2,junction1, robot1loc]
    back12 = [junction6, junction4, junction3, junction1, robot1loc]
    back13 = [junction5, junction3,junction1, robot1loc]
    forward = [forward11, forward12, forward13]
    back = [back11, back12, back13]
    i = random.choice(forward)
    j = random.choice(back)
    testway1 = [junction1, junction2, junction4, junction6, station6,junction6,junction5,junction3,junction1,robot1loc]
    print(i.__add__(j))
    robotway1 = i.__add__(j)

    forward31 = [junction4, junction2, junction1, junction3, junction5, station5]
    forward32 = [junction4, junction6, junction5, station5]
    forward33 = [junction4, junction3, junction5, station5]
    back31 = [junction5, junction3, junction4, robot3loc]
    back32 = [junction5, junction6, junction4, robot3loc]
    back33 = [junction5, junction3, junction1, junction2, junction4, robot3loc]
    forward3 = [forward31, forward32, forward33]
    back3 = [back31, back32, back33]
    k = random.choice(forward3)
    l = random.choice(back3)
    testway3 = [junction4,junction3,station3,station5,junction5,junction3,junction1,junction2,junction4,robot3loc]
    robotways3 = k.__add__(l)

    forward21 = [junction2, junction1, junction3, station3]
    forward22 = [junction2, junction4, junction3, station3]
    forward23 = [junction2, junction4, junction6, junction5, junction3, station3]
    back21 = [junction3, junction4, junction2, robot2loc]
    back22 = [junction3, junction5, junction6, junction4, junction2, robot2loc]
    back23 = [junction3, junction1, junction2, robot2loc]
    forward4 = [forward21, forward22, forward23]
    back4 = [back21, back22, back23]
    m = random.choice(forward4)
    n = random.choice(back4)
    testway2 = [junction2,junction4,junction6,junction5,junction3,station3,junction3,junction1,junction2,robot2loc]
    robotways2 = m.__add__(n)

    forward41 = [junction5, junction6, junction4, station4]
    forward42 = [junction5, junction3, junction1, junction2, junction4, station4]
    forward43 = [junction5, junction3, junction4, station4]
    back41 = [junction4, junction3, junction5, robot4loc]
    back42 = [junction4, junction2, junction1, junction3, junction5, robot4loc]
    back43 = [junction4, junction6, junction5, robot4loc]
    back5 = random.choice([back41, back42, back43])
    forward5 = random.choice([forward41, forward42, forward43])
    testway4 = [station3,station1,junction1,junction2,station2,station4,station6,junction6,junction5,robot4loc]
    robotways4 = forward5.__add__(back5)

    sprite1 = pg.sprite.Group(Entity((39, 150), testway1))
    sprite2 = pg.sprite.Group(Entity((968, 150), testway2))
    sprite3 = pg.sprite.Group(Entity((968, 490), testway3))
    sprite4 = pg.sprite.Group(Entity((39, 819), testway4))

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        sprite1.update()
        sprite2.update()
        sprite3.update()
        sprite4.update()

        screen.fill((40, 40, 40))
        sprite2.draw(screen)
        sprite1.draw(screen)
        sprite3.draw(screen)
        sprite4.draw(screen)
        for point in robotway1:
            pg.draw.rect(screen, (90, 200, 40), (point, (4, 4)))

        # defining the robot grid
        pg.draw.line(screen, (255, 255, 255), (0, 156), (1020, 156), 4)
        pg.draw.line(screen, (255, 255, 255), (0, 490), (1020, 490), 4)
        pg.draw.line(screen, (255, 255, 255), (0, 819), (1020, 819), 4)
        pg.draw.line(screen, (255, 255, 255), (246, 0), (246, 1008), 4)
        pg.draw.line(screen, (255, 255, 255), (761, 0), (761, 1008), 4)
        pg.draw.line(screen, (255, 255, 255), (39, 0), (39,1008), 4)
        pg.draw.line(screen, (255, 255, 255), (968, 0), (968, 1008), 4)

        #station markers
        green =(0, 255, 0)
        home_position = (0,0,255)
        pg.draw.circle(screen, home_position, station1, 20)
        pg.draw.circle(screen, home_position, station2, 20)
        pg.draw.circle(screen, green, station3, 20)
        pg.draw.circle(screen, home_position, station4, 20)
        pg.draw.circle(screen, home_position, station5, 20)
        pg.draw.circle(screen, green, station6, 20)



        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
