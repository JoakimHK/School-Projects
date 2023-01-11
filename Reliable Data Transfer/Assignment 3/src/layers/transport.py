from copy import copy
from threading import Timer

from packet import Packet


class TransportLayer:
    """The transport layer receives chunks of data from the application layer
    and must make sure it arrives on the other side unchanged and in order.
    """

    def __init__(self):
        self.timer = None
        self.timeout = 0.4  # Seconds
        self.window_size = 3
        self.base = 1
        self.next_seqnum = 1
        self.excp_seqnum = 1
        self.dictionary = {}

        self.counter = 1


    def with_logger(self, logger):
        self.logger = logger
        return self

    def register_above(self, layer):
        self.application_layer = layer

    def register_below(self, layer):
        self.network_layer = layer

    def callback(self):
        self.reset_timer(self.callback)
        for i in range(self.base, self.next_seqnum):
            # self.network_layer.logger.warning(f"Sending    c {self.dictionary[i]}")

            self.network_layer.send(self.dictionary[i])
    
    def checksum(self, data):
        r = 0
        for c in data:
            r += c
        r = (r % 256)
        return bytes([r]) 

            

    def from_app(self, binary_data):
        self.counter += 1
        while (self.next_seqnum < self.counter):

            if(self.next_seqnum < self.base + self.window_size):
                cSum = self.checksum(binary_data)
                packet = Packet(binary_data, False, self.next_seqnum, 0, cSum)
                self.dictionary[packet.sequence] = packet

                # self.network_layer.logger.warning(f"Sending      {packet}")
                self.network_layer.send(packet)

                if(self.base == self.next_seqnum):
                    self.reset_timer(self.callback)
                self.next_seqnum += 1
                # print(self.next_seqnum)

    def from_network(self, packet: Packet):
        
        # Sender
        if packet.ack:
            # self.network_layer.logger.warning(f"Ack Received {packet}")
            if self.base < packet.sequence + 1:
                self.base = packet.sequence + 1

                if self.base == self.next_seqnum:
                    if(self.timer):
                        self.timer.cancel()
                else:
                    self.reset_timer(self.callback)

        # Reciever
        else:
            if(self.excp_seqnum == packet.sequence and packet.cSum == self.checksum(packet.data)):
                self.application_layer.receive_from_transport(packet.data)

                # self.network_layer.logger.warning(f"Received     {packet}")
                ACK_pack = Packet(b"", True, self.excp_seqnum, 1, b"")

                # self.network_layer.logger.warning(f"Acknowlege   {ACK_pack}")
                self.network_layer.send(ACK_pack)

                self.excp_seqnum += 1
            else:
                ACK_pack = Packet(b"", True, self.excp_seqnum - 1, 1, b"")
                # self.network_layer.logger.warning(f"Acknowlege b {ACK_pack}")

                self.network_layer.send(ACK_pack)


    def reset_timer(self, callback, *args):
        # This is a safety-wrapper around the Timer-objects, which are
        # separate threads. If we have a timer-object already,
        # stop it before making a new one so we don't flood
        # the system with threads!
        if self.timer:
            if self.timer.is_alive():
                self.timer.cancel()
        # callback(a function) is called with *args as arguments
        # after self.timeout seconds.
        self.timer = Timer(self.timeout, callback, *args)
        self.timer.start()
