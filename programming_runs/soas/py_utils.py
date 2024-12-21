import ast
import astor
import functools
import traceback
from typing import List, Dict, Any, Callable

from executors import executor_factory
from generators import generator_factory, model_factory
#from executors.py_executor import get_call_str
from executors.executor_utils import function_with_timeout


def ignore_snippet(code_with_snippet):
    return code_with_snippet.replace("```python", "").replace("```", "")

def get_output(assert_statement, namespace, timeout=5):
    try:
        func_call = assert_statement
        output = function_with_timeout(eval, (func_call, namespace), timeout)
        return output
    except TimeoutError:
        return "TIMEOUT"
    except Exception as e:
        return str(e)

def generate_error_message(func_name, error=None, previous_error_msg=None):
    if previous_error_msg:
        return previous_error_msg.replace("{current_func}", func_name)
    else:
        return f"`{func_name}` did not execute because the following error occurred in `{func_name}` function: '{error}'."

def convert_import_statements(imported_modules):
    converted_import_statements = []
    for module in imported_modules:
        if '.' in module:
            converted_import_statements.append("from " + " import ".join(module.split('.')))
        else:
            converted_import_statements.append("import " + module)
    return converted_import_statements


class MyPythonExecute:
    def __init__(self, model_name):
        language = "py"
        self.exe = executor_factory(language, is_leet=False)
        self.gen = generator_factory(language)
        self.model = model_factory(model_name)

    def execute_test(self, code_prompt, cur_func_impl):
        return self.execute_generated_test(code_prompt, cur_func_impl)

    def execute_generated_test(self, code_prompt, cur_func_impl):
        tests_i = self.generate_unit_tests(code_prompt, 1)
        is_passing, feedback, _ = self.exe.execute(cur_func_impl, tests_i)
        return is_passing, feedback
    
    def execute_defined_test(self, test_code, cur_func_impl):
        is_passing, feedback, _ = self.exe.execute(cur_func_impl, test_code)
        return is_passing, feedback
    
    def evaluate(self, entry_point, cur_func_impl, test_code):
        is_solved = self.exe.evaluate(
            entry_point, cur_func_impl, test_code, timeout=10)
        return is_solved
    
    def generate_unit_tests(self, signature, n_tests):
        return self.gen.internal_tests(signature, self.model, n_tests)

class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_code = None

    def visit_FunctionDef(self, node):
        if node.name == self.function_name:
            self.function_code = ast.unparse(node)

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.called_functions = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.called_functions.append(node.func.id)
        self.generic_visit(node)

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imported_modules = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imported_modules.append(alias.name)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imported_modules.append(f"{module}.{alias.name}")

class FunctionIOCapture:
    def __init__(self):
        self.io_details = []

    def capture_io(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_data = args[0] if args else kwargs
            is_error_in_previous_func = isinstance(input_data, str) and input_data.startswith("** error **:")
            
            output, stack_trace, is_error = None, None, False
            
            if is_error_in_previous_func:
                output = input_data
            else:
                try:
                    output = func(*args, **kwargs)
                except Exception as e:
                    output = f"** error **: {str(e)}"
                    stack_trace = traceback.format_exc()
                    is_error = True

            self.io_details.append({
                'function_name': func.__name__,
                'input': input_data,
                'output': output,
                'stack_trace': stack_trace,
                'is_error': is_error or is_error_in_previous_func
            })
            return output
        
        return wrapper

    def execute_and_record_io(self, code_string: str, function_names: List[str], unit_tests: List[str]):
        local_scope = {}
        exec(code_string, globals(), local_scope)

        for name in function_names:
            if name in local_scope:
                captured_func = self.capture_io(local_scope[name])
                local_scope[name] = captured_func
                globals()[name] = captured_func

        for test in unit_tests:
            try:
                exec(test, globals(), local_scope)
            except AssertionError as e:
                print(f"Test failed: {test}, Error: {e}")

        return self.io_details

# Functions
def extract_python_function_from_text(code, function_name):
    code = ignore_snippet(code)
    tree = ast.parse(code)
    extractor = FunctionExtractor(function_name)
    extractor.visit(tree)
    func = extractor.function_code
    assert func, function_name
    assert func, code
    assert func, code + "\n\n" + function_name
    return func

def extract_python_function_names(code):
    code = ignore_snippet(code)
    function_names = []

    class FunctionNameExtractor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            function_names.append(node.name)

    tree = ast.parse(code)
    extractor = FunctionNameExtractor()
    extractor.visit(tree)

    return function_names

def extract_python_source_code_from_text(code):
    code = ignore_snippet(code)
    parsed_ast = ast.parse(code)
    new_ast = ast.Module(body=[], type_ignores=[])

    for node in parsed_ast.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom)):
            new_ast.body.append(node)

    new_source_code = astor.to_source(new_ast)
    return new_source_code

def get_exec_function_order_list(code, sub_function_name_list, main_function_name):
    code = ignore_snippet(code)
    parsed_code = ast.parse(code)
    visitor = FunctionCallVisitor()
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef) and node.name == main_function_name:
            visitor.visit(node)

    called_functions = visitor.called_functions
    called_functions = [func_name for func_name in called_functions if func_name in sub_function_name_list]
    called_functions.append(main_function_name)
    return called_functions

def extract_imported_module_names(code):
    code = ignore_snippet(code)
    parsed_code = ast.parse(code)
    import_visitor = ImportVisitor()
    import_visitor.visit(parsed_code)
    imported_modules = import_visitor.imported_modules
    return imported_modules

def extract_imported_module_statements(code):
    imported_modules = extract_imported_module_names(code)
    return convert_import_statements(imported_modules)

def record_io(function_names: List[str], code: str, unit_tests: List[str]) -> List[Dict[str, Any]]:
    code = ignore_snippet(code)
    namespace = {"List": List}
    exec(code, namespace)
    original_functions = {name: func for name, func in namespace.items() if name in function_names}
    func_io_each_tests = []

    def wrap_function(func):
        def wrapper(*args, **kwargs):
            if len(calls) > 0 and calls[-1]['is_error']:
                error_msg = calls[-1]['error_msg']
                is_error, output = True, None
            else:
                try:
                    output = func(*args, **kwargs)
                    is_error, error_msg = False, None
                except Exception as e:
                    is_error, output = True, None
                    error_msg = f"Error at `{func.__name__}` function: {str(e)}"

            calls.append({
                'function_name': func.__name__,
                'input': args[0] if args else "No input",
                'output': output,
                'is_error': is_error,
                'error_msg': error_msg
            })
            return output
        return wrapper

    for name, func in original_functions.items():
        namespace[name] = wrap_function(func)
    
    is_good_assert = False
    for assert_statement in unit_tests:
        for name in function_names:
            if name in assert_statement:
                is_good_assert = True
    assert is_good_assert, unit_tests

    for assert_statement in unit_tests:
        calls = []
        output = get_output(assert_statement, namespace)

        _calls = []
        is_error = False
        for i, c in enumerate(calls):
            if c['is_error'] or is_error:
                is_error = True
                c['output'] = None
                c['is_error'] = True
                if i > 0:
                    c['error_msg'] = _calls[-1]['error_msg']
                _calls.append(c)
            else:
                _calls.append(c)
        calls = _calls

        func_io_each_tests.append(calls)
        
    return func_io_each_tests

def find_called_functions_in_function(code, calling_func_name):
    code = ignore_snippet(code)

    class FunctionCallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.called_functions = []

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name): 
                self.called_functions.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):  
                self.called_functions.append(node.func.attr)
            self.generic_visit(node)

    class SpecificFunctionVisitor(ast.NodeVisitor):
        def __init__(self, target_func_name):
            self.target_func_name = target_func_name
            self.function_call_visitor = FunctionCallVisitor()

        def visit_FunctionDef(self, node):
            if node.name == self.target_func_name:
                self.function_call_visitor.visit(node)
            self.generic_visit(node)

    tree = ast.parse(code)
    visitor = SpecificFunctionVisitor(calling_func_name)
    visitor.visit(tree)

    return visitor.function_call_visitor.called_functions

def find_calling_functions_of_function(code, called_func_name):
    code = ignore_snippet(code)
    
    class CallingFunctionVisitor(ast.NodeVisitor):
        def __init__(self, target_func_name):
            self.target_func_name = target_func_name
            self.calling_functions = []

        def visit_Call(self, node):
            if ((isinstance(node.func, ast.Name) and node.func.id == self.target_func_name) or
                (isinstance(node.func, ast.Attribute) and node.func.attr == self.target_func_name)):
                if hasattr(self, 'current_function') and self.current_function not in self.calling_functions:
                    self.calling_functions.append(self.current_function)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            self.generic_visit(node)
            del self.current_function

    tree = ast.parse(code)
    visitor = CallingFunctionVisitor(called_func_name)
    visitor.visit(tree)

    return visitor.calling_functions