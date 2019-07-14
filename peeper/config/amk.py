from enum import Enum


class Motors(Enum):
    FL = 3
    FR = 2
    RL = 1
    RR = 0


AMK_VALUES_1_CAN_IDS = ['283', '284', '287', '288']
AMK_VALUES_2_CAN_IDS = ['285', '286', '289', '28a']
AMK_SETPOINTS_CAN_IDS = ['184', '185', '188', '189']

AMK_VALUES_1 = {
    motor: AMK_VALUES_1_CAN_IDS[motor.value]
    for motor in Motors
}
AMK_VALUES_2 = {
    motor: AMK_VALUES_2_CAN_IDS[motor.value]
    for motor in Motors
}
AMK_SETPOINTS = {
    motor: AMK_SETPOINTS_CAN_IDS[motor.value]
    for motor in Motors
}

MOTOR_LABELS = ["FL", "FR", "RL", "RR"]
