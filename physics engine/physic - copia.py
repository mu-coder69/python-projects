import pygame as pg
import pymunk as pm
import pymunk.pygame_util as dw
import matplotlib.pyplot as plt
import numpy as np


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
    shape.elasticity = 1
    space.add(body, shape)
    return shape


def run(window, width, height):
    run = True
    clock = pg.time.Clock()
    fps = 60

    space = pm.Space()
    space.gravity = (0, 0)

    L = 300
    #create_pendulum(space, (100, 0), L)
    b0 = space.static_body
    p0 = 0,300
    body = pm.Body()
    body.position = 100, L
    circle = pm.Circle(body, 1)
    circle.mass = 30
    circle.elasticity = 1
    rotation_center_joint = pm.DampedSpring(body,b0, (0,0), p0, 150, 20, 0)
    space.add(circle, body, rotation_center_joint)


    draw_options = dw.DrawOptions(window)
    x = []
    t = []
    # ball = create_ball(space)
    create_boundaries(space, WIDTH, HEIGHT)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            
        draw(space, window, draw_options)
        x.append(space.bodies[0].position[0])
        space.step(1/fps) 
        clock.tick(fps)
        t.append(pg.time.get_ticks()/1000)

    pg.quit()
    t = np.array(t)
    t -= t[0]

    tstep = 1/fps
    n = t.size
    fft = np.fft.fft(x, n)
    psd = fft * np.conj(fft)/n
    freq = (1/(tstep*n))*np.arange(n)
    L = np.arange(1, np.floor(n/2), dtype='int')
    plt.plot(freq[L], psd[L])
    plt.xlim(freq[1], 1)
    freq = freq[1+np.where(psd[L] == np.amax(psd[L]))[0]]
    print(freq)
    plt.show()
    #print((30*4*np.pi**2)/T**2)
    plt.plot(t, 50*np.sin(2*np.pi*freq*t+3*np.pi/2) + 150)
    plt.plot(t, x)
    plt.show()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
