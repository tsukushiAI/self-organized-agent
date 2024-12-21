from utils import enumerate_resume, make_printv, write_jsonl, resume_success_count
#from executors import executor_factory
from generators import generator_factory, model_factory
from typing import List
import soas


def run_soa(
    dataset: List[dict],
    model_name: str,
    language: str,
    max_iters: int,
    pass_at_k: int,
    log_path: str,
    verbose: bool,
    max_depth: int,
    is_leetcode: bool = False
) -> None:
    #exe = executor_factory(language, is_leet=is_leetcode)
    gen = generator_factory(language)
    model_for_gen_test = model_factory("gpt-4-0125-preview")
    print_v = make_printv(verbose)

    num_items = len(dataset)
    num_success = resume_success_count(dataset)

    for i, item in enumerate_resume(dataset, log_path):
        cur_func_impl_is_None = True
        while cur_func_impl_is_None:
            cur_pass = 0
            is_solved = False
            #implementations = []
            test_feedback = []
            cur_func_impl = ""

            while cur_pass < pass_at_k and not is_solved:
                assert not is_leetcode
                tests_i = gen.internal_tests(item["prompt"], model_for_gen_test, 3) 

                docstrings = item["prompt"]
                function_name = item["entry_point"]
                unit_tests = tests_i

                max_iterations = max_iters
                cur_func_impl = soas.generate_and_modify_code_with_soa(function_name, docstrings, unit_tests, max_depth, max_iterations, model_name)
                eval_test = item['test']
                is_solved = soas.final_test(function_name, cur_func_impl, eval_test)

                cur_pass += 1

                num_success += int(is_solved)

                if cur_func_impl is None:
                    cur_func_impl_is_None = True
                    break
                else:
                    cur_func_impl_is_None = False                

        item["is_solved"] = is_solved
        item["test_feedback"] = test_feedback
        item["solution"] = cur_func_impl
        write_jsonl(log_path, [item], append=True)
        print_v(
            f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
        
        break

