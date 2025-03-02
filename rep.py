import rcu

# Импортируем модуль rcu для управления LEGO EV3
wait = rcu.SetWaitForTime
# Создаем псевдоним для функции SetWaitForTime из модуля rcu
enc = rcu.GetMotorCode
# Создаем псевдоним для функции GetMotorCode из модуля rcu
D = 6.5
# Диаметр колеса в сантиметрах
pi = 3.141592
# Значение числа pi
track = 16
# Расстояние между колесами (колея) в сантиметрах
err_old = 0
# Предыдущее значение ошибки (используется для коррекции движения)
err = 0
# Текущее значение ошибки
err0_L = rcu.GetMotorCode(1)
# Начальное значение кодировщика для левого мотора
err0_R = rcu.GetMotorCode(2)
# Начальное значение кодировщика для правого мотора
k = 2
# Коэффициент для коррекции ошибки

def distance(dis, speed):
    """
    Функция для движения робота на заданное расстояние с заданной скоростью.

    :param dis: Расстояние, которое нужно проехать (в сантиметрах)
    :param speed: Скорость движения (от -100 до 100)
    """
    rcu.SetMotorCode(1)
    rcu.SetMotorCode(2)
    # Сброс кодировщиков моторов

    while (abs(dis) > abs(rcu.GetMotorCode(1)) / 360 * 6.5 * 3.14) or (
            abs(dis) > abs(rcu.GetMotorCode(2)) / 360 * 6.5 * 3.14):
        # Цикл продолжается до тех пор, пока робот не проедет заданное расстояние

        err_L = abs(rcu.GetMotorCode(1)) - err0_L
        err_R = abs(rcu.GetMotorCode(2)) - err0_R
        # Вычисляем текущие ошибки для левого и правого моторов

        err = (err_L - err_R) * k
        # Вычисляем общую ошибку с учетом коэффициента k

        s1 = speed - err
        s2 = speed + err
        # Корректируем скорости моторов на основе ошибки

        if dis < 0:
            rcu.SetMotor(1, -s1)
            rcu.SetMotor(2, -s2)
        else:
            rcu.SetMotor(1, s1)
            rcu.SetMotor(2, s2)
        # Устанавливаем скорости моторов в зависимости от направления движения

    rcu.SetMotor(1, 0)
    rcu.SetMotor(2, 0)
    # Останавливаем моторы после завершения движения

def turn(angle, speed):
    """
    Функция для поворота робота на заданный угол с заданной скоростью.

    :param angle: Угол поворота (в градусах)
    :param speed: Скорость поворота (от -100 до 100)
    """
    while (abs(enc(1) / 360 * D * pi) < abs(angle / 360 * track * pi)) or (
            abs(enc(2) / 360 * D * pi) < abs(angle / 360 * track * pi)):
        # Цикл продолжается до тех пор, пока робот не повернет на заданный угол

        if angle > 0:
            rcu.SetMotor(1, speed)
            rcu.SetMotor(2, -speed)
        else:
            rcu.SetMotor(1, -speed)
            rcu.SetMotor(2, speed)
        # Устанавливаем скорости моторов в зависимости от направления поворота

    rcu.SetMotor(1, 0)
    rcu.SetMotor(2, 0)
    # Останавливаем моторы после завершения поворота

def BO():
    """
    Функция для считывания бинарного кода с помощью ультразвукового датчика.

    :return: Возвращает два числа, представляющих собой бинарный код
    """
    s = ''
    # Инициализируем строку для хранения бинарного кода

    if rcu.GetUltrasound(5) < 18:
        s += '1'
    else:
        s += '0'
    # Считываем первый бит с помощью ультразвукового датчика

    for i in range(7):
        # distance(30, 35)
        line(35, 30)
        # Двигаемся вперед на 30 см

        rcu.SetMotorCode(1)
        rcu.SetMotorCode(2)
        # Сброс кодировщиков моторов

        if rcu.GetUltrasound(5) < 18:
            s += '1'
        else:
            s += '0'
        # Считываем следующий бит

    s1 = s[1] + s[0]
    s2 = s[3] + s[2]
    s3 = s[5] + s[4]
    s4 = s[7] + s[6]
    # Формируем пары битов

    s1 = int(s1, 2)
    s2 = int(s2, 2)
    s3 = int(s3, 2)
    s4 = int(s4, 2)
    # Преобразуем пары битов в десятичные числа

    rcu.SetDisplayString(2, s, 0xFFFF, 0x0000)
    # Выводим бинарный код на дисплей

    return s3, s4
    # Возвращаем два числа, представляющих собой бинарный код

def line(speed, dis):
    """
    Функция для следования по линии с заданной скоростью и расстоянием.

    :param speed: Скорость движения (от -100 до 100)
    :param dis: Расстояние, которое нужно проехать (в сантиметрах)
    """
    while (rcu.GetMotorCode(1) / 360 * D * pi) < dis:
        # Цикл продолжается до тех пор, пока робот не проедет заданное расстояние

        s1 = speed + (rcu.GetLightSensor(7) - rcu.GetLightSensor(6)) * 0.02
        s2 = speed - (rcu.GetLightSensor(7) - rcu.GetLightSensor(6)) * 0.02
        # Корректируем скорости моторов на основе разницы значений датчиков света

        if s1 < -100:
            s1 = -100
        elif s1 > 100:
            s1 = 100

        if s2 < -100:
            s2 = -100
        elif s2 > 100:
            s2 = 100
        # Ограничиваем скорости моторов значениями от -100 до 100

        rcu.SetMotor(1, s1)
        rcu.SetMotor(2, s2)
        # Устанавливаем скорости моторов

    rcu.SetMotor(1, 0)
    rcu.SetMotor(2, 0)
    # Останавливаем моторы после завершения движения
