import pygame as pg
import pymunk as pm
import pymunk.pygame_util as dw
import numpy as np
import matplotlib.pyplot as plt


pg.init()
WIDTH, HEIGHT = 500, 500
window = pg.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options):
    window.fill("black")
    space.debug_draw(draw_options)
    pg.display.update()

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)],
    ]
    for pos, size, in rects:
        body = pm.Body(body_type=pm.Body.STATIC)
        body.position = pos
        shape = pm.Poly.create_box(body, size)
        shape.elasticity = 0.8
        shape.friction = 0.5
        space.add(body, shape)

def create_pendulum(space, pos, L, second_body=None):
    body = pm.Body()
    body.position = [pos[0], pos[1]+L]
    circle = pm.Circle(body, 20)
    circle.mass = 30
    circle.elasticity = 1
    if second_body:
        rotation_center_joint = pm.PinJoint(body, second_body, (0,0))
    else:
        rotation_center_body = pm.Body(body_type=pm.Body.STATIC)
        rotation_center_body.position = pos
        rotation_center_joint = pm.PinJoint(body, rotation_center_body, (0,0))
    
    space.add(circle, body, rotation_center_joint)


def create_ball(space):
    body = pm.Body()
    body.position = (250, 250)
    shape = pm.Circle(body, 20)
    shape.mass = 20
    shape.color = (250, 250, 250, 100)
    shape.elasticity = 0.1
    space.add(body, shape)
    return shape


def run(window, width, height):
    run = True
    clock = pg.time.Clock()
    fps = 60

    space = pm.Space()
    space.gravity = (0, 900)

    L = 300
    create_pendulum(space, (100, 0), L)
    create_pendulum(space, (WIDTH-200, 0), L)
    rotation_center_joint = pm.DampedSpring(space.bodies[0],space.bodies[1], (0,0), (0,0), 100, 20, 0)
    space.add(rotation_center_joint)
    create_pendulum(space, space.bodies[0].position, 100, space.bodies[0])

    draw_options = dw.DrawOptions(window)
    t = []
    theta1 = []
    theta2 = []
    theta3 = []

    # ball = create_ball(space)
    create_boundaries(space, WIDTH, HEIGHT)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        t.append(pg.time.get_ticks()/1000)
        theta1.append(np.arctan2(space.bodies[0].position[1], (space.bodies[0].position[0]-100)))
        theta2.append(np.arctan2(space.bodies[1].position[1], (space.bodies[1].position[0]-WIDTH+200)))
        theta3.append(np.arctan2((space.bodies[2].position[1]-L), (space.bodies[2].position[0]-100)))
        draw(space, window, draw_options)
        space.step(1/fps) 
        clock.tick(fps)

    pg.quit()
    t = np.array(t)
    theta1 = np.array(theta1)
    theta2 = np.array(theta2)
    theta3 = np.array(theta3)
    t -= t[0]
    plt.plot(t, theta1)
    plt.show()
    plt.plot(t, theta2)
    plt.show()
    plt.plot(t, theta3)
    plt.show()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
