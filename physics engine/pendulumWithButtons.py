import pygame as pg
import pymunk as pm
import pymunk.pygame_util as dw
from numpy import pi, sin, cos
from buttons import *

# ----------pygame initialization----------
pg.init()
WIDTH, HEIGHT = 500, 500
window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
# ----------end pygame initialization----------


# ----------button setup----------
pause_img = pg.image.load('icons/pause1.png').convert_alpha()
resume_img = pg.image.load('icons/play.png').convert_alpha()
restart_img = pg.image.load('icons/restart.png').convert_alpha()

button.screen = window

pauseButton = button(10, 20, pause_img, 0.03)
resumeButton = button(10, 20, resume_img, 0.03, show=False)
restartButton = button(40, 20, restart_img, 0.03)
# ----------button setup----------

# ----------draw/update function----------
def draw(space, window, draw_options, buttons):
    window.fill("black") #background color
    space.debug_draw(draw_options)
    for button in buttons:
        if button.show:
            button.drawButton()
    pg.display.update()
# ----------end draw/update function----------

# ----------pause function----------
def pause():
    paused = True
    pauseButton.show = False
    resumeButton.show = True
    while paused:
        resumeButtonStatus = resumeButton.trigger()
        restartButtonStatus = restartButton.trigger()
        if resumeButtonStatus:
            # pauseButton.show = True
            # resumeButton.show = False
            # pg.display.update()
            paused = False
        elif restartButtonStatus:
            restart()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()
        # clock.tick(5)
# ----------end pause function----------

# ----------restart function----------
def restart(space, initialConditions):
    '''
    works, but only when simulation is running
    '''
    space.bodies[0].position , space.bodies[0].velocity = initialConditions
    pg.display.update()
# ----------end restart function----------

def create_pendulum(space, initAngle, L, second_body=None):
    global WIDTH, HEIGHT
    body = pm.Body()
    body.position = (L*sin(initAngle)+WIDTH/2, L*cos(initAngle))
    circle = pm.Circle(body, 20)
    circle.mass = 30
    circle.elasticity = 1
    if second_body:
        rotation_center_joint = pm.PinJoint(body, second_body, (0,0))
    else:
        rotation_center_body = pm.Body(body_type=pm.Body.STATIC)
        rotation_center_body.position = (WIDTH/2, 0)
        rotation_center_joint = pm.PinJoint(body, rotation_center_body, (0,0))

    space.add(circle, body, rotation_center_joint)


def run(window, width, height):
    run = True
    fps = 60

    space = pm.Space()
    space.gravity = (0, 981)
    L = 450
    initAngle = 20 #degrees
    initAngleRadians = initAngle*2*pi/360
    create_pendulum(space, initAngleRadians, L)
    IC = [space.bodies[0].position, space.bodies[0].velocity]

    draw_options = dw.DrawOptions(window)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     pauseButton.trigger()
            
        buttonList = [resumeButton, pauseButton, restartButton]
        draw(space, window, draw_options, buttonList)


        # ----------check buttons status----------
        if pauseButton.trigger():
            
        elif restartButton.trigger():
            restart(space, IC)
        # ----------check buttons status ended----------        
        space.step(1/fps) 
        clock.tick(fps)
    

    pg.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
