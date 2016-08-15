import math

def rad2deg(x):
    return ((x*180)/math.pi)

def deg2rad(x):
    return ((x*math.pi)/180)

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
