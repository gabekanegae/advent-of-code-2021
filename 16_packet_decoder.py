##################################
# --- Day 16: Packet Decoder --- #
##################################

from functools import reduce
import operator
import AOCUtils

ops = {
    0: {'fn': operator.add, 'str': '+'},
    1: {'fn': operator.mul, 'str': '*'},
    2: {'fn': min, 'str': 'min'},
    3: {'fn': max, 'str': 'max'},
    5: {'fn': operator.gt, 'str': '>'},
    6: {'fn': operator.lt, 'str': '<'},
    7: {'fn': operator.eq, 'str': '=='},
}

class StringStream:
    def __init__(self, stream):
        self.stream = stream
        self.i = 0

    def skip(self, n):
        self.i += n

    def read(self, n):
        s = self.i
        e = s + n

        self.skip(n)

        return self.stream[s:e]

    def peekAfter(self, n):
        s = self.i + n

        return self.stream[s:]

class Packet:
    def __init__(self, packet_bin):
        packet_stream = StringStream(packet_bin)

        self.version = int(packet_stream.read(3), 2)
        self.type_id = int(packet_stream.read(3), 2)

        self.value = None
        self.length_type_id = None
        self.length_of_subpackets = None
        self.number_of_subpackets = None
        self.subpackets = []

        if self.type_id == 4: # Literal value
            number_bin = ''

            keep_going = True
            while keep_going:
                if packet_stream.read(1) == '0':
                    keep_going = False
            
                number_bin += packet_stream.read(4)

            self.value = int(number_bin, 2)
        else: # Operator
            self.length_type_id = int(packet_stream.read(1), 2)

            if self.length_type_id == 0:
                self.length_of_subpackets = int(packet_stream.read(15), 2)

                length_read = 0
                self.subpackets = []
                while length_read < self.length_of_subpackets:
                    subpacket = Packet(packet_stream.peekAfter(length_read))
                    length_read += subpacket.packet_length

                    self.subpackets.append(subpacket)

                packet_stream.skip(length_read)
            else:
                self.value_of_subpackets = int(packet_stream.read(11), 2)

                for _ in range(self.value_of_subpackets):
                    subpacket = Packet(packet_stream.peekAfter(0))
                    packet_stream.skip(subpacket.packet_length)

                    self.subpackets.append(subpacket)

        self.packet_length = packet_stream.i
        # self.packet_bin = packet_bin[:self.packet_length+1]

        self.version_sum = self.version + sum(subpacket.version_sum for subpacket in self.subpackets)

        subpacket_values = (subpacket.value for subpacket in self.subpackets)

        if self.type_id != 4:
            op = ops[self.type_id]['fn']
            self.value = reduce(op, subpacket_values)

    def __repr__(self):
        if self.type_id == 4:
            return str(self.value)

        op = ops[self.type_id]['str']
        subpackets = ' '.join(map(str, self.subpackets))

        return f'({op} {subpackets})'

##################################

packet_hex = AOCUtils.load_input(16)

packet_bin = bin(int(packet_hex, 16))[2:].zfill(len(packet_hex) * 4)
packet = Packet(packet_bin)

# print(packet)

print(f'Part 1: {packet.version_sum}')

print(f'Part 2: {packet.value}')

AOCUtils.print_time_taken()