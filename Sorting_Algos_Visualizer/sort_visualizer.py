import pygame
import random
import math
pygame.init()

class DrawingInfo:
    BLACK = 0,0,0
    WHITE = 255,255,255
    BLUE = 0,0,255
    GREEN = 0,255,0
    RED = 255,0,0
    GREY = 128,128,128
    DGRAY = 160,160,160
    DDGRAY=192,192,192
    BACKGROUND_COLOR=WHITE
    GRADIENTS =  [GREY, DGRAY, DDGRAY]

    FONT = pygame.font.SysFont('comicsans', 30)
    LFONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, arr):
        self.width=width
        self.height=height
        self.window=pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualization')
        self.set_array(arr)
    
    def set_array(self, arr):
        self.arr=arr
        self.max=max(arr)
        self.min=min(arr)
        self.block_width=round((self.width - self.SIDE_PADDING)/len(arr) )# Take away the side pad from the window's width in order to get the drawable area, divide by the length of the array to know the width od each element/bar in array.
        self.block_height= math.floor((self.height - self.TOP_PADDING)/(self.max - self.min)) # Take away the top padding frow drawable area, then divide by the number of values in the range of the array. This away the block's height are dinamic.
        self.start_x=self.SIDE_PADDING//2 # Set start value for drawing in x-axis

def generate_arr(n, min_val, max_val):
    arr=[]
    for i in range(n):
        ele=random.randint(min_val, max_val)
        arr.append(ele)
    return arr

def draw(draw_info, sort_name, asc):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LFONT.render(f"{sort_name} - {'Ascending' if asc else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(title, ((draw_info.width/2 - (title.get_width()/2), 5)))

    controls = draw_info.FONT.render('R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending', 1, draw_info.BLACK)
    draw_info.window.blit(controls, ((draw_info.width/2 - (controls.get_width()/2), 45)))

    typesort = draw_info.FONT.render('I - Insertion Sort | B - Bubble Sort | S - Selection Sort', 1, draw_info.BLACK)
    draw_info.window.blit(typesort, ((draw_info.width/2 - (typesort.get_width()/2), 75)))

    draw_arr(draw_info)
    pygame.display.update()

def draw_arr(draw_info, color_pos={}, clear_bg=False):
    arr=draw_info.arr

    if clear_bg:
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i in range(len(arr)):
        x=draw_info.start_x + i*draw_info.block_width
        y=draw_info.height - (arr[i]-draw_info.min)*draw_info.block_height

        color = draw_info.GRADIENTS[i%3]
        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()
  


def bubble_sort(draw_info, asc=True):
    arr=draw_info.arr

    for i in range(len(arr)-1):
        for j in range(len(arr)-1):
            n1=arr[j]
            n2=arr[j+1]
            if (n1>n2 and asc) or (n1<n2 and not asc):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                draw_arr(draw_info, {j:draw_info.GREEN, j+1:draw_info.RED}, True)
                yield True # This lets the execution of the function half way through and resume where yield was called. This allows the user to continuosly use the controls.
    return arr

def insertion_sort(draw_info, asc=True):
    arr=draw_info.arr
    
    for i in range(1, len(arr)):
        curr=arr[i]
        while True:
            ascending=i>0 and arr[i-1]>curr and asc
            descending=i>0 and arr[i-1]<curr and not asc

            if not ascending and not descending:
                break
            arr[i]=arr[i-1]
            i=i-1
            arr[i]=curr
            draw_arr(draw_info, {i:draw_info.GREEN, i-1:draw_info.RED}, True)
            yield True
    return arr

def selection_sort(draw_info, asc=True):
    array=draw_info.arr

    for ind in range(len(array)):
        target_index = ind
        for j in range(ind + 1, len(array)):
            # select the minimum element in every iteration
            if array[j] < array[target_index] and asc:
                target_index = j
            if array[j] > array[target_index] and not asc:
                target_index = j

            draw_arr(draw_info, {ind:draw_info.GREEN, target_index:draw_info.RED}, True)
            
            
         # swapping the elements to sort the array
        (array[ind], array[target_index]) = (array[target_index], array[ind])
        yield True
        
    return array


def main():
    cont=True
    clk=pygame.time.Clock()
    n=50
    minv=0
    maxv=100

    tosort=False
    ascending=True
    sort_chosen = bubble_sort
    name_chosen = 'Bubble Sort'
    generator_chosen = None

    arr=generate_arr(n, minv, maxv)
    draw_info=DrawingInfo(800, 600, arr)

    tick_rate = 60

    while cont:
        clk.tick(tick_rate) # Maximun number of times loop will run per second

        if tosort:
            try:
                next(generator_chosen)
            except StopIteration:
                tosort=False
        else:
            draw(draw_info, name_chosen, ascending)



        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT: # If top right corner 'x' is clicked program will exit
                cont=False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                arr=generate_arr(n, minv, maxv)
                tosort=False
                draw_info.set_array(arr)
            elif event.key == pygame.K_SPACE and tosort==False:
                tosort=True
                generator_chosen=sort_chosen(draw_info, ascending)
            elif event.key == pygame.K_a and tosort==False:
                ascending=True
            elif event.key == pygame.K_d and tosort==False:
                ascending=False
            elif event.key == pygame.K_i and tosort==False:
                sort_chosen = insertion_sort
                name_chosen = 'Insertion Sort'
            elif event.key == pygame.K_b and tosort==False:
                sort_chosen = bubble_sort
                name_chosen = 'Bubble Sort'
            elif event.key == pygame.K_s and tosort==False:
                #tick_rate=200
                sort_chosen = selection_sort
                name_chosen = 'Selection Sort'

    pygame.quit()

if __name__ == '__main__':
    main()


