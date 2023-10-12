#!/usr/bin/env python3
"""The catpig memory-hard password-hashing function.
"""

from hashlib import blake2b, shake_256

K: int = 2 ** 10
M: int = 2 ** 20
BYTEORDER = 'little'
RND_CHUNK_SIZE: int = 8
SHAKE_SIZE: int = 64
READ_CHUNK_SIZE: int = K * 4
READ_BLOCK_SIZE: int = K * 64
NUM_CHUNKS_IN_READ_BLOCK: int = READ_BLOCK_SIZE // READ_CHUNK_SIZE
NUM_READ_BLOCKS_IN_MIB: int = M // READ_BLOCK_SIZE
RND_BLOCK_SIZE: int = RND_CHUNK_SIZE * NUM_CHUNKS_IN_READ_BLOCK + SHAKE_SIZE
MAX_SPACE_BLOCK_SIZE: int = (2 ** 31 - 1) // M
MAX_SPACE_MIB: int = (256 ** RND_CHUNK_SIZE - 1) // M


def catpig(
    password: bytes,
    salt: bytes,
    space_mib: int,
    passes: int
) -> bytes:
    """Memory-hard password-hashing function.
    """
    if space_mib < 1 or space_mib > MAX_SPACE_MIB:
        raise ValueError('Invalid space_mib value')

    if passes < 1:
        raise ValueError('Invalid passes value')

    space_size: int = space_mib * M
    num_read_blocks: int = NUM_READ_BLOCKS_IN_MIB * space_mib * passes
    half_num_read_blocks: int = num_read_blocks // 2 - 1

    ho_blake = blake2b()
    ho_blake.update(password)
    key64: bytes = ho_blake.digest()

    ho_blake = blake2b()
    ho_blake.update(salt)
    salt64: bytes = ho_blake.digest()

    ho_passes = blake2b()
    ho_passes.update(key64)
    ho_passes.update(salt64)

    ho_space = shake_256()
    ho_space.update(key64)
    ho_space.update(salt64)

    ho_mem_access_pattern = shake_256()
    ho_mem_access_pattern.update(salt64)

    num_space_blocks: int = space_size // MAX_SPACE_BLOCK_SIZE
    rem_space_size: int = space_size % MAX_SPACE_BLOCK_SIZE

    space_block_list: list = []

    for _ in range(num_space_blocks):
        space_block: bytes = ho_space.digest(MAX_SPACE_BLOCK_SIZE)
        space_block_list.append(space_block)
        ho_space.update(space_block[-SHAKE_SIZE:])

    if rem_space_size > 0:
        space_block = ho_space.digest(rem_space_size)
        space_block_list.append(space_block)

    for i in range(num_read_blocks):
        rnd_block: bytes = ho_mem_access_pattern.digest(RND_BLOCK_SIZE)
        rnd_block_read_pos: int = 0

        for _ in range(NUM_CHUNKS_IN_READ_BLOCK):
            rnd_chunk: bytes = rnd_block[rnd_block_read_pos:
                                         rnd_block_read_pos + RND_CHUNK_SIZE]
            int_rnd_chunk: int = int.from_bytes(rnd_chunk, byteorder=BYTEORDER)
            rnd_offset: int = int_rnd_chunk % space_size

            cur_block_num: int = rnd_offset // MAX_SPACE_BLOCK_SIZE
            cur_block_rnd_offset: int = rnd_offset % MAX_SPACE_BLOCK_SIZE
            cur_block_size: int = len(space_block_list[cur_block_num])

            if cur_block_size - cur_block_rnd_offset >= READ_CHUNK_SIZE:
                read_chunk: bytes = space_block_list[cur_block_num][
                    cur_block_rnd_offset:
                    cur_block_rnd_offset + READ_CHUNK_SIZE]
            else:
                if space_size - rnd_offset < READ_CHUNK_SIZE:
                    cur_block_num2: int = 0
                else:
                    cur_block_num2 = cur_block_num + 1

                read_size1: int = cur_block_size - cur_block_rnd_offset
                read_size2: int = READ_CHUNK_SIZE - read_size1

                read_chunk = b''.join([
                    space_block_list[cur_block_num][-read_size1:],
                    space_block_list[cur_block_num2][:read_size2]
                ])

            ho_passes.update(read_chunk)
            rnd_block_read_pos += RND_CHUNK_SIZE

        ho_mem_access_pattern.update(rnd_block[-SHAKE_SIZE:])

        if i >= half_num_read_blocks:
            passes_intermediate_digest = ho_passes.digest()
            ho_mem_access_pattern.update(passes_intermediate_digest)

    derived_key: bytes = ho_passes.digest()

    return derived_key
