PAGE_SIZE = 1024
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}

def translate_paged(logical_address):
    page_num = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE
    if page_num not in PAGE_TABLE:
        return f"PAGE FAULT for logical address {logical_address}"
    frame_num = PAGE_TABLE[page_num]
    physical_address = (frame_num * PAGE_SIZE) + offset
    return physical_address

def translate_segmented(segment_num, offset):
    if segment_num not in SEGMENT_TABLE:
        return f"SEGMENTATION FAULT for segment {segment_num}"
    base, limit = SEGMENT_TABLE[segment_num]
    if offset >= limit:
        return f"SEGMENTATION FAULT: Offset {offset} >= Limit {limit} for segment {segment_num}"
    physical_address = base + offset
    return physical_address

if __name__ == "__main__":
    paged_addresses = [260, 1500, 3000, 5000]
    print("--- Paged Translations ---")
    for addr in paged_addresses:
        print(f"Address {addr} -> {translate_paged(addr)}")

    segmented_addresses = [(0, 150), (1, 350), (2, 100)]
    print("\n--- Segmented Translations ---")
    for seg, off in segmented_addresses:
        print(f"Segment ({seg}, {off}) -> {translate_segmented(seg, off)}")
