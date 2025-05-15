import struct
import os
import argparse

UNKNOWN_HEADER_SIZE = 22
UINT32_SIZE = 4

def parse_meowers(data):
    offset = 0
    total_size = len(data)
    meowers = []

    while offset + UNKNOWN_HEADER_SIZE + 2 * UINT32_SIZE <= total_size:
        bruh = data[offset:offset + UNKNOWN_HEADER_SIZE]
        file_len, string_len = struct.unpack('<II', data[offset + UNKNOWN_HEADER_SIZE:offset + UNKNOWN_HEADER_SIZE + 8])
        offset += UNKNOWN_HEADER_SIZE + 8

        if offset + string_len + file_len > total_size:
            print("⚠️  Incomplete or corrupt struct at offset", offset)
            break

        filename = data[offset:offset + string_len].decode('utf-8', errors='replace')
        offset += string_len

        file_data = data[offset:offset + file_len]
        offset += file_len

        meowers.append((filename, file_data))

    return meowers

def write_files(meowers, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in meowers:
        safe_name = os.path.basename(filename)
        path = os.path.join(output_dir, safe_name)
        with open(path, 'wb') as f:
            f.write(content)
        print(f"✅ Wrote '{safe_name}' ({len(content)} bytes)")

def main():
    parser = argparse.ArgumentParser(description="Extract JPK structs from a binary file and write to files.")
    parser.add_argument("input", help="Path to the binary input file")
    parser.add_argument("-o", "--output", default="output", help="Directory to write extracted files")

    args = parser.parse_args()

    with open(args.input, "rb") as f:
        data = f.read()

    meowers = parse_meowers(data)
    print(f"🔍 Found {len(meowers)} meower(s).")
    write_files(meowers, args.output)

if __name__ == "__main__":
    main()
