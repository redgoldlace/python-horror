import os
import uuid
from typing import Dict, List, Optional, Tuple

import parso
from parso.python.tree import PythonNode
from tokenize import generate_tokens, TokenInfo, INDENT
from io import StringIO


def token_at(line_number: int, token_type: int, tokens: List[TokenInfo]) -> Optional[TokenInfo]:
    for token in tokens:
        if token.start[0] >= line_number and token.type == token_type:
            return token


def find_from_children(type_: str, node: PythonNode) -> Optional[PythonNode]:
    for child in node.children:
        if child.type == type_:
            return child


def find_decorated_nodes(module: PythonNode) -> List[PythonNode]:
    decorated = []
    to_process = [module]
    while to_process:
        relevant_node = to_process.pop()
        if not hasattr(relevant_node, "children"):
            continue

        decorator_found = False
        for child in relevant_node.children:
            if not decorator_found and child.type == "decorator":
                name = find_from_children("name", child).value
                if name == "horror":
                    decorator_found = True
                    continue
            elif decorator_found and child.type == "funcdef":
                decorated.append(child)
            if hasattr(child, "children"):
                to_process.append(child)

    return decorated


def transform_asm(lines: List[str]) -> str:
    source_code = "".join(lines)
    module = parso.parse(source_code)
    tokens = list(generate_tokens(StringIO(source_code).readline))
    asm_code = find_decorated_nodes(module)
    lines = ["\n", "import subprocess\n"] + lines[1:]  # Add a subprocess import at the top of the file
    offset = 1

    # Make a subdirectory
    subdirectory_name = f"run_{uuid.uuid4()}".replace("-", "_")
    os.makedirs(f"asm_builds/{subdirectory_name}", exist_ok=True)

    for inline_asm_func in asm_code:
        path = f"asm_builds/{subdirectory_name}/{inline_asm_func.name.value}"
        starting_line = inline_asm_func.start_pos[0] + offset
        ending_line = inline_asm_func.end_pos[0] + offset

        # Clean up from last run
        # for path in [f"{path}.asm", f"{path}.o", f"{path}"]:
        #     try:
        #         os.remove(path)
        #     except Exception:
        #         pass

        # skip the first line - it's the function signature
        with open(f"{path}.asm", "w", encoding="utf-8", errors="ignore") as asm_file:
            asm_file.writelines(inline_asm_func.get_code().split("\n")[1:])

        os.system(f"nasm -f elf64 -o {path}.o {path}.asm && ld -o {path} {path}.o")

        indent = token_at(starting_line - offset, INDENT, tokens).string
        lines[starting_line] = f'{indent}subprocess.run("./{path}")\n'

        for i in range(starting_line + 1, ending_line - 1):
            lines[i] = ""

    return "".join(lines)
