# RoboticaMovel
Tópicos Avançados em Automação - Seguidor de Linha

## Sensores e Atuadores do Robô Seguidor de Linha
* 2 Motores
* 3 Sensores RGB
* 1 Sensor Ultrassônico

## Função GO STRAIGHT
```def go_straight(motor_left, motor_right, power=64, distance=100):
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
```
## Função de Leitura de Sensores
```
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
```


## Fluxo Principal do Seguidor de Linha
```
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
   ```

