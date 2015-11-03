import logging

class StringConverter:
    def __init__(self, exd_manager, language, enable_conditions = False):
        self.exd_manager = exd_manager
        self.language = language
        self.enable_conditions = enable_conditions

    def process_string(self, bytes_mem_view):
        bytes_mem_view, string_size = self.process_sequence(bytes_mem_view[1:])
        if string_size > len(bytes_mem_view):
            logging.error('ASCII control too short to process_string: %s', bytes_mem_view.tobytes())
            raise Exception('Integrity error')
        string_bytes_mem_view = bytes_mem_view[:string_size]
        return bytes_mem_view[string_size:], self.convert(string_bytes_mem_view)

    def process_int(self, bytes_mem_view):
        length = len(bytes_mem_view)
        int_type = bytes_mem_view[0]
        effective_size = 2
        result = None
        if length < effective_size:
            logging.error('ASCII control too short to process_int: %s', bytes_mem_view.tobytes())
            raise Exception('Out of bounds')
        byte_0 = bytes_mem_view[1]
        if int_type == 0xF0:
            result = byte_0
        elif int_type == 0xF1:
            result = byte_0 << 8
        elif int_type == 0xF7:
            result = byte_0 << 24
        elif int_type == 0xF3:
            result = byte_0 << 16
        else:
            effective_size = 3
            if length < effective_size:
                logging.error('ASCII control too short to process_int: %s' % bytes_mem_view.tobytes())
                raise Exception('Out of bounds')
            byte_1 = bytes_mem_view[2]
            if int_type == 0xF2:
                result = (byte_0 << 8) + byte_1
            elif int_type == 0xF4:
                result = (byte_0 << 16) + byte_1
            elif int_type == 0xF5:
                result = ((byte_0 << 16) + byte_1) << 8
            elif int_type == 0xF8:
                result = (byte_0 << 24) + byte_1
            elif int_type == 0xF9:
                result = ((byte_0 << 16) + byte_1) << 8
            elif int_type == 0xFB:
                result = ((byte_0 << 8) + byte_1) << 16
            else:
                effective_size = 4
                if length < effective_size:
                    logging.error('ASCII control too short to process_int: %s' % bytes_mem_view.tobytes())
                    raise Exception('Out of bounds')
                byte_2 = bytes_mem_view[3]
                if int_type == 0xF6:
                    result = (((byte_0 << 8) + byte_1) << 8) + byte_2
                elif int_type == 0xFA:
                    result = (((byte_0 << 16) + byte_1) << 8) + byte_2
                elif int_type == 0xFC:
                    result = (((byte_0 << 8) + byte_1) << 16) + byte_2
                elif int_type == 0xFD:
                    result = ((((byte_0 << 8) + byte_1) << 8) + byte_2) << 8
                else:
                    effective_size = 5
                    if length < effective_size:
                        logging.error('ASCII control too short to process_int: %s' % bytes_mem_view.tobytes())
                        raise Exception('Out of bounds')
                    byte_3 = bytes_mem_view[4]
                    if int_type == 0xFE:
                        result = (((((byte_0 << 8) + byte_1) << 8) + byte_2) << 8) + byte_3
                    else:
                        logging.error('Unknown int_type for process_int: %s', int_type)
                        raise Exception('Integrity error')
        return bytes_mem_view[effective_size:], result

    def process_special_values(self, bytes_mem_view):
        special_type = bytes_mem_view[0]
        bytes_mem_view, value = self.process_sequence(bytes_mem_view[1:])
        result = None 
        if special_type == 0xE9 and value == 0x04:
            result = 'is_woman'
        elif special_type == 0xE9 and value == 0x05:
            result = 'action_target_is_woman'
        elif special_type == 0xE9 and value == 0x0B:
            result = 'ig_hours'
        elif special_type == 0xE9 and value == 0x0C:
            result = 'ig_minutes'
        elif special_type == 0xE9 and value == 0x0D:
            result = 'say_color'
        elif special_type == 0xE9 and value == 0x0E:
            result = 'shout_color'
        elif special_type == 0xE9 and value == 0x0F:
            result = 'tell_color'
        elif special_type == 0xE9 and value == 0x10:
            result = 'party_color'
        elif special_type == 0xE9 and value >= 0x12 and value <= 0x19:
            result = 'linkshell_%d_color' % (value - 0x11)
        elif special_type == 0xE9 and value == 0x1A:
            result = 'free_company_color'
        elif special_type == 0xE9 and value == 0x1E:
            result = 'custom_emotes_color'
        elif special_type == 0xE9 and value == 0x1F:
            result = 'standard_emotes_color'
        elif special_type == 0xE9 and value == 0x44:
            result = 'class_job'
        elif special_type == 0xE9 and value in [0x45, 0x48]:
            result = 'level'
        else:
            result = 'not_implemented(0x%0.2X-0x%0.2X)' % (special_type, value)
            #logging.warn(result)

        return bytes_mem_view, result if self.enable_conditions else ''

    def process_test(self, bytes_mem_view):
        test_type = bytes_mem_view[0]
        
        bytes_mem_view, left_value = self.process_sequence(bytes_mem_view[1:])
        bytes_mem_view, right_value = self.process_sequence(bytes_mem_view)
        
        test_operator = None
        if test_type == 0xE0:
            test_operator = '>='
        elif test_type == 0xE1:
            test_operator = '>'
        elif test_type == 0xE2:
            test_operator = '<='
        elif test_type == 0xE3:
            test_operator = '<'
        elif test_type == 0xE4:
            test_operator = '=='
        elif test_type == 0xE5:
            test_operator = '!='
        else:
            logging.error('Unknown test_type for process_test: %s', first_byte)
            raise Exception('Integrity error')
        
        return bytes_mem_view, {
            'operator': test_operator,
            'left_operand': left_value,
            'right_operand': right_value
        } if self.enable_conditions else ''

    def process_date(self, bytes_mem_view):
        date_type = bytes_mem_view[0]
        result = None
        if date_type == 0xD8:
            result = 'milliseconds'
        elif date_type == 0xD9:
            result = 'seconds'
        elif date_type == 0xDA:
            result = 'minutes'
        elif date_type == 0xDB:
            result = 'hours'
        elif date_type == 0xDC:
            result = 'day'
        elif date_type == 0xDD:
            result = 'week_day'
        elif date_type == 0xDE:
            result = 'month'
        elif date_type == 0xDF:
            result = 'year'
        else:
            logging.error('Unknown date_type for parse_date: %s', date_type)
            raise Exception('Integrity error')
        return bytes_mem_view[1:], ''

    def process_sequence(self, bytes_mem_view):
        sequence_type = bytes_mem_view[0]
        if sequence_type == 0xFF:
            return self.process_string(bytes_mem_view)
        elif sequence_type >= 0xF0:
            return self.process_int(bytes_mem_view)
        elif sequence_type >= 0xED:
            logging.error('0x%0.2X while trying to decode sequence', sequence_type)
            raise Exception('Integrity error')
        elif sequence_type >= 0xE8:
            return self.process_special_values(bytes_mem_view)
        elif sequence_type >= 0xE6:
            logging.error('0x%0.2X while trying to decode sequence', sequence_type)
            raise Exception('Integrity error')
        elif sequence_type >= 0xE0:
            return self.process_test(bytes_mem_view)
        elif sequence_type >= 0xD8:
            return self.process_date(bytes_mem_view)
        elif sequence_type > 0x00:
            return bytes_mem_view[1:], sequence_type - 1
        else:
            logging.error('0x00 while trying to decode sequence')
            raise Exception('Integrity error')

    def control_boolean_choice(self, bytes_mem_view):
        bytes_mem_view, condition = self.process_sequence(bytes_mem_view)
        bytes_mem_view, value_Y = self.process_sequence(bytes_mem_view)
        bytes_mem_view, value_N = self.process_sequence(bytes_mem_view)
        return {
            'condition': condition,
            'yes': value_Y if type(value_Y) != int else '%d' % value_Y,
            'no': value_N if type(value_N) != int else '%d' % value_N,
        } if self.enable_conditions else '%s' % value_Y

    def control_linefeed(self, bytes_mem_view):
        return '  '

    def control_color(self, bytes_mem_view):
        if bytes_mem_view[0] == 0xEC:
            return '' # reset_color
        else:
            bytes_mem_view, value = self.process_sequence(bytes_mem_view)
            return '' # color

    def control_bold(self, bytes_mem_view):
        bytes_mem_view, value = self.process_sequence(bytes_mem_view)
        if value == 0x00:
            return '' # reset bold
        elif value == 0x01:
            return '' # bold
        else:
            logging.error('ASCII bold control invalid: %s', bytes_mem_view.tobytes())
            raise Exception('Integrity error')

    def control_empty(self, bytes_mem_view):
        return ''

    def control_link(self, bytes_mem_view):
        return '-'


    def control_int(self, bytes_mem_view):
        bytes_mem_view, value = self.process_sequence(bytes_mem_view)
        if type(value) == int:
            value = '%d' % value
        return value

    def control_mod_int(self, bytes_mem_view):
        bytes_mem_view, value = self.process_sequence(bytes_mem_view)
        if type(value) == int:
            value = '%d' % (value%100)
        return value

    def control_ref(self, bytes_mem_view):
        bytes_mem_view, category = self.process_sequence(bytes_mem_view)
        bytes_mem_view, id = self.process_sequence(bytes_mem_view)
        bytes_mem_view, offset = self.process_sequence(bytes_mem_view)

        if type(id) == int:
            return self.exd_manager.get_category(category).get_ln_id_data(self.language, id)[offset].decode('utf-8')
        else:
            return ''

    ASCII_CONTROL_TYPES = { 
        0x08: control_boolean_choice,
        0x10: control_linefeed,
        0x13: control_color,
        0x1A: control_bold,
        0x1D: control_empty,
        0x1F: control_link,
        0x20: control_int,
        0x24: control_mod_int,
        0x28: control_ref
    }

    STX = 0x02
    ETX = 0x03

    def parse_ascii_control(self, bytes_mem_view):
        if len(bytes_mem_view) < 0x04:
            logging.error('ASCII control too short: %s', bytes_mem_view.tobytes())
            raise Exception('Out of bounds')
        ascii_control_type = bytes_mem_view[1]
        bytes_mem_view, ascii_control_size = self.process_sequence(bytes_mem_view[2:])
        if not bytes_mem_view[ascii_control_size] == self.ETX:
            logging.error('Bad char at end of ASCII control: %s', bytes_mem_view[ascii_control_size])
            raise Exception('Integrity error')
        
        ascii_control_mem_view = bytes_mem_view[:ascii_control_size]
        remainder = bytes_mem_view[ascii_control_size + 1:]

        result = ''
        try:
            if ascii_control_type in self.ASCII_CONTROL_TYPES:
                result = self.ASCII_CONTROL_TYPES[ascii_control_type](self, ascii_control_mem_view)
            else:
                logging.debug('Unknown control types: 0x%0.2X - %s', ascii_control_type, repr(ascii_control_mem_view.tobytes()))
        except Exception as exc:
            logging.info('Exception caught in string_parsing F***ing SE: %s', exc)
        
        return remainder, result

    def convert(self, bytes_mem_view):
        if len(bytes_mem_view) == 0x00:
            return ''
        result = list()
        while True:
            stx_index = bytes_mem_view.tobytes().find(self.STX)
            if stx_index == -1:
                if len(bytes_mem_view) > 0x00:
                    result.append(bytes_mem_view.tobytes().decode('utf-8'))
                break
            else:
                if stx_index > 0x00:
                    result.append(bytes_mem_view[:stx_index].tobytes().decode('utf-8'))
                bytes_mem_view, ascii_control_result = self.parse_ascii_control(bytes_mem_view[stx_index:])
                result.append(ascii_control_result)

        current_result = list()
        current_str_list = list()
        for item in result:
            if type(item) == str:
                current_str_list.append(item)
            else:
                if current_str_list:
                    current_result.append(''.join(current_str_list))
                    current_str_list = list()
                current_result.append(item)

        if current_str_list:
            current_result.append(''.join(current_str_list))

        if len(current_result) == 1 and type(current_result[0]) == str:
            current_result = current_result[0]

        return current_result
