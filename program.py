from tkinter import *
from heapq import *
from collections import deque
from random import shuffle
from math import sin, cos, floor

canvas_size = 800

col = "rainbow"
bg_col = "black"
time = 0.0
checks = 0


def update_canvas(l, ms=2):
    canvas.delete("all")
    global bg_col
    canvas.config(bg=bg_col)
    color = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    for i in range(len(l)):
        global col
        c = ""
        if col == "rainbow":
            c = color[floor((l[i] / (canvas_size / 7)) % 7)]
        else:
            c = col
        global c_vis
        if c_vis == "Linear Points":
            canvas.create_oval(i-2, canvas_size - l[i]-2, i+2, canvas_size - l[i]+2, fill=c)
        elif c_vis == "Linear Bars":
            canvas.create_line(i, canvas_size, i, canvas_size - l[i], width=1, fill=c)
        elif c_vis == "Spiral":
            npos_x = cos(l[i]) * (canvas_size * ((i / canvas_size) / 2.25))
            npos_y = sin(l[i]) * (canvas_size * ((i / canvas_size) / 2.25))
            canvas.create_oval((canvas_size / 2) + npos_x + 2, (canvas_size / 2) + npos_y + 2,
                               (canvas_size / 2) + npos_x - 2, (canvas_size / 2) + npos_y - 2, fill=c)
    global time
    global checks
    time += 0.02028 / ms
    checks += 1
    txt_time["text"] = "Time: {} milliseconds / {} seconds\nChecks: {}\nItems: {}".format(round(time, 5), round(time / 1000, 6), checks, canvas_size)
    canvas.update()
    canvas.after(ms)


def atomize(l):
    return deque(
        map(
            lambda x: deque([x]),
            l if l is not None else []
        )
    )


def merge(l, r):
    res = deque()
    while (len(l) + len(r)) > 0:
        if len(l) < 1:
            res += r
            r = deque()
        elif len(r) < 1:
            res += l
            l = deque()
        else:
            res.append(l.popleft()) if l[0] <= r[0] else res.append(r.popleft())
    return res


def merge_sort(l):
    atoms = atomize(l)
    while len(atoms) > 1:
        atoms.append(merge(atoms.popleft(), atoms.popleft()))
        update_canvas([num for atom in atoms for num in atom], 10)
    return list(atoms[0])


def selection_sort(l):
    for i in range(len(l)):
        min_idx = i
        for j in range(i + 1, len(l)):
            if l[min_idx] > l[j]:
                min_idx = j
        l[i], l[min_idx] = l[min_idx], l[i]
        update_canvas(l, 5)


def insertion_sort(l):
    for i in range(1, len(l)):
        key = l[i]
        j = i - 1
        while j >= 0 and key < l[j]:
            l[j + 1] = l[j]
            update_canvas(l, 1)
            j -= 1
        l[j + 1] = key
        update_canvas(l, 5)


def radix_sort(l):
    steps = len(str(max(l)))
    for d in range(steps):
        q = 10 ** d
        buckets = [[] for i in range(10)]
        for x in l:
            buckets[(x // q) % 10].append(x)
            update_canvas([y for bucket in buckets for y in bucket])
        l = [y for bucket in buckets for y in bucket]
    return l


def partition(arr, l, h):
    i = (l - 1)
    x = arr[h]
    for j in range(l, h):
        if arr[j] <= x:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            update_canvas(arr, 1)
    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)


def quick_sort(l):
    le = 0
    h = len(l) - 1
    size = h - le + 1
    stack = [0] * (size)
    top = -1
    top = top + 1
    stack[top] = le
    top = top + 1
    stack[top] = h
    while top >= 0:
        h = stack[top]
        top = top - 1
        le = stack[top]
        top = top - 1
        p = partition(l, le, h)
        if p - 1 > le:
            top = top + 1
            stack[top] = le
            top = top + 1
            stack[top] = p - 1
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
        update_canvas(l, 15)


def heap_sort(l):
    H = []
    for x in l:
        heappush(H, x)
    for i in range(len(l)):
        l[i] = heappop(H)
        update_canvas(l)


def slow_sort(l):
    '''
    O(n^2)
    O(1) in memory usage
    '''
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            update_canvas(l)
            if l[j] < l[i]:
                l[i], l[j] = l[j], l[i]


def bogosort(l):
    '''
    O(n!)
    '''
    while True:
        shuffle(l)
        for i in range(len(l)-1):
            update_canvas(l)
            if l[i + 1] < l[i]:
                break
        else:
            return


algs_dict = {
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Merge Sort": merge_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Radix Sort": radix_sort,
    "Slow Sort": slow_sort,
    "Bogosort": bogosort
}
algs = [
    "Quick Sort",
    "Heap Sort",
    "Merge Sort",
    "Insertion Sort",
    "Selection Sort",
    "Radix Sort",
    "Slow Sort",
    "Bogosort"
]
viss = [
    "Linear Points",
    "Linear Bars",
    "Spiral"
]
c_alg = "Quick Sort"
c_vis = "Linear Points"


"""
Menus with
1. Algorithm:
2. Visualization:
"""


def update_text():
    global c_vis
    global c_alg
    txt["text"] = "Algorithm: {}\nVisualization: {}".format(c_alg, c_vis)


def set_vis(x):
    global c_vis
    c_vis = x
    update_text()
    update_canvas([i for i in range(canvas_size)], 1)


def set_alg(x):
    global c_alg
    c_alg = x
    update_text()


def set_cols(x):
    global bg_col
    global col
    if x[0] == "b":
        bg_col = "black"
    elif x[0] == "w":
        bg_col = "white"
    if x[1] == "b":
        col = "black"
    elif x[1] == "w":
        col = "white"
    elif x[1] == "r":
        col = "rainbow"


def go():
    global c_alg
    l = [i for i in range(canvas_size)]
    shuffle(l)
    global time
    global checks
    time = 0
    checks = 0
    update_canvas(l)
    algs_dict[c_alg](l)


root = Tk()

root.title("Sorting Visualizer")

menubar = Menu(root)
vismenu = Menu(menubar, tearoff=0)
vismenu.add_command(label=viss[0], command=lambda: set_vis(viss[0]))
vismenu.add_command(label=viss[1], command=lambda: set_vis(viss[1]))
vismenu.add_command(label=viss[2], command=lambda: set_vis(viss[2]))
menubar.add_cascade(label="Visualizations", menu=vismenu)
algmenu = Menu(menubar, tearoff=0)
algmenu.add_command(label=algs[0], command=lambda: set_alg(algs[0]))
algmenu.add_command(label=algs[1], command=lambda: set_alg(algs[1]))
algmenu.add_command(label=algs[2], command=lambda: set_alg(algs[2]))
algmenu.add_command(label=algs[3], command=lambda: set_alg(algs[3]))
algmenu.add_command(label=algs[4], command=lambda: set_alg(algs[4]))
algmenu.add_command(label=algs[5], command=lambda: set_alg(algs[5]))
algmenu.add_command(label=algs[6], command=lambda: set_alg(algs[6]))
algmenu.add_command(label=algs[7], command=lambda: set_alg(algs[7]))
menubar.add_cascade(label="Algorithms", menu=algmenu)
colormenu = Menu(menubar, tearoff=0)
colormenu.add_command(label="White (black bg)", command=lambda: set_cols("bw"))
colormenu.add_command(label="Black (white bg)", command=lambda: set_cols("wb"))
colormenu.add_command(label="Rainbow (black bg)", command=lambda: set_cols("br"))
colormenu.add_command(label="Rainbow (white bg)", command=lambda: set_cols("wr"))
menubar.add_cascade(label="Colors", menu=colormenu)
readymenu = Menu(menubar, tearoff=0)
readymenu.add_command(label="Go", command=go)
readymenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Ready", menu=readymenu)
root.config(menu=menubar)

canvas = Canvas(width=canvas_size, height=canvas_size, bg='black')
canvas.grid(row=1)
txt = Label(root, text="Algorithm: {}\nVisualization: {}".format(c_alg, c_vis))
txt.grid(row=0)
txt_time = Label(root, text="Time: 0 milliseconds / 0 seconds\nChecks: 0\nItems: 0")
txt_time.grid(row=2)


mainloop()
