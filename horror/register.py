#!/usr/bin/env python
import codecs
import encodings
import io
from encodings import utf_8
from .parser import transform_asm


def horror_transform(stream):
    output = transform_asm(stream.readlines())
    return output.rstrip()


def horror_transform_string(received_input):
    stream = io.StringIO(bytes(received_input).decode("utf-8"))
    return horror_transform(stream)


def horror_decode(received_input, errors="strict"):
    return horror_transform_string(received_input), len(received_input)


class HorrorIncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, received_input, final=False):
        self.buffer += received_input
        if received_input:
            old_buffer = self.buffer
            self.buffer = b""
            return super().decode(horror_transform_string(old_buffer).encode("utf-8"), final=True)
        else:
            return ""


class HorrorStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = io.StringIO(horror_transform(self.stream))


def search_function(encoding):
    if encoding != "horror":
        return None

    utf8 = encodings.search_function("utf8")
    return codecs.CodecInfo(
        name="horror",
        encode=utf8.encode,
        decode=horror_decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=HorrorIncrementalDecoder,
        streamreader=HorrorStreamReader,
        streamwriter=utf8.streamwriter,
    )


codecs.register(search_function)
