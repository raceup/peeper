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

    time_stamp = toggle_endianness(values)  # little endian
    time_stamp = "".join(time_stamp)
    return int(time_stamp, 16)  # convert to decimal value


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

    hexadecimal_values = get_hexadecimal(locals().values())

    time_stamp = parse_raw_data(hexadecimal_values[:4])
    general_status = parse_raw_data(hexadecimal_values[4: 6])
    clock_stauts = parse_raw_data(hexadecimal_values[6:])

    return time_stamp, general_status, clock_stauts


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

    hexadecimal_values = get_hexadecimal(locals().values())

    time_stamp = parse_raw_data(hexadecimal_values[:4])
    imu_status = parse_raw_data(hexadecimal_values[4: 6])
    temperature = parse_raw_data(hexadecimal_values[6:])

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

    hexadecimal_values = get_hexadecimal(locals().values())

    acc_x = parse_raw_data(hexadecimal_values[:2])
    acc_y = parse_raw_data(hexadecimal_values[2: 4])
    acc_z = parse_raw_data(hexadecimal_values[4: 6])

    return acc_x, acc_y, acc_z
