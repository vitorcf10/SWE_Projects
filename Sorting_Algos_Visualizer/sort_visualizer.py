import pygame
import random
import math
import time

# Start pygame
pygame.init()

# Drawing info class in order to keep all the drawing information stored in one variable when main function is called.
class DrawingInfo:
    # Set colors to be used
    COLOR_CONTROLS = 0,0,0
    COLOR_TITLE = 0,0,255
    SELECT1 = 0,255,0
    SELECT2 = 255,0,0
    GRAD1 = 128,128,128
    GRAD2 = 160,160,160
    GRAD3=192,192,192
    BACKGROUND_COLOR=255,255,255
    GRADIENTS =  [GRAD1, GRAD2, GRAD3]

    # Set fonts and pedding
    FONT = pygame.font.SysFont('comicsans', 25)
    LFONT = pygame.font.SysFont('comicsans', 35)
    SIDE_PADDING = 50
    TOP_PADDING = 150

    # Initiate the window pygame display with specified features
    def __init__(self, width, height, arr):
        self.width=width
        self.height=height
        self.window=pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualization')
        self.set_array(arr)
    
    # Initiate array's features
    def set_array(self, arr):
        self.arr=arr
        self.max=max(arr)
        self.min=min(arr)
        self.block_width=round((self.width - self.SIDE_PADDING)/len(arr) )# Take away the side pad from the window's width in order to get the drawable area, divide by the length of the array to know the width od each element/bar in array.
        self.block_height= math.floor((self.height - self.TOP_PADDING)/(self.max - self.min)) # Take away the top padding frow drawable area, then divide by the number of values in the range of the array. This away the block's height are dinamic.
        self.start_x=self.SIDE_PADDING//2 # Set start value for drawing in x-axis

# Generate random array with specified range and length
def generate_arr(n, min_val, max_val):
    arr=[]
    for i in range(n):
        ele=random.randint(min_val, max_val)
        arr.append(ele)
    return arr

# Draw function draws in the pygame display the application's interface
def draw(draw_info, sort_name, asc):
    # Fill background with background color
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Draw dinamic title
    title = draw_info.LFONT.render(f"{sort_name} - {'Ascending' if asc else 'Descending'}", 1, draw_info.COLOR_TITLE)
    draw_info.window.blit(title, ((draw_info.width/2 - (title.get_width()/2), 5)))

    # Draw first line of controls
    controls = draw_info.FONT.render('R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending', 1, draw_info.COLOR_CONTROLS)
    draw_info.window.blit(controls, ((draw_info.width/2 - (controls.get_width()/2), 40)))

    # Draw second line of controls
    controls2 = draw_info.FONT.render('P - Use Last Start Sorting Array', 1, draw_info.COLOR_CONTROLS)
    draw_info.window.blit(controls2, ((draw_info.width/2 - (controls2.get_width()/2), 65)))

    # Draw sorting type selection line
    typesort = draw_info.FONT.render('I - Insertion Sort | B - Bubble Sort | S - Selection Sort | C - Shell Sort', 1, draw_info.COLOR_CONTROLS)
    draw_info.window.blit(typesort, ((draw_info.width/2 - (typesort.get_width()/2), 90)))

    # Draw color palette selection line
    palette = draw_info.FONT.render('Color Palette: W - Default | X - Dark | Y - Google | Z - Ocean', 1, draw_info.COLOR_CONTROLS)
    draw_info.window.blit(palette, ((draw_info.width/2 - (palette.get_width()/2), 115)))

    # Draw the array
    draw_arr(draw_info)
    pygame.display.update()

# This function is responsible for drawing the array in draw_info.arr in the application's screen
def draw_arr(draw_info, color_pos={}, clear_bg=False):
    arr=draw_info.arr

    # Clear the background if needed
    if clear_bg:
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Draw side by side rectangles for each element in the array
    for i in range(len(arr)):
        x=draw_info.start_x + i*draw_info.block_width
        y=draw_info.height - (arr[i]-draw_info.min)*draw_info.block_height

        color = draw_info.GRADIENTS[i%3]
        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    # Update the display after drawing a new array
    if clear_bg:
        pygame.display.update()
  

# Bubble Sort implementation as a generator
def bubble_sort(draw_info, asc=True):
    arr=draw_info.arr

    for i in range(len(arr)-1):
        for j in range(len(arr)-1):
            n1=arr[j]
            n2=arr[j+1]
            if (n1>n2 and asc) or (n1<n2 and not asc):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                time.sleep(0.02)
                draw_arr(draw_info, {j:draw_info.SELECT1, j+1:draw_info.SELECT2}, True)
                yield True # This lets the execution of the function half way through and resume where yield was called. This allows the user to continuosly use the controls. Generator
    return arr

# Insertion Sort implementation as a generator
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
            time.sleep(0.02)
            draw_arr(draw_info, {i:draw_info.SELECT1, i-1:draw_info.SELECT2}, True)
            yield True
    return arr

# Selection Sort implementation as a generator
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
        
            draw_arr(draw_info, {ind:draw_info.SELECT1, target_index:draw_info.SELECT2}, True)
            
            
         # swapping the elements to sort the array
        time.sleep(0.1)
        (array[ind], array[target_index]) = (array[target_index], array[ind])
        yield True
        
    return array


# Shell Sort implementation as a generator
def shell_sort(draw_info, asc=True): 
    arr=draw_info.arr
    n=len(arr)
    gap=(n)//2
    while gap>0: 
        j=gap 
        # Check the array in from left to right 
        # Till the last possible index of j 
        while j<n: 
            i=j-gap # This will keep help in maintain gap value 
              
            while i>=0: 
                # If value on right side is already greater than left side value 
                # We don't do swap else we swap 
                if asc:
                    if arr[i+gap]>arr[i]: 
                        break
                    else: 
                        arr[i+gap],arr[i]=arr[i],arr[i+gap] 
                        time.sleep(0.02)
                        draw_arr(draw_info, {i+gap:draw_info.SELECT1, i:draw_info.SELECT2}, True)
                        yield True
                else:
                    if arr[i+gap]<arr[i]: 
                        break
                    else: 
                        arr[i+gap],arr[i]=arr[i],arr[i+gap] 
                        time.sleep(0.05)
                        draw_arr(draw_info, {i+gap:draw_info.SELECT1, i:draw_info.SELECT2}, True)
                        yield True
                i=i-gap # To check left side also 
                            # If the element present is greater than current element  
            j+=1
        gap=gap//2

# Define colors will change the application's color palette to the specified arguments.
def defineColors(draw_info, ct, cc, sel1, sel2, g1, g2, g3, bgc):
    draw_info.COLOR_CONTROLS = ct
    draw_info.COLOR_TITLE = cc
    draw_info.SELECT1 = sel1
    draw_info.SELECT2 = sel2
    draw_info.GRAD1 = g1
    draw_info.GRAD2 = g2
    draw_info.GRAD3= g3
    draw_info.BACKGROUND_COLOR= bgc
    draw_info.GRADIENTS =  [draw_info.GRAD1, draw_info.GRAD2, draw_info.GRAD3]


def main():
    cont=True 
    clk = pygame.time.Clock()
    n= 60 # Size of sorting array
    minv=0 # Lowest value in the array
    maxv=60 # Greatest value in the array

    # Initiate variables and flags
    tosort=False
    ascending=True
    sort_chosen = bubble_sort
    name_chosen = 'Bubble Sort'
    generator_chosen = None

    # Generate first array in the display
    arr=generate_arr(n, minv, maxv)
    prev=arr[:]

    # Generate the window
    draw_info=DrawingInfo(800, 600, arr)

    tick_rate = 60

    # Start the application's loop
    while cont: 

        clk.tick(tick_rate) # Maximum number of times loop will run per second (stored in tick_rate)

        # Define the generator for the sorting algorithm so the program's control is given back to the main loop
        if tosort:
            try:
                next(generator_chosen)
            except StopIteration:
                tosort=False
        else:
            draw(draw_info, name_chosen, ascending)

    

        pygame.display.update()

        # Define the events that can be performed by the user
        for event in pygame.event.get():
            # If top right corner 'x' is clicked program will exit
            if event.type==pygame.QUIT: 
                cont=False
            # If the event is not a key down do nothing
            if event.type != pygame.KEYDOWN:
                continue
            # Else follow the controls in the application's interface
            if event.key == pygame.K_r:
                arr=generate_arr(n, minv, maxv)
                tosort=False
                draw_info.set_array(arr)
            elif event.key == pygame.K_p:
                tosort=False
                draw_info.set_array(prev)
            elif event.key == pygame.K_SPACE and tosort==False:
                prev=draw_info.arr[:]
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
                sort_chosen = selection_sort
                name_chosen = 'Selection Sort'
            elif event.key == pygame.K_c and tosort==False:
                sort_chosen = shell_sort
                name_chosen = 'Shell Sort'
            elif event.key == pygame.K_x and tosort==False:
                defineColors(draw_info, [255,255,255], [255,0,0], [0,0,255], [255,255,0], [138,138,138], [170,170,170], [202,202,202], [0,0,0])
            elif event.key == pygame.K_y and tosort==False:
                defineColors(draw_info, [214,45,32], [255,255,255], [255,255,255], [214,45,32], [255,167, 0], [0,135,68], [0,87,231], [196,196,196])
            elif event.key == pygame.K_z and tosort==False:
                defineColors(draw_info, [94, 86, 86], [128, 0, 128], [255,0,0], [255,255,0], [88,102,139], [118,180,189], [150, 234, 255], [235,244,246])
            elif event.key == pygame.K_w and tosort==False:
                defineColors(draw_info, [0,0,0], [0,0,255], [0,255,0], [255,0,0], [128,128,128], [160,160,160], [192,192,192], [255,255,255])
    # If loop is broken terminate the application
    pygame.quit()

if __name__ == '__main__':
    main()


