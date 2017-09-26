'''
  |__ \ / ____/  /_  __/   | / ____/ / / / __ \/ ___/   _____   <  /  _________ ___
  __/ //___ \     / / / /| |/ /   / /_/ / / / /\__ \   /____/   / /  / ___/ __ `__ \
 / __/____/ /    / / / ___ / /___/ __  / /_/ /___/ /  /____/   / /  / /__/ / / / / /
/__________/ _________/  _________/_______________/         ____/   \___/_/ /_/ /_/
   / ____/  /_  __/   | / ____/ / / / __ \/ ___/   _____   <  /  ____/ /__  ____ _________  ___
  /___ \     / / / /| |/ /   / /_/ / / / /\__ \   /____/   / /  / __  / _ \/ __ `/ ___/ _ \/ _ \
 ____/ /    / / / ___ / /___/ __  / /_/ /___/ /  /____/   / /  / /_/ /  __/ /_/ / /  /  __/  __/
/_____/    /_/ /_/  |_\____/_/ /_/\____//____/           /_/   \__,_/\___/\__, /_/   \___/\___/
                                                                         /____/
'''




import nxt
from nxt.sensor.generic import Touch, Ultrasonic, Color20
from nxt.motor import Motor
from nxt import motor

brick = nxt.locator.find_one_brick()
from nxt.sensor import common
import os

colors = {'black': 1, 'blue' : 2, 'green':3, 'yellow':4,'red':5,'white':6}

LEFT = 0x00
RIGHT = 0x01


def turn_motors(motor_left, motor_right, degrees, direction=LEFT, power=64, powerEnd = 64 ):
    first_read_right = motor_right._read_state()[1].tacho_count
    first_read_left = motor_left._read_state()[1].tacho_count
    if direction==LEFT:
        leader_motor =  motor_right
        leader_measure = first_read_right
        follower_motor = motor_left
    else:
        leader_motor = motor_left
        leader_measure = first_read_left
        follower_motor = motor_right
    leader_motor.run(power)
    follower_motor.idle()

    while (leader_motor._read_state()[1].tacho_count - leader_measure < degrees*5):
        pass
    leader_motor.run(powerEnd)
    follower_motor.run(powerEnd)

try:
    print 'Teste Cor'
    #my_touch_sensor = Touch(brick=brick,port=common.PORT_1)
    # my_ultrasonic_sensor = Ultrasonic(brick=brick,port=common.PORT_2)
    my_color20_sensor = Color20(brick=brick, port=common.PORT_3)
    my_motor_left = Motor(brick=brick,port=motor.PORT_A)
    my_motor_right = Motor(brick=brick, port=motor.PORT_B)
    #my_motor_left.run(64)
    #my_motor_right.run(64)

    '''
    if not os.path.isfile("Output_color_sensor.txt"):
        output = 'reading\tmeasurement_unit\n'
    else:
        output = ''
    '''

    while (True):
        first_read = 0

        # sensor de contato
        ''' if(my_sensor.is_pressed()):
            print True
        '''
        # sonar
        '''result = str(my_ultrasonic_sensor.get_distance()) +  '\t' +\
                 my_ultrasonic_sensor.get_measurement_units()+'\n'
        output += result
        print result
        time.sleep(1)
        '''

        #print my_color20_sensor.get_color()
        #print my_motor_right._read_state()[1].tacho_count #contador do motor
        # luminosidade
        if(my_color20_sensor.get_color() == colors['black']):
            my_motor_right.reset_position(True)
            my_motor_left.reset_position(True)
            first_read_right = my_motor_right._read_state()[1].tacho_count
            first_read_left =  my_motor_right._read_state()[1].tacho_count #valor do contador no momento que detecta a cor vermelha
            #my_motor_left.run(64)
            #my_motor_right.run(64)
            #my_motor_right.weak_turn(64,1000)
            #my_motor_left.idle()
            #print my_motor_right._read_state()[1].tacho_count
            #while (my_motor_right._read_state()[1].tacho_count - first_read < 180): #terminou de girar?
                #pass
            while (my_motor_right._read_state()[1].tacho_count - first_read_right < 250):
                print str(first_read_right) + ' ' + str(my_motor_right._read_state()[1].tacho_count)
                print str(first_read_left) + ' ' + str(my_motor_left._read_state()[1].tacho_count)
            #my_motor_left.run(64)
            #my_motor_right.run(64)
            my_motor_left.idle()
            my_motor_right.idle()

        #print my_motor._read_state()[1]


except KeyboardInterrupt:
    #luminosidade

    #print my_color20_sensor.get_color()

    # o motor para ao clicar ctrl+c
    my_motor_left.idle()
    my_motor_right.idle()
    '''text_file = open("Output.txt", "a")

    text_file.write(output)

    text_file.close()
    '''


