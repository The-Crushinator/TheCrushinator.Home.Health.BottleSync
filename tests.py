# Test `parse_sip()` from `connect.py`
#016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown: bytearray(b'\x04\x07&\x00\xe7<\x00\x00\x05\x8a \x8f\xdc\x8b\x80\x8b\x00\x00\x00\x00')
#016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown: bytearray(b'\x03\x04*\x00\xf3;\x00\x00\x05\x8a \x8f\x80\x8bG\x8b\x00\x00\x00\x00')
#016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown: bytearray(b'\x02\x04.\x00\x197\x00\x00\x05\x8a \x8fG\x8b\x08\x8b\x00\x00\x00\x00')
#016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown: bytearray(b'\x01\x020\x00^\x1b\x00\x00\x05\x8a \x8f\x08\x8b\xe8\x8a\x00\x00\x00\x00')
#016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

import sys
sys.path.append('.')
from connect import parse_sip, get_size_from_byte_array

def test_parse_sip():
    #bottle_size = get_size_from_byte_array(b'\xc2\x03')
    #bottle_size = get_size_from_byte_array(b'\x18\x00(\x00\x00\x00*\x00')
    bottle_size = get_size_from_byte_array(b'\x80\x00\x00\x00')
    sip = b'\x04\x07&\x00\xe7<\x00\x00\x05\x8a \x8f\xdc\x8b\x80\x8b\x00\x00\x00\x00'
    value = parse_sip(sip, bottle_size=bottle_size)
    # TODO: Confirm values
    #assert value == 0x04

if __name__ == '__main__':
    test_parse_sip()
    print('All tests passed')