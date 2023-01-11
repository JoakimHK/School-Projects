class Packet:
    """Represent a packet of data.
    Note - DO NOT REMOVE or CHANGE the data attribute!
    The simulation assumes this is present!"""

    def __init__(self, binary_data, ack_data, sqn_data, pck_type, data_sum):
        # Add which ever attributes you think you might need
        # to have a functional packet.
        # TIPS: Add a __str__ method to print a packet-object nicely! :)
        self.data = binary_data
        self.ack = ack_data
        self.sequence = sqn_data
        self.cSum = data_sum
        self.type = pck_type

    def __str__(self):
        if self.type == 0:
            return f"|| Data: {self.data} || " + f"Seq: {self.sequence}"
        if self.type == 1:
            return f"|| Seq: {self.sequence}"
        # Extend me!
