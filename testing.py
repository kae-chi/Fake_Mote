from helpers import get_interface_name, parse_command

# Generate values for pin number 5 and interface number 3 with actuator on state
pin_num = 5 | 0b10000000  # Setting highest bit to 1 for actuator command, rest for pin number
actuator_state = True
interface_num = 3

# Construct the config_num byte
actuator_state_mask = 0b01000000 if actuator_state else 0
config_num = actuator_state_mask | interface_num

# Combine pin_num and config_num into data to parse
data = bytes([pin_num, config_num])

parse_command(data)
