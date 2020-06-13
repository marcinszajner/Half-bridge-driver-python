import struct

BYTE_PER_SAMPLE = 2
SIGNATURE = 0xAA
FREQUENCY_BIT = (1 << 31)

UPDATE = 1
DATA_REQ = 2

# typedef struct head_t
# {
#     uint8_t signature;
#     uint8_t type;
#     uint16_t size;
#     uint32_t crc;
# } __attribute__ ((packed)) head_t;
HEAD_T_SIZE = 4
SIGNATURE_IDX = 0
TYPE_IDX = 1
SIZE_IDX = 2
CRC_IDX = 3
head_t = struct.Struct('< B B H I')

# typedef struct protocol_change
# {
#     head_t head;
#     uint32_t bitfield;
#     uint32_t payload[];
#
# } __attribute__ ((packed)) protocol_change;
PROTOCOL_CHANGE_REQ_SIZE = HEAD_T_SIZE + 1
BITFIELD_IDX = HEAD_T_SIZE
protocol_change_t = struct.Struct('< B B H I I')

#TODO dubbled indexes name

# typedef struct protocol_data_req
# {
#     head_t head;
#     uint32_t  packet_size;
#     uint32_t  n_packet;
#     int32_t  fequency_step;
#     uint32_t actual_frequency
#
# }__attribute__ ((packed)) protocol_data_req;
PROTOCOL_DATA_REQ_SIZE = HEAD_T_SIZE + 4
PACKET_SIZE_IDX = HEAD_T_SIZE
N_PACKET_IDX = HEAD_T_SIZE + 1
FREQUENCY_STEP_IDX = HEAD_T_SIZE + 2
ACTUAL_FREQUENCY_IDX = HEAD_T_SIZE + 3
protocol_data_req_t = struct.Struct('< B B H I I I i I')

# typedef struct protocol_data_resp
# {
#     head_t head;
#     uint32_t  packet_size;
#     uint32_t  n_packet;
#     int32_t  fequency_step;
#     uint32_t actual_frequency
#     uint8_t payload[];
# }__attribute__ ((packed)) protocol_data_resp;
PROTOCOL_DATA_RESP_SIZE = HEAD_T_SIZE + 4
PACKET_SIZE_IDX = HEAD_T_SIZE
N_PACKET_IDX = HEAD_T_SIZE + 1
FREQUENCY_STEP_IDX = HEAD_T_SIZE + 2
ACTUAL_FREQUENCY_IDX = HEAD_T_SIZE + 3
protocol_data_resp_t = struct.Struct('< B B H I I I i I')
