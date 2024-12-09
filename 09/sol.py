with open("puzzle.input", "r") as fp:
    line = [l.strip() for l in fp.readlines()][0]


def checksum_q1(blocks):
    if len(blocks) % 2 == 0:
        blocks = blocks[:-1]

    storage_index = 0
    checksum = 0
    file_id_front = 0
    file_id_back = len(line[::2]) - 1
    block_index_front, block_index_back = 0, -1
    while block_index_front <= len(blocks) + block_index_back:
        if is_file_block(block_index_front):
            checksum += add_file(
                blocks[block_index_front], storage_index, file_id_front
            )
            file_id_front += 1
            storage_index += blocks[block_index_front]
            blocks[block_index_front] = 0
        else:
            while blocks[block_index_front] > blocks[block_index_back]:
                # more space in free block than last file
                checksum += add_file(
                    blocks[block_index_back], storage_index, file_id_back
                )
                storage_index += blocks[block_index_back]
                blocks[block_index_front] -= blocks[block_index_back]
                blocks[block_index_back] = 0
                file_id_back -= 1
                block_index_back -= 2

            checksum += add_file(blocks[block_index_front], storage_index, file_id_back)
            blocks[block_index_back] -= blocks[block_index_front]
            storage_index += blocks[block_index_front]
            blocks[block_index_front] = 0

        block_index_front += 1
    return checksum


def checksum_q2(blocks):
    if len(blocks) % 2 == 0:
        blocks = blocks[:-1]

    file_sizes = blocks[::2]
    processed_files = set()

    storage_index = 0
    checksum = 0

    for block_index, b in enumerate(blocks):
        if len(file_sizes) == len(processed_files):
            return checksum
        if is_file_block(block_index) and (block_index // 2) not in processed_files:
            file_index = block_index // 2
            checksum += add_file(b, storage_index, file_index)
            storage_index += b
            processed_files.add(file_index)
        else:
            while b > 0:
                try:
                    file_index = max(
                        [
                            file_index
                            for file_index, file_size in enumerate(file_sizes)
                            if file_size <= b and file_index not in processed_files
                        ]
                    )
                except ValueError:
                    storage_index += b
                    break

                checksum += add_file(file_sizes[file_index], storage_index, file_index)
                storage_index += file_sizes[file_index]
                b -= file_sizes[file_index]
                processed_files.add(file_index)

    return checksum


def add_file(size, position, file_index):
    return sum([(position + i) * file_index for i in range(size)])


def is_file_block(index):
    return index % 2 == 0


print("q1", checksum_q1([int(k) for k in line]))
print("q2", checksum_q2([int(k) for k in line]))
