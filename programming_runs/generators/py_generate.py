from generators.model import ModelBase
#, message_to_str
from .generator_types import Generator
#from .generator_utils import generic_generate_func_impl, generic_generate_internal_tests, generic_generate_self_reflection
from .generator_utils import generic_generate_internal_tests

#from typing import Optional, List, Union
from typing import List
import ast
import re
#from .parse import parse_code_block, add_code_block


PY_TEST_GENERATION_FEW_SHOT = """Examples:
func signature:
def add3Numbers(x, y, z):
    \"\"\" Add three numbers together.
    This function takes three numbers as input and returns the sum of the three numbers.
    \"\"\"
unit tests:
assert add3Numbers(1, 2, 3) == 6
assert add3Numbers(-1, 2, 3) == 4
assert add3Numbers(1, -2, 3) == 2
assert add3Numbers(1, 2, -3) == 0
assert add3Numbers(-3, -2, -1) == -6
assert add3Numbers(0, 0, 0) == 0
"""

PY_TEST_GENERATION_CHAT_INSTRUCTION = """You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""

PY_TEST_GENERATION_COMPLETION_INSTRUCTION = f"""You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

{PY_TEST_GENERATION_FEW_SHOT}"""


class PyGenerator(Generator):
    #def self_reflection(self, func: str, feedback: str, model: ModelBase) -> str:
    #    return generic_generate_self_reflection(
    #        func=func,
    #        feedback=feedback,
    #        model=model,
    #        self_reflection_chat_instruction=PY_SELF_REFLECTION_CHAT_INSTRUCTION,
    #        self_reflection_completion_instruction=PY_SELF_REFLECTION_COMPLETION_INSTRUCTION,
    #        add_code_block=lambda x: add_code_block(x, "python"),
    #        self_reflection_few_shot=PY_SELF_REFLECTION_FEW_SHOT
    #    )

    '''
    def func_impl(
        self,
        func_sig: str,
        model: ModelBase,
        strategy: str,
        prev_func_impl: Optional[str] = None,
        feedback: Optional[str] = None,
        self_reflection: Optional[str] = None,
        num_comps: int = 1,
        temperature: float = 0.0,
    ) -> Union[str, List[str]]:
        return generic_generate_func_impl(
            func_sig=func_sig,
            model=model,
            strategy=strategy,
            prev_func_impl=prev_func_impl,
            feedback=feedback,
            self_reflection=self_reflection,
            num_comps=num_comps,
            temperature=temperature,
            reflexion_chat_instruction=PY_REFLEXION_CHAT_INSTRUCTION,
            reflexion_few_shot=PY_REFLEXION_FEW_SHOT_ADD,
            simple_chat_instruction=PY_SIMPLE_CHAT_INSTRUCTION,
            reflexion_completion_instruction=PY_REFLEXION_COMPLETION_INSTRUCTION,
            simple_completion_instruction=PY_SIMPLE_COMPLETION_INSTRUCTION,
            code_block_instruction=USE_PYTHON_CODEBLOCK_INSTRUCTION,
            parse_code_block=lambda x: parse_code_block(x, "python"),
            add_code_block=lambda x: add_code_block(x, "python"),
        )
    '''

    def internal_tests(self, func_sig: str, model: ModelBase, max_num_tests: int = 5) -> List[str]:
        def parse_tests(tests: str) -> List[str]:
            return [test.strip() for test in tests.splitlines() if "assert" in test]
        """
        Generates tests for a function.
        """
        return generic_generate_internal_tests(
            func_sig=func_sig,
            model=model,
            max_num_tests=max_num_tests,
            test_generation_few_shot=PY_TEST_GENERATION_FEW_SHOT,
            test_generation_chat_instruction=PY_TEST_GENERATION_CHAT_INSTRUCTION,
            test_generation_completion_instruction=PY_TEST_GENERATION_COMPLETION_INSTRUCTION,
            parse_tests=parse_tests,
            is_syntax_valid=py_is_syntax_valid,
        )


DUMMY_FUNC_SIG = "def func():"
DUMMY_FUNC_CALL = "func()"


def handle_first_line_indent(func_body: str) -> str:
    if func_body.startswith("    "):
        return func_body
    split = func_body.splitlines()
    return f"    {split[0]}\n" + "\n".join(split[1:])


def handle_entire_body_indent(func_body: str) -> str:
    split = func_body.splitlines()
    res = "\n".join(["    " + line for line in split])
    return res


def fix_turbo_response(func_body: str) -> str:
    return fix_markdown(remove_unindented_signatures(func_body))


def fix_markdown(func_body: str) -> str:
    return re.sub("`{3}", "", func_body)


def remove_unindented_signatures(code: str) -> str:
    regex = r"^def\s+\w+\s*\("

    before_signature = []
    after_signature = []
    signature_found = False

    for line in code.split("\n"):
        if re.match(regex, line):
            signature_found = True
            continue

        if signature_found:
            after_signature.append(line)
        else:
            if not line.startswith("    ") and line.strip():
                line = "    " + line
            before_signature.append(line)

    return "\n".join(before_signature + after_signature)


def py_fix_indentation(func_body: str) -> str:
    func_body = fix_turbo_response(func_body)
    """
    3 cases:
        1. good syntax
        2. first line not good
        3. entire body not good
    """
    def parse_indent_rec(f_body: str, cur_state: int) -> str:
        f_body = fix_markdown(f_body)
        if cur_state > 1:
            return f_body
        code = f'{DUMMY_FUNC_SIG}\n{f_body}\n{DUMMY_FUNC_CALL}'
        try:
            exec(code)
            return f_body
        except (IndentationError, SyntaxError):
            p_func = handle_first_line_indent if cur_state == 0 else handle_entire_body_indent
            return parse_indent_rec(p_func(func_body), cur_state + 1)
        except Exception:
            return f_body
    return parse_indent_rec(func_body, 0)


def py_is_syntax_valid(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except Exception:
        return False
