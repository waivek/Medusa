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

def get_target_point(vertical_x, horizontal_y, v_x, v_y, p_x, p_y):
    #slope is 0 or 90?
    if v_x == 0:
        return (p_x, horizontal_y)
    elif v_y == 0:
        if abs(horizontal_y - p_y) < 1: #hack to allow walking
            return (p_x,p_y)
        return (vertical_x, p_y)

    #get points
    x = ((horizontal_y - p_y)/v_y) * v_x + p_x
    y = ((vertical_x - p_x) / v_x) * v_y + p_y

    #check dist
    d_vertical_x = (vertical_x - p_x) ** 2 + (y - p_y) ** 2
    d_horizontal_y = (x - p_x) ** 2 + (horizontal_y - p_y) ** 2
    if d_horizontal_y < d_vertical_x:
        return (x, horizontal_y)
    else:
        return (vertical_x, y)
