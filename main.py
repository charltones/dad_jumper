import pgzrun

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.3
P1WALK = 3
JUMPSPEED = -10
BUMPSPEED = 1
# we stand this many units below top of ground block
STANDPOS = 5
# we need to bump this many units below or above the top to register as a side bump
BUMPPOS = 8

def make_ground(x, y, width):
    ground = []
    for i in range(int(width / images.ground.get_width())):
        ground.append(Actor('ground',
            topleft=(x + images.ground.get_width() * i, y)))
    return ground

p1 = Actor('p1_front')
p1.pos = 100, 56
p1.vy = 0
p1.vx = 0
p1.on_land = False
p1.jump = False
p1.walkindex = 0
p1.keyleft = False
p1.keyright = False

p1walk = ['p1_walk%02d' % (n + 1) for n in range(11)]
p1walkl = ['p1_walkl%02d' % (n + 1) for n in range(11)]
grounds = []
grounds += make_ground(0, HEIGHT - images.ground.get_height(), WIDTH)
grounds += make_ground(400, 400, 400)
grounds += make_ground(25, 250, 250)
grounds += make_ground(450, 150, 200)

def on_key_down(key):
    if key == keys.UP and p1.on_land:
        p1.vy = JUMPSPEED
        p1.jump = True
    if key == keys.LEFT:
        p1.keyleft = True
        p1.vx = -1 * P1WALK
    if key == keys.RIGHT:
        p1.keyright = True
        p1.vx = P1WALK

def on_key_up(key):
    if key == keys.LEFT:
        p1.keyleft = False
        # Allow for rolling from one key to next
        if not p1.keyright:
            p1.vx = 0
    if key == keys.RIGHT:
        p1.keyright = False
        # Allow for rolling from one key to next
        if not p1.keyleft:
            p1.vx = 0

def update_player():
    on_land = False
    for g in grounds:
        # Check if the player has bumped into any of the ground objects
        if p1.colliderect(g):
            # We've collided with a ground block - now we need
            # to work out if we're above, below or to the side of it
            if p1.vx != 0 and ((p1.midbottom[1] > g.midtop[1]+BUMPPOS and p1.midbottom[1] < g.midbottom[1]-BUMPPOS) or
                               (p1.midtop[1] < g.midbottom[1]-BUMPPOS and p1.midtop[1] > g.midtop[1]+BUMPPOS)):
                print("sideways block hit")
                # if we're walking sideways and hit a block then stop
                p1.vx = 0
            elif p1.y <= g.y:
                on_land = True
                # Correct our y position to be on top of the block
                p1.midbottom = (p1.x, g.midtop[1]+STANDPOS)
            elif p1.y > g.y and not p1.on_land:
                print("hit my head!")
                # if we've jumped upward and hit a block then stop going up and start falling
                p1.midtop = (p1.x, g.midbottom[1])
                p1.vy = BUMPSPEED

    if on_land and not p1.jump:
        # We're walking or standing on a ground object
        p1.on_land = True
        p1.vy = 0
        print("on land!", p1.vx)
    else:
        # We're either falling or jumping
        if p1.jump:
            print("jumping!")
        else:
            print("falling!")
        p1.on_land = False
        p1.jump = False
        # Calculate our new y position, if we're moving at speed vy under influence of gravity
        uy = p1.vy
        p1.vy += GRAVITY
        p1.y += (uy + p1.vy) / 2

    # Move player left or right at speed vx
    p1.x += p1.vx

    if p1.vx == 0:
        # If standing still show the front facing image
        p1.image = 'p1_front'
        p1.walkindex = 0
    elif p1.vx > 0:
        # If walking to the right, show each right facing image in sequence to animate
        p1.image = p1walk[p1.walkindex]
        p1.walkindex += 1
        if p1.walkindex > len(p1walk)-1:
            p1.walkindex = 0
    elif p1.vx < 0:
        # If walking to the left, show the left images in sequence
        p1.image = p1walkl[p1.walkindex]
        p1.walkindex += 1
        if p1.walkindex > len(p1walk)-1:
            p1.walkindex = 0

def update():
    update_player()

def draw():
    screen.clear()
    p1.draw()
    for g in grounds:
        g.draw()

pgzrun.go()

