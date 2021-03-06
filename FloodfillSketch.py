class Node:
    def init(is_white,x,y):
        self.is_white = is_white
        self.x = x
        self.y = y

def convert_to_node(img,x,y):
    r,g,b = image.getpixel((x,y))
    if r = 255:
        is_white = true
    else:
        is_white = false
    point = Node(is_white,x,y)
    return point

def floodfill(image,x,y):
    cur_point = convert_to_node(image,x,y)
    north = convert_to_node(image,x,y+1)
    south = convert_to_node(image,x,y-1)
    east = convert_to_node(image,x+1,y)
    west = convert_to_node(image,x-1,y)

    Q = []
    Q.append(cur_point)
    last_x, last_y = x,y

    while Q.count > 0:
        n = Q.pop(0)
        last_x = n.x
        last_y = n.y
        if n.is_white = true:
            n.is_white = false
            Q.append(west)
            Q.append(east)
            Q.append(north)
            Q.append(south)
    return last_x,last_y