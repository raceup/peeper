# -*- coding: utf-8 -*-

"""Parses Ellipse 2N data"""

from parsers.can.models import BytesParser


class Ellipse2NParser(BytesParser):
    def get_as_status_01(self):
        raw_values = self.parse([4, 2, 2], scalings=None)

        time_stamp = self.from_micro(raw_values[0])  # micro-seconds
        general_status = self.to_binary(raw_values[1], 16)
        clock_status = self.to_binary(raw_values[2], 16)

        return time_stamp, general_status, clock_status

    def get_as_utc_0(self):
        return self.parse([4, 4], [10 ** -6, 10 ** -3])

    def get_as_utc_1(self):
        return self.parse(
            [1, 1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 10 ** -4]
        )

    def get_as_imu_info(self):
        raw_values = self.parse(
            [4, 2, 2]
        )

        time_stamp = self.from_micro(raw_values[0])  # micro-seconds
        imu_status = self.to_binary(raw_values[1], 16)
        temperature = self.apply_scaling(raw_values[2], 10 ** -2)

        return time_stamp, imu_status, temperature

    def get_as_acc(self):
        scaling = 10 ** -2

        byte_num = 2
        num_values = 3

        return self.parse(
            num_values * [byte_num], num_values * [scaling], two_complement=True
        )

    def get_as_gyro(self):
        scaling = 10 ** -3
        byte_num = 2
        num_values = 3

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_delta_vel(self):
        return self.get_as_acc()

    def get_as_delta_angle(self):
        scaling = 10 ** -3
        byte_num = 2
        num_values = 3

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_ekf_quaternion(self):
        scaling = 32768 ** -1
        byte_num = 2
        num_values = 4

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_ekf_euler(self):
        scaling = 10 ** -4
        byte_num = 2
        num_values = 3

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_ekf_orientation_accuracy(self):
        scaling = 10 ** -4
        byte_num = 2
        num_values = 3

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_gps1_pos_info(self):
        raw_values = self.parse(
            [4, 4]
        )

        time_stamp = self.from_micro(raw_values[0])  # micro-seconds
        imu_status = self.to_binary(raw_values[1], 32)

        return time_stamp, imu_status

    def get_as_gps1_pos(self):
        scaling = 10 ** -7
        byte_num = 4
        num_values = 2

        return self.parse(num_values * [byte_num], num_values * [scaling])

    def get_as_gps1_alt(self):
        raw_values = self.parse(
            [4, 2, 1, 1]
        )

        altitude = self.from_milli(raw_values[0])
        undulation = self.apply_scaling(raw_values[1], 0.005)
        vehicles = int(raw_values[2])
        age = self.to_binary(raw_values[3], 8)

        return altitude, undulation, vehicles, age

    def get_as_odo_velocity(self):
        return self.parse([4])
