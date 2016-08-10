import math


def cut_horizontal (p_x,p_y, p_t, c_x, c_y, c_t): #cuts a horizontal line with a vertical line

    if ((p_x <= c_x and p_t <= c_x) or (p_x >= c_x and p_t >= c_x)):
            return (p_t, p_y)

    if ((c_y <= p_y and c_t <= p_y) or (c_y >= p_y and c_t >= p_y)):
            return (p_t, p_y)

    if p_t > c_x:
        return (c_x-1, p_y)
    else:
        return (c_x+1, p_y)


def cut_vertical(p_x, p_y, p_t, c_x, c_y, c_t):  # cuts a vertical line with a horizontal line
    if ((p_y <= c_y and p_t <= c_y) or (p_y >= c_y and p_t >= c_y)):
        return (p_x, p_t)
    if ((c_x <= p_x and c_t <= p_x) or (c_x >= p_x and c_t >= p_x)):
        return (p_x, p_t)

    if p_t > c_y:
        return (p_x, c_y-1)
    else:
        return (p_x , c_y+1)

def reduce_line2 ( p, t, rect ):
    rect1_x = rect.topleft[0]     #horizontal
    rect1_y = rect.topleft[1]
    rect1_t = rect.bottomright[0]

    rect2_x = rect.topleft[0]     #horizontal
    rect2_y = rect.bottomright[1]
    rect2_t = rect.bottomright[0]

    rect3_x = rect.topleft[0]     #vertical
    rect3_y = rect.topleft[1]
    rect3_t = rect.bottomright[1]

    rect4_x = rect.bottomright[0] #vertical
    rect4_y = rect.topleft[1]
    rect4_t = rect.bottomright[1]

    px_x = p[0]
    px_y = p[1]
    px_t = t[0]

    py_x = p[0]
    py_y = p[1]
    py_t = t[1]

    tx = cut_horizontal(px_x,px_y,px_t,rect3_x,rect3_y,rect3_t)
    tx = cut_horizontal(px_x,px_y,tx[0],rect4_x,rect4_y,rect4_t)

    ty = cut_vertical(py_x,py_y,py_t,rect1_x,rect1_y,rect1_t)
    ty = cut_vertical(py_x,py_y,ty[1],rect2_x,rect2_y,rect2_t)

    if((tx[0],ty[1])!=t):
        print("rect 1 : %d %d %d" % (rect1_x, rect1_y, rect1_t))
        print("rect 2 : %d %d %d" % (rect2_x, rect2_y, rect2_t))

        print("rect 3 : %d %d %d" % (rect3_x, rect3_y, rect3_t))
        print("rect 4 : %d %d %d" % (rect4_x, rect4_y, rect4_t))

        print("px : %d %d %d" % (px_x, px_y, px_t))
        print("py : %d %d %d" % (py_x, py_y, py_t))

    return (tx[0],ty[1])

def cut_line_x (p_x,p_y,t_x,t_y,start,dist,x):

    v_x = t_x-p_x
    v_y = t_y-p_y

    if (abs(v_x) <= 1):
        return (t_x, t_y)

    y = int(((x - p_x) / v_x) * v_y + p_y)

    if(y < start and y > start+dist):
        return (x,y)
    else:
        return (t_x, t_y)

def cut_line_y (p_x,p_y,t_x,t_y,start,dist,y):

    v_x = t_x - p_x
    v_y = t_y - p_y

    if(abs(v_y) <= 1):
        return (t_x, t_y)

    x = int(((y - p_y) / v_y) * v_x + p_x)

    if(x < start and x < start+dist):
        return (x,y)
    else:
        return (t_x, t_y)

def reduce_line ( p, t, rect ):
    (a1, b1) = cut_line_y(p[0],p[1],t[0],t[1],rect.topleft[0],rect.bottomright[0]-rect.topleft[0],rect.topleft[1])
    (a2, b2) = cut_line_y(p[0], p[1], a1, b1, rect.topleft[0], rect.bottomright[0] - rect.topleft[0],
                          rect.bottomright[1])
    (a3, b3) = cut_line_x(p[0], p[1], a2, b2, rect.topleft[1], rect.bottomright[1] - rect.topleft[1],
                          rect.topleft[0])
    (a4, b4) = cut_line_x(p[0], p[1], a3, b3, rect.topleft[1], rect.bottomright[1] - rect.topleft[1],
                          rect.bottomright[0])

    return (a4,b4)

def rect_intersect(rect1, rect2):
    flag = 0
    if rect1.topleft[0] >= rect2.topleft[0] \
            and rect1.topleft[0] <= rect2.bottomright[0]:
        flag = 1
    if rect1.bottomright[0] >= rect2.topleft[0] \
            and rect1.bottomright[0] <= rect2.bottomright[0]:
        flag = 1
    if flag == 1:
        if rect1.topleft[1] >= rect2.topleft[1] \
                and rect1.topleft[1] <= rect2.bottomright[1]:
            return True
        if rect1.bottomright[1] >= rect2.topleft[1] \
                and rect1.bottomright[1] <= rect2.bottomright[1]:
            return True
    return False

def point_inside_rect(point, rect):
    if point[0] > rect.topleft[0] and point[0] < rect.bottomright[0]:
        if point[1] > rect.topleft[1] and point[1] < rect.bottomright[1]:
            return True
    return False

def point_in_rect(point , rect):
    if point[0] >= rect.topleft[0] and point[0] <= rect.bottomright[0]:
        if point[1] >= rect.topleft[1] and point[1] <= rect.bottomright[1]:
            return True
    return False

def point_on_rect(point, rect):
    if point[0] >= rect.topleft[0] and point[0] <= rect.bottomright[0]:
        if point[1] >= rect.topleft[1] and point[1] <= rect.bottomright[1]:
            if not point_inside_rect(point, rect):
                return True
    return False

def get_intersecting_line_tuples(rect1, rect2):
    player_left =  rect1.topleft[0] >= rect2.topleft[0] \
                   and rect1.topleft[0] <= rect2.bottomright[0]
    player_right =  rect1.bottomright[0] >= rect2.topleft[0] \
                    and rect1.bottomright[0] <= rect2.bottomright[0]
    player_upper =  rect1.topleft[1] >= rect2.topleft[1] \
                    and rect1.topleft[1] <= rect2.bottomright[1]
    player_lower =  rect1.bottomright[1] >= rect2.topleft[1] \
                    and rect1.bottomright[1] <= rect2.bottomright[1]
    return (player_left, player_right, player_upper, player_lower)

def get_intersecting_lines(rect1, rect2):
    horizontal_y = -1
    vertical_x = -1

    (player_left, player_right, player_upper, player_lower) = \
        get_intersecting_line_tuples(rect1, rect2)

    if player_left:
        vertical_x = rect2.right
    elif player_right:
        vertical_x = rect2.left

    if player_upper:
        horizontal_y = rect2.bottom
    elif player_lower:
        horizontal_y = rect2.top

    return (vertical_x, horizontal_y)

def get_inner_point(player_rect, intersecting_rect):

    (player_left, player_right, player_upper, player_lower) = \
        get_intersecting_line_tuples(player_rect, intersecting_rect)

    point = None

    if player_left:
        if player_upper:
            point = player_rect.topleft
        elif player_lower:
            point = player_rect.bottomleft
    if player_right:
        if player_upper:
            point = player_rect.topright
        elif player_lower:
            point = player_rect.bottomright

    return (point[0], point[1])

def push_out(x, y, rect):
    if point_in_rect((x,y),rect):
        minx = min([abs(x-rect.topleft[0]), abs(rect.bottomright[0]-x)])
        miny = min([abs(y-rect.topleft[1]), abs(rect.bottomright[1]-y)])

        if minx < miny:
            if abs(x-rect.topleft[0]) < abs(rect.bottomright[0]-x):
                x = rect.topleft[0]-1
            else:
                x = rect.bottomright[0]+1
        else:
            if abs(y - rect.topleft[1]) < abs(rect.bottomright[1] - y):
                y = rect.topleft[1]-1
            else:
                y = rect.bottomright[1]+1

    return (x,y)


def get_target_point(vertical_x, horizontal_y, v_x, v_y, p_x, p_y):

    print("args: %d %d %d %d %d %d" % (vertical_x,horizontal_y,v_x,v_y,p_x,p_y))

    if (v_y > 0):
        horizontal_y = horizontal_y + 1
        print("down")
    elif(v_y < 0):
        horizontal_y = horizontal_y - 1
        print("up")

    if (v_x > 0):
        print("right")
        vertical_x = vertical_x + 1
    elif (v_x < 0):
        print("left")
        vertical_x = vertical_x - 1

    if(v_x==v_y==0):
        print("same")

    if(v_x==0 and v_y==0):
        print("ERROR vel is 0")
        return (p_x-1,p_y-1)

    #slope is 0 or 90?
    if v_x == 0:
        if abs(vertical_x - p_x) < 1: #hack to allow walking
            return (p_x,p_y-1)
        return (p_x , horizontal_y)
    elif v_y == 0:
        if abs(horizontal_y - p_y) < 1: #hack to allow walking
            return (p_x-1,p_y)
        return (vertical_x, p_y)

    #get points
    x = int(((horizontal_y - p_y)/v_y) * v_x + p_x)
    y = int(((vertical_x - p_x) / v_x) * v_y + p_y)

    #check dist
    d_vertical_x = (vertical_x - p_x) ** 2 + (y - p_y) ** 2
    d_horizontal_y = (x - p_x) ** 2 + (horizontal_y - p_y) ** 2
    if d_horizontal_y < d_vertical_x:
        return (x, horizontal_y)
    else:
        return (vertical_x, y)
