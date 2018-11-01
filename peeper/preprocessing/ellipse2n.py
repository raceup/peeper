# -*- coding: utf-8 -*-

"""Parses Ellipse 2N data"""


def toggle_endianness(values):
    """Toggle endianness of values

    :param values: list of bytes, ints ...
    :return: values with other endianness (little -> big, big -> little)
    """

    return list(reversed(values))


def parse_raw_data(values):
    """Converts raw Ellipse 2N data

    :param values: raw values
    :return: decimal value
    """

    val = toggle_endianness(values)  # little endian
    val = "".join(val)
    return int(val, 16)  # convert to decimal value


def to_binary(val, expected_length=8):
    """Converts decimal value to binary

    :param val: decimal
    :param expected_length: length of data
    :return: binary value
    """

    val = bin(val)[2:]  # to binary

    while len(val) < expected_length:
        val = "0" + val

    return val


def get_hexadecimal(values):
    """Converts values to hexadecimal

    :param values: decimal values
    :return: hexadecimal values
    """

    return [
        hex(dec)[2:]  # remove "0x"
        for dec in values
    ]


def get_STATUS_01(byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6,
                  byte_7):
    """Calculates TIME STAMP based on data field

    :param byte_0: byte 0 of data field
    :param byte_1: byte 1 of data field
    :param byte_2: byte 2 of data field
    :param byte_3: byte 3 of data field
    :param byte_4: byte 4 of data field
    :param byte_5: byte 5 of data field
    :param byte_6: byte 6 of data field
    :param byte_7: byte 7 of data field
    :return: TIME_STAMP, GENERAL_STATUS, CLOCK_STATUS
    """

    arguments = list(reversed(list(locals().values())))
    hexadecimal_values = get_hexadecimal(arguments)

    time_stamp = parse_raw_data(hexadecimal_values[:4]) / 10 ** 6

    general_status = parse_raw_data(hexadecimal_values[4: 6])
    general_status = to_binary(general_status, 7)

    clock_status = parse_raw_data(hexadecimal_values[6:])
    clock_status = to_binary(clock_status, 4)

    return time_stamp, general_status, clock_status


def get_IMU_INFO(byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6,
                 byte_7):
    """Calculates IMU_INFO based on data field

    :param byte_0: byte 0 of data field
    :param byte_1: byte 1 of data field
    :param byte_2: byte 2 of data field
    :param byte_3: byte 3 of data field
    :param byte_4: byte 4 of data field
    :param byte_5: byte 5 of data field
    :param byte_6: byte 6 of data field
    :param byte_7: byte 7 of data field
    :return: TIME_STAMP, IMU_STATUS, TEMPERATURE
    """

    arguments = list(reversed(list(locals().values())))
    hexadecimal_values = get_hexadecimal(arguments)

    time_stamp = parse_raw_data(hexadecimal_values[:4]) / 10 ** 6

    imu_status = parse_raw_data(hexadecimal_values[4: 6])
    imu_status = to_binary(imu_status, 10)
    temperature = parse_raw_data(hexadecimal_values[6:]) / 10 ** 2

    return time_stamp, imu_status, temperature


def get_IMU_ACCEL(byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6,
                  byte_7):
    """Calculates IMU_INFO based on data field

    :param byte_0: byte 0 of data field
    :param byte_1: byte 1 of data field
    :param byte_2: byte 2 of data field
    :param byte_3: byte 3 of data field
    :param byte_4: byte 4 of data field
    :param byte_5: byte 5 of data field
    :param byte_6: byte 6 of data field
    :param byte_7: byte 7 of data field
    :return: ACCEL_X, ACCEL_Y, ACCEL_Z
    """

    arguments = list(reversed(list(locals().values())))
    hexadecimal_values = get_hexadecimal(arguments)
    scaling = 10 ** 2

    acc_x = parse_raw_data(hexadecimal_values[:2]) / scaling
    acc_y = parse_raw_data(hexadecimal_values[2: 4]) / scaling
    acc_z = parse_raw_data(hexadecimal_values[4: 6]) / scaling

    return acc_x, acc_y, acc_z
