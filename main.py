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
    ''' 
        return a list of Actors of type ground starting at (x,y) and being
        at least width wide 
    '''
    ground = []
    for i in range(int(width / images.ground.get_width())):
        ground.append(Actor('ground',
            topleft=(x + images.ground.get_width() * i, y)))
    return ground

def collide(rect1, dx, dy, rect2):
    '''
        Check if rect1 will collide with rect2, specifically to check that
        when it moves by dx left or right and dy up or down that
        - rect1 is on top of rect2 (standing)
        - rect1 is to the left or right of rect2 (blocked from moving that way)
        - rect1 is underneath rect2 (underneath and bumping up into it)

        return:
        - (Standing, ypos)
        - (LeftOf, xpos)
        - (RightOf, xpos)
        - (Under, ypos)
    '''
    testrect = rect1.copy().move(dx, dy)
    if testrect.colliderect(rect2):
        botoverlap = testrect.bottom - rect2.top
        topoverlap = rect2.bottom - testrect.top
        rightoverlap = testrect.right - rect2.left
        leftoverlap = rect2.right - testrect.left
        #print("Bot=%f Top=%f Left=%f Right=%f dx=%f dy=%f" % (botoverlap, topoverlap, leftoverlap, rightoverlap, dx, dy))
        if botoverlap > 0 and botoverlap <= abs(dy):
            # standing on rect2
            return ('standing', rect2.top)
        elif topoverlap > 0 and topoverlap <= abs(dy):
            # bumping up into rect2
            return ('under', rect2.bottom)
        elif rightoverlap > 0 and rightoverlap <= abs(dx):
            # bumped into rect2 on our right
            return ('leftof', rect2.left)
        elif leftoverlap > 0 and leftoverlap <= abs(dx):
            # dumped into rect2 on our left
            return ('rightof', rect2.right)
        else:
            print("Collision detection fail!")
    else:
        return None

p1 = Actor('p1_front')
p1.pos = 100, 56
p1.vy = 0
p1.vx = 0
p1.on_land = False
p1.walkindex = 0
p1.keyleft = False
p1.keyright = False

p1walk = ['p1_walk%02d' % (n + 1) for n in range(11)]
p1walkl = ['p1_walkl%02d' % (n + 1) for n in range(11)]
grounds = []
grounds += make_ground(0, HEIGHT - images.ground.get_height(), WIDTH+50)
grounds += make_ground(400, 400, 400)
grounds += make_ground(25, 250, 250)
grounds += make_ground(450, 150, 200)

def on_key_down(key):
    if key == keys.UP and p1.on_land:
        p1.vy = JUMPSPEED
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
    p1.on_land = False
    # calculate how far we will move left or right
    dx = p1.vx
    # Calculate how far we will move up or down, 
    # if we're moving at speed vy under influence of gravity
    uy = p1.vy
    p1.vy += GRAVITY
    dy = (uy + p1.vy) / 2

    for g in grounds:
        result = collide(p1, dx, dy, g)
        if result:
            if result[0]=='standing':
                p1.on_land = True
                # Correct our y position to be on top of the block
                p1.bottom = g.top-1
                if p1.vy > 0:
                    # if we're standing on something, just slow our speed by the
                    # amount we increased it or we will alternate between standing and not
                    # and be unable to jump
                    p1.vy -= GRAVITY
                dy = 0
            elif result[0]=='under':
                print("hit my head!")
                # if we've jumped upward and hit a block then stop going up and start falling
                p1.top = g.bottom+1
                p1.vy = BUMPSPEED
                dy = 0
            elif result[0]=='leftof':    
                print("sideways block hit")
                # if we're walking sideways and hit a block then stop
                p1.vx = 0
                p1.right = g.left-1
                dx = 0
            elif result[0]=='rightof':
                print("sideways block hit")
                # if we're walking sideways and hit a block then stop
                p1.vx = 0
                p1.left = g.right+1
                dx = 0

    p1.x += dx
    p1.y += dy

    if p1.vx == 0:
        # If standing still show the front facing image
        p1.image = 'p1_front'
        p1.walkindex = 0
    elif p1.vx > 0:
        # If walking to the right, show each right facing image in sequence to animate
        old_height = p1.height
        old_width = p1.width
        p1.image = p1walk[p1.walkindex]
        # not all the images are the same size, which can cause us to move through
        # blocks if we don't correct for it
        p1.x -= p1.width - old_width
        p1.y -= p1.height - old_height
        p1.walkindex += 1
        if p1.walkindex > len(p1walk)-1:
            p1.walkindex = 0
    elif p1.vx < 0:
        # If walking to the left, show the left images in sequence
        old_height = p1.height
        old_width = p1.width
        p1.image = p1walkl[p1.walkindex]
        p1.x += p1.width - old_width
        p1.y -= p1.height - old_height
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

