from PIL import Image
from warnings import warn
import heapq


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent# исходная для текущей нода
        self.position = position
        self.g = self.h = self.f = 0
    def __eq__(self, other):
        return self.position == other.position
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"
    def __lt__(self, other):#параметры для правильной расстановки приоритетов
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):# возврат обратного пути
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def astar(maze, start, end, allow_diagonal_movement=False):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)
    outer_iterations = 0
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)
    while len(open_list) > 0:
        outer_iterations += 1
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        if current_node == end_node:
            return return_path(current_node)
        children = []
        for new_position in adjacent_squares:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue
            child.g = current_node.g + (((child.position[0] - child.parent.position[0]) ** 2) + (
                        (child.position[1] - child.parent.position[1]) ** 2)) ** 0.5
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)) ** 0.5
            child.f = child.g + child.h
            if child in open_list:
                idx = open_list.index(child)
                if child.g < open_list[idx].g:
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                heapq.heappush(open_list, child)

    warn("Path not found")
    return None


def demonstration(print_maze=False, save_img=True):#обработка карты
    maze, width, height = img2maze("Test1.png")
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    path = astar(maze, start, end)

    if save_img and path:
        img = []
        for step in path:
            maze[step[0]][step[1]] = 2

        for line in maze:
            for pix in line:
                if pix == 0:
                    img.append((255, 255, 255))
                elif pix == 1:
                    img.append((0, 0, 0))
                elif pix == 2:
                    img.append((255, 0, 0))

        image_out = Image.new("RGB", (width, height))
        image_out.putdata(img)
        image_out.save('test_out2.png')

    if print_maze and path:
        for step in path:
            maze[step[0]][step[1]] = 2

        for row in maze:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append(".")
            print("".join(line))

    print(path)


def img2maze(filename_img: str):
    img = Image.open(filename_img)
    width, height = img.size
    pixels = list(img.getdata())
    for i, x in enumerate(pixels):
        if x == (255, 255, 255) or x == (255, 255, 255, 255):#резервный параметр для альфа канала в некоторых файлах
            pixels[i] = 0
        else:
            pixels[i] = 1
    maze = [pixels[i:i + width] for i in range(0, len(pixels), width)]
    return maze, width, height

demonstration()
