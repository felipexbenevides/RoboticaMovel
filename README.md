# RoboticaMovel
Tópicos Avançados em Automação - Seguidor de Linha
![alt text](https://raw.githubusercontent.com/felipexbenevides/RoboticaMovel/master/arquivos/imgs/1.jpg)
## Sensores e Atuadores do Robô Seguidor de Linha
* 2 Motores
* 3 Sensores RGB
* 1 Sensor Ultrassônico

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

