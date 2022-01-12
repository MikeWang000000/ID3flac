import sys
import mimetypes
import mutagen.flac


def main():
    input_path = sys.argv[1]
    i = input_path.rfind('.')
    output_path = input_path[:i] + "-id3v2" + input_path[i:]
    flac_add_id3_cover(input_path, output_path)


def flac_add_id3_cover(input_path, output_path):
    flac = mutagen.flac.FLAC(input_path)
    pic = flac.pictures[0]
    add_id3_cover(input_path, output_path, pic.data, pic.mime)


def add_id3_cover(input_path, output_path, image=None, mime_type=None, image_path=None):
    if image is None or mime_type is None:
        mime_type = mimetypes.guess_type(input_path)[0]
        if not mime_type:
            raise ValueError("Invalid image file type")
        with open(image_path, "rb") as fin:     
            image = fin.read()

    padding_size = 512
    cover_size = len(image)
    apic_size = 4 + len(mime_type) + cover_size
    id3_size = 10 + apic_size + padding_size

    # ID3v2 header (10 bytes)
    id3_bin  = b"ID3"                       # ID3v2/file identifier
    id3_bin += b"\x03\x00"                  # ID3v2 version
    id3_bin += b"\x00"                      # ID3v2 flags
    id3_bin += bytes([                      # ID3v2 size
        (id3_size >> 21) & 0b01111111,
        (id3_size >> 14) & 0b01111111,
        (id3_size >>  7) & 0b01111111,
        (id3_size      ) & 0b01111111
    ])

    # ID3v2 APIC frame header (10 bytes)
    id3_bin += b"APIC"                      # Frame ID
    id3_bin += bytes([                      # Frame size
        (apic_size >> 24) & 0b11111111,
        (apic_size >> 16) & 0b11111111,
        (apic_size >>  8) & 0b11111111,
        (apic_size      ) & 0b11111111
    ])
    id3_bin += b"\x00\x00"                  # Flags

    # ID3v2 APIC frame
    id3_bin += b"\x00"                      # Text encoding
    id3_bin += mime_type.encode() + b"\0"   # MIME type
    id3_bin += b"\x03"                      # Picture type  (Cover (front))
    id3_bin += b"\x00"                      # Description   (blank)
    id3_bin += image                        # Picture data
    
    # Padding
    id3_bin += b"\x00" * padding_size

    with (open(input_path, "rb") as fin, open(output_path, "wb") as fout):
        buff = id3_bin
        fout.write(buff)
        while buff:
            buff = fin.read(1048576)
            fout.write(buff)


if __name__ == '__main__':
    main()
