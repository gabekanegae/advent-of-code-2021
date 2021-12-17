##################################
# --- Day 16: Packet Decoder --- #
##################################

import AOCUtils

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

    def seeAfter(self, n):
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
                    subpacket = Packet(packet_stream.seeAfter(length_read))
                    length_read += subpacket.packet_length

                    self.subpackets.append(subpacket)

                packet_stream.skip(length_read)
            else:
                self.value_of_subpackets = int(packet_stream.read(11), 2)

                for _ in range(self.value_of_subpackets):
                    subpacket = Packet(packet_stream.seeAfter(0))
                    packet_stream.skip(subpacket.packet_length)

                    self.subpackets.append(subpacket)

        self.packet_length = packet_stream.i
        # self.packet_bin = packet_bin[:self.packet_length+1]

        self.version_sum = self.version + sum(subpacket.version_sum for subpacket in self.subpackets)

        if self.type_id == 0:
            self.value = sum(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 1:
            self.value = 1
            for subpacket in self.subpackets:
                self.value *= subpacket.value
        elif self.type_id == 2:
            self.value = min(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 3:
            self.value = max(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 5:
            self.value = int(self.subpackets[0].value > self.subpackets[1].value)
        elif self.type_id == 6:
            self.value = int(self.subpackets[0].value < self.subpackets[1].value)
        elif self.type_id == 7:
            self.value = int(self.subpackets[0].value == self.subpackets[1].value)

    def __repr__(self):
        if self.type_id == 4:
            return str(self.value)
        else:
            op = {0: '+', 1: '*', 2: 'min', 3: 'max', 5: '>', 6: '<', 7: '=='}[self.type_id]

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