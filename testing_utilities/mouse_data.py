from pynput.mouse import Controller
import matplotlib.pyplot as plt
import keyboard
import time


mouse = Controller()
start = False
while True:
    xpoints = []
    ypoints = []
    in_loop = False
    old_pos = mouse.position
    old_time = time.time()

    if keyboard.is_pressed('ctrl'):
        start = True
        print('starting')

    while start:
        time.sleep(.1)
        time_change = time.time() - old_time
        old_time = time.time()
        pos = mouse.position
        x_disp = abs(pos[0] - old_pos[0])
        y_disp = abs(pos[1] - old_pos[1])
        old_pos = pos
        x_vel = (x_disp / time_change) * .1
        y_vel = (y_disp / time_change) * .1
        print(f"Moved {y_disp} in {time_change}. Velocity: {y_vel}")
        #xpoints.append(pos[0])
        ypoints.append(y_vel)
        xpoints.append(x_vel)
        if keyboard.is_pressed('alt'):
            start = False
            print('ended')



    if xpoints:
        # with open('mouse_data.txt', 'w') as f:
        #     for i in xpoints:
        #         f.write(str(i) + '\n')
        yAxis = xpoints
        xAxis = [0 + i for i in range(len(yAxis))]
        plt.plot(xAxis, yAxis)
        plt.plot(xAxis, ypoints)
        plt.title('Velocity')
        plt.xlabel('Time')
        plt.ylabel('Velocity')
        plt.xlim([0, 100])
        plt.ylim([0, 200])
        plt.show()


