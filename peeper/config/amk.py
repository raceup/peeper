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
    Motors.FL: AMK_VALUES_1_CAN_IDS[Motors.FL.value],
    Motors.FR: AMK_VALUES_1_CAN_IDS[Motors.FR.value],
    Motors.RL: AMK_VALUES_1_CAN_IDS[Motors.RL.value],
    Motors.RR: AMK_VALUES_1_CAN_IDS[Motors.RR.value]
}
AMK_VALUES_2 = {
    Motors.FL: AMK_VALUES_2_CAN_IDS[Motors.FL.value],
    Motors.FR: AMK_VALUES_2_CAN_IDS[Motors.FR.value],
    Motors.RL: AMK_VALUES_2_CAN_IDS[Motors.RL.value],
    Motors.RR: AMK_VALUES_2_CAN_IDS[Motors.RR.value]
}
AMK_SETPOINTS = {
    Motors.FL: AMK_SETPOINTS_CAN_IDS[Motors.FL.value],
    Motors.FR: AMK_SETPOINTS_CAN_IDS[Motors.FR.value],
    Motors.RL: AMK_SETPOINTS_CAN_IDS[Motors.RL.value],
    Motors.RR: AMK_SETPOINTS_CAN_IDS[Motors.RR.value]
}
