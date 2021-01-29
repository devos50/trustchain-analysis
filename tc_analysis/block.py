
import time

from deprecated.encoding import decode


GENESIS_HASH = '0'*32    # ID of the first block of the chain.
GENESIS_SEQ = 1
UNKNOWN_SEQ = 0
EMPTY_SIG = '0'*64
EMPTY_PK = '0'*74


class TrustChainBlock(object):
    """
    Container for TrustChain block information
    """

    def __init__(self, data=None):
        super(TrustChainBlock, self).__init__()
        if data is None:
            # data
            self.type = 'unknown'
            self.transaction = {}
            # identity
            self.public_key = EMPTY_PK
            self.sequence_number = GENESIS_SEQ
            # linked identity
            self.link_public_key = EMPTY_PK
            self.link_sequence_number = UNKNOWN_SEQ
            # validation
            self.previous_hash = GENESIS_HASH
            self.signature = EMPTY_SIG
            self.timestamp = int(round(time.time() * 1000))
            # debug stuff
            self.insert_time = None
        else:
            _, self.transaction = decode(str(data[1]))
            (self.type, self.public_key, self.sequence_number, self.link_public_key, self.link_sequence_number,
             self.previous_hash, self.signature, self.timestamp, self.insert_time) = (data[0], data[2], data[3],
                                                                                      data[4], data[5], data[6],
                                                                                      data[7], data[8], data[9])
            if isinstance(self.public_key, buffer):
                self.public_key = str(self.public_key)
            if isinstance(self.link_public_key, buffer):
                self.link_public_key = str(self.link_public_key)
            if isinstance(self.previous_hash, buffer):
                self.previous_hash = str(self.previous_hash)
            if isinstance(self.signature, buffer):
                self.signature = str(self.signature)

    def __str__(self):
        # This makes debugging and logging easier
        return "Block {0} from ...{1}:{2} links ...{3}:{4} for {5} type {6}".format(
            self.hash.encode("hex")[-8:],
            self.public_key.encode("hex")[-8:],
            self.sequence_number,
            self.link_public_key.encode("hex")[-8:],
            self.link_sequence_number,
            self.transaction,
            self.type)

    def __hash__(self):
        return self.hash

    @property
    def block_id(self):
        return "%s.%d" % (self.public_key.encode('hex'), self.sequence_number)

    @property
    def linked_block_id(self):
        return "%s.%d" % (self.link_public_key.encode('hex'), self.link_sequence_number)

    @property
    def is_genesis(self):
        return self.sequence_number == GENESIS_SEQ or self.previous_hash == GENESIS_HASH
