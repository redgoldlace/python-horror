# Horror
Effortlessly write inline x86_64 asm in Python source code
```python
# coding: horror
from horror import horror


@horror
def it_has_begun():
    %define stdout 1
    %define stderr 2

    %define newline 10

    section .data

        message db "Everything is terrible", newline
        message_length equ $-message

    section .text

    global _start
    _start:
        mov     rax, 1  
        mov     rdi, stdout
        mov     rsi, message
        mov     rdx, message_length
        syscall

        mov     rax, 60
        xor     rdi, rdi
        syscall


print("Oh god oh fuck oh shit")
it_has_begun()
```
This project is based upon and HEAVILY inspired by [Inline C](https://github.com/georgek42/inlinec).
Inline C states that it was inspired by [Pyxl](https://github.com/pyxl4/pyxl4), so I guess by proxy this project is also inspired by Pyxl.

# How does this work?
Python has a mechanism for creating custom codecs, which given an input token stream, produce an output token stream. Much like Inline C, Horror takes this token stream, runs a fault-tolerant parser on it, and identifies which functions are decorated with the @horror decorator. It then calls `nasm` and `ld`, building an executable out of the asm source code, and finally replaces the asm function with a `subprocess.run` call to this executable in the output token stream.

# Limitations
Note: This is just a joke that I put too much effort into. Don't expect anything serious.

* There's no way to interact with the asm program from python
* Shells out to `nasm` and `ld`
* Compilation is not cached
* Compilation creates an asm_builds directory which gets filled very quickly
* The source file can occasionally be parsed multiple times unnecessarily for no fucking reason (I don't know why this happens and I can't be bothered to fix it)
* Many more


# Installation
Just.. install the package. You'll need at least Python 3.6. I've tested with 3.6.9, but in theory it should be fine with later versions too.

```sh
python -m pip install git+https://github.com/kaylynn234/python-horror
```
(Season for taste depending on environment, you may want python3 on *nix systems for example)

Note that you'll need to have `ld` and `nasm` installed on path for this to work. Good luck running this on windows.