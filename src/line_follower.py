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
         .-+~~~~+-.
        /          \
        |'~~~~~~~~`|
        ||  o  o  ||
        ||  \__/  ||
        |`--------'|
        >----------<
     ,p~V          V~q,
    ,Z  /.sdbs. d7 \  N,
    Z  | 8(  )8_/P `|  N
   d'  | `YbdY'     |  `b
  |' ,.|            |., `|
  | _ /|            |~   |
.p~~TV/             ./*T~\,
|( ) \|~~~~~~~~~~~~~V ()#,|
`b'\\.|-----+--+-----\/  ~'
 `` ``|     |  |     |~+
      |     |  |     |
      |------`'------|
      |      ||      |
      |------||------|
      |      ||      |
      |______||______|
LEFT EYE = LEFT RGB SENSOR
MIDDLE EYE = MIDDLE RGB SENSOR
RIGHT EYE = RIGHT RGB SENSOR

'''

import nxt
from nxt.sensor import *
from nxt.sensor.generic import Touch, Ultrasonic, Color20
from nxt.motor import Motor, SynchronizedMotors
from nxt import motor
from collections import Counter
brick = nxt.locator.find_one_brick()
from nxt.sensor import common
import os

colors = {'black': 1, 'blue' : 2, 'green':3, 'yellow':4,'red':5,'white':6}
direction = {'LEFT' : False, 'RIGHT' : True}
LEFT = 0x00
RIGHT = 0x01
READINGS = 3
'''
seguir em linha reta uma certa distancia
'''
def go_straight(motor_left, motor_right, power=64, distance=100):
    first_read_right = motor_right._read_state()[1].tacho_count

    motor_left.run(power)
    motor_right.run(power)
    if distance is not None:
        while (motor_right._read_state()[1].tacho_count - first_read_right < distance * 25):
            pass
        motor_left.idle()
        motor_right.idle()
    else:
        return

def avoidance(my_motor_left,my_motor_right):
    KVmax = 0.64
    KVmin = 0.64
    KVmean = 0.84
    my_motor_left.idle()
    my_motor_right.idle()
    turn_motors(my_motor_left, my_motor_right, 90, direction=direction['RIGHT'], power=100 * KVmax, powerEnd=100 * KVmin,
                follower_power=None)
    go_straight(motor_left=my_motor_left, motor_right=my_motor_right, power=100 * KVmin, distance=20)
    turn_motors(my_motor_left, my_motor_right, 90, direction=direction['LEFT'], power=100 * KVmax,
                powerEnd=100 * KVmin,
                follower_power=None)
    go_straight(motor_left=my_motor_left, motor_right=my_motor_right, power=100 * KVmin, distance=1)
    my_motor_left.run(100*KVmax)
    my_motor_right.run(100*KVmax)


def read_sensors(left_eyes,middle_eyes,right_eyes):
    left_multi = []
    middle_multi = []
    right_multi = []
    for i in range(0,READINGS):
        left_multi.append(left_eyes.get_color())
        middle_multi.append(middle_eyes.get_color())
        right_multi.append(right_eyes.get_color())

    left_counter = Counter(left_multi).most_common(1)[0][0]
    middle_counter = Counter(middle_multi).most_common(1)[0][0]
    right_counter = Counter(right_multi).most_common(1)[0][0]

    return left_counter,middle_counter,right_counter


def turn_motors(motor_left, motor_right, degrees, direction=direction['LEFT'], power=64, powerEnd = 64, follower_power = 32 ):
    first_read_right = motor_right._read_state()[1].tacho_count
    first_read_left = motor_left._read_state()[1].tacho_count
    if direction==False:
        leader_motor =  motor_right
        leader_measure = first_read_right
        follower_motor = motor_left
    else:
        leader_motor = motor_left
        leader_measure = first_read_left
        follower_motor = motor_right
    leader_motor.run(power)
    if follower_power is None:
        follower_motor.idle()
    else:
        follower_motor.run(follower_power)

    while (leader_motor._read_state()[1].tacho_count - leader_measure < degrees*5):
        pass

    leader_motor.run(powerEnd)
    follower_motor.run(powerEnd)

try:
    '''
      _____  ______ ______ 
     |  __ \|  ____|  ____|
     | |  | | |__  | |__   
     | |  | |  __| |  __|  
     | |__| | |____| |     
     |_____/|______|_|                               
    '''
    print 'I have a brain...'
    print 'Eyes and Legs assemble!'
    my_ultrasonic_sensor = Ultrasonic(brick=brick,port=common.PORT_2)
    b = BaseDigitalSensor(brick=brick, port=common.PORT_3)
    left_eyes_sensor = Color20(brick=brick, port=common.PORT_3)
    right_eyes_sensor = Color20(brick=brick, port=common.PORT_4)
    middle_eyes_sensor = Color20(brick=brick, port=common.PORT_1)

    print 'I can see...'

    my_motor_left = Motor(brick=brick,port=motor.PORT_A)
    my_motor_right = Motor(brick=brick, port=motor.PORT_B)

    print 'I can walk... lets do this!'

    KVmax = 1.24 #velocidade na reta
    KVmin = 0.64 #velocidade reversa
    KVmean = 0.84 #velocidade maior na curva
    '''
      __  __          _____ _   _ 
     |  \/  |   /\   |_   _| \ | |
     | \  / |  /  \    | | |  \| |
     | |\/| | / /\ \   | | | . ` |
     | |  | |/ ____ \ _| |_| |\  |
     |_|  |_/_/    \_\_____|_| \_|
                                  
    '''
    while (True):
        first_read = 0
        # 3 EYES
        left_eyes_s, middle_eyes_s, right_eyes_s = read_sensors(left_eyes_sensor,middle_eyes_sensor,right_eyes_sensor)
        print str(left_eyes_s) + ' ' + str(middle_eyes_s) + ' ' + str(
            right_eyes_s)
        # ANDE RETO
        if (left_eyes_s != colors['black'] and middle_eyes_s  == colors['black'] and right_eyes_s != colors['black']):
            go_straight(motor_left=my_motor_left, motor_right=my_motor_right, power=100*KVmax, distance=None)
        # ANDE RETO (LINHA SEGMENTADA)
        if (middle_eyes_s  != colors['black'] and left_eyes_s != colors['black'] and right_eyes_s != colors['black']):
            pass
        # OLHO ESQUERDO DETECTA LINHA e GIRA em PASSOS de 10 graus
        if (left_eyes_s == colors['black'] and right_eyes_s != colors['black']):
            my_motor_left.run(100*(-KVmin))
            my_motor_right.run(100*(KVmean))
        # OLHO DIREITO  DETECTA LINHA e GIRA em PASSOS de 10 graus
        if (left_eyes_s != colors['black'] and right_eyes_s == colors['black']):
            my_motor_left.run(100 * (KVmean))
            my_motor_right.run(100 * (-KVmin))
        if (left_eyes_s != colors['black'] and middle_eyes_s == colors['black'] and right_eyes_s == colors['black']):
            my_motor_left.run(100 * (KVmean))
            my_motor_right.run(100 * (-KVmean))
        # DESVIO DE OBSTACULO
        if (my_ultrasonic_sensor.get_distance() < 20):
            sm = SynchronizedMotors(my_motor_left,my_motor_right,100)
            sm.turn(80,200,True)
            go_straight(motor_left=my_motor_left, motor_right=my_motor_right, power=100 * 0.8, distance=22)
            sm = SynchronizedMotors(my_motor_right, my_motor_left, 100)
            sm.turn(80,200,True)
            go_straight(motor_left=my_motor_left, motor_right=my_motor_right, power=100 * 0.8, distance=40)
            sm = SynchronizedMotors(my_motor_right, my_motor_left, 100)
            sm.turn(80, 200, True)
            my_motor_right.idle()
            my_motor_left.idle()
            my_motor_right.run(80)
            my_motor_left.run(80)
            while (middle_eyes_sensor.get_color() != colors['black']):
                pass
except KeyboardInterrupt:
    # o motor para ao clicar ctrl+c
    my_motor_left.idle()
    my_motor_right.idle()


