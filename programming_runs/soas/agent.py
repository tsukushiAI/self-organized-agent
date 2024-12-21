from typing import List, Dict, Union
#from api import api_chat_completions
from . import api
from . import prompt
from . import py_utils
test_generator = py_utils.MyPythonExecute("gpt-3.5-turbo-1106")



# Helper functions (not provided in the pseudocode)
def generate_skeleton(docstrings: str, model_name: str) -> str:
    # Generate skeleton code based on docstrings and unit tests
    full_prompt = prompt.PROMPT_TEMPLATES["generate_skeleton"].replace("{function}", docstrings)
    code = api.api_chat_completions(full_prompt, model_name=model_name)
    return py_utils.extract_python_source_code_from_text(code)


def generate_code(docstrings: str, model_name: str) -> str:
    # Generate code based on docstrings and unit tests
    full_prompt = prompt.PROMPT_TEMPLATES["generate_code"].replace("{function}", docstrings)
    code = api.api_chat_completions(full_prompt, model_name=model_name)
    return py_utils.extract_python_source_code_from_text(code)


def get_subtasks(code: str, main_func_name: str, n_gen_tests: int) -> List[tuple]:
    # Extract subtask docstrings and unit tests from the code
    function_names = py_utils.extract_python_function_names(code)

    subtasks = []
    for func_name in function_names:
        if func_name != main_func_name:
            subtask_docstrings = py_utils.extract_python_function_from_text(code, func_name)
            #subtask_unit_tests = test_generator.generate_unit_tests(subtask_docstrings, n_gen_tests)
            subtasks.append([func_name, subtask_docstrings])
    return subtasks


def update_code(code: str, test_result: str, feedback: str, model_name: str) -> str:
    # Update code based on feedback
    full_prompt = prompt.PROMPT_TEMPLATES["modify_code"].replace("{code}", code)
    full_prompt = full_prompt.replace("{test_result}", test_result)
    full_prompt = full_prompt.replace("{feedback}", feedback)
    updated_code = api.api_chat_completions(full_prompt, model_name=model_name)
    return py_utils.extract_python_source_code_from_text(updated_code)


def generate_feedback(old_code: str, test_result: bool, upper_agent_observation: Union[Dict, None], model_name: str) -> str:
    # Generate feedback based on test results and upper agent observation
    if upper_agent_observation is None:
        full_prompt = prompt.PROMPT_TEMPLATES["generate_feedback_for_root_mother"].replace("{code}", old_code)
        full_prompt = full_prompt.replace("{test_result}", test_result)
    else:
        full_prompt = prompt.PROMPT_TEMPLATES["generate_feedback"].replace("{code}", old_code)
        full_prompt = full_prompt.replace("{test_result}", test_result)
        full_prompt = full_prompt.replace("{mother_feedback}", upper_agent_observation['feedback'])
        full_prompt = full_prompt.replace("{mother_old_code}", upper_agent_observation['old_code'])
        full_prompt = full_prompt.replace("{mother_new_code}", upper_agent_observation['new_code'])
    feedback = api.api_chat_completions(full_prompt, model_name=model_name)
    return feedback



def generate_unit_tests(code: str, n_tests: int, upper_agent_observation: Union[Dict, None], model_name: str) -> List[str]:
    # Generate unit tests based on the docstrings, mother agent's feedback, old code, and new code
    full_prompt = prompt.PROMPT_TEMPLATES["generate_unit_tests"].replace("{code}", code)
    full_prompt = full_prompt.replace("{mother_feedback}", upper_agent_observation['feedback'])
    full_prompt = full_prompt.replace("{mother_test_result}", upper_agent_observation['test_result'])
    full_prompt = full_prompt.replace("{mother_old_code}", upper_agent_observation['old_code'])
    full_prompt = full_prompt.replace("{mother_new_code}", upper_agent_observation['new_code'])

    generated_tests = api.api_chat_completions(full_prompt, model_name=model_name)
    
    # Extract individual test cases from the generated content
    test_cases = generated_tests.strip().split("\n")
    
    # Return the desired number of test cases
    return test_cases[:n_tests]


class Agent:
    def __init__(self, func_name: str, docstrings: str, model_name: str):
        self.func_name = func_name
        self.docstrings = docstrings
        self.code = docstrings
        self.unit_tests = []
        self.subagents = []
        self.n_gen_tests = 1
        self.model_name = model_name

    def update_memory(self, code):
        self.code = code

    def update_code(self, code: str, test_result: str, feedback: str) -> str:
        # Update code based on feedback
        return update_code(code, test_result, feedback, self.model_name)
    
    def generate_feedback(self, old_code: str, test_result: bool, upper_agent_observation: Union[Dict, None]) -> str:
        return generate_feedback(old_code, test_result, upper_agent_observation, self.model_name)
    
    def generate_unit_tests(self, code: str, n_tests: int, upper_agent_observation: Union[Dict, None]) -> List[str]:
        return generate_unit_tests(code, n_tests, upper_agent_observation, self.model_name)


class ChildAgent(Agent):
    def __init__(self, func_name: str, docstrings: str, model_name: str):
        super().__init__(func_name, docstrings, model_name)
        self.agent_type = "child"

    def generate_code(self, docstrings: str) -> str:
        return generate_code(docstrings, self.model_name)


class MotherAgent(Agent):
    def __init__(self, func_name: str, docstrings: str, model_name: str):
        super().__init__(func_name, docstrings, model_name)
        self.agent_type = "mother"

    def generate_skeleton(self, docstrings: str) -> str:
        return generate_skeleton(docstrings, self.model_name)

    def get_subtasks(self, skeleton) -> List[tuple]:
        return get_subtasks(skeleton, self.func_name, self.n_gen_tests)
    




