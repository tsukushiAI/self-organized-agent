PROMPT_TEMPLATES = {}

PROMPT_TEMPLATES["generate_skeleton"] = """
You will be given a function's docstring. Follow these steps to decompose thefunction into multiple helper functions:

1. Copy the docstrings from the beginning of the given function without omitting any part of it.

2. Implement the skeleton of the main function:
   - Write the function signature and the docstring.
   - Inside the function, call the helper functions you will create in the next steps.

3. Create helper functions to break down the functionality of the main function:
   - For each helper function, write the function signature and a docstring.
   - The docstring should include:
     - A brief description of what the helper function does.
     - The parameters of the helper function, including their types and a brief description.
     - The return value of the helper function, including its type and a brief description.
     - Unit tests using doctest syntax. These tests should cover the expected behavior and edge cases of the helper function.
   - Do not write the actual implementation of the helper functions. Instead, simply write `pass` as a placeholder. This will help focus on the structure and organization of the helper functions without getting distracted by the implementation details.

Remember:
- The main function should have its skeleton implemented, including the function signature, docstring, and calls to the helper functions.
- The helper functions should have their function signatures and docstrings written, but their actual implementation should be replaced with the `pass` statement.


### Example 1 ###
INPUT:
```python
def sort_and_sum(numbers: List[int]) -> int:
    '''
    Sorts a list of integers and then sums up all the elements.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    int - The sum of all elements in the sorted list.
    
    >>> sort_and_sum([3, 1, 2])
    6
    >>> sort_and_sum([-1, -2, -3, 0])
    -6
    >>> sort_and_sum([5])
    5
    '''
```

OUTPUT:
```python
from typing import List

# Skeleton (Implemented)
def sort_and_sum(numbers: List[int]) -> int:
    '''
    Sorts a list of integers and then sums up all the elements.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    int - The sum of all elements in the sorted list.
    
    >>> sort_and_sum([3, 1, 2])
    6
    >>> sort_and_sum([-1, -2, -3, 0])
    -6
    >>> sort_and_sum([5])
    5
    '''
    sorted_numbers = sort_list(numbers) # Helper function 1
    total = sum_list(sorted_numbers) # Helper function 2
    return total


# Helper function 1 (Not implemented)
def sum_list(numbers: List[int]) -> int:
    '''
    Calculates the sum of all elements in a given list of integers.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    int - The sum of the list's values.
    
    >>> sum_list([1, 2, 3])
    6
    >>> sum_list([-3, -2, -1, 0])
    -6
    >>> sum_list([5])
    5
    '''
    pass


# Helper function 2 (Not implemented)
def sort_list(numbers: List[int]) -> List[int]:
    '''
    Sorts a given list of integers.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    List[int] - The sorted list.
    
    >>> sort_list([3, 1, 2])
    [1, 2, 3]
    >>> sort_list([-1, -2, -3, 0])
    [-3, -2, -1, 0]
    >>> sort_list([5])
    [5]
    '''
    pass
```



### Example2 ### 
INPUT:
```python
def find_top_k_frequent_words(words: List[str], k: int) -> List[str]:
    '''
    Find the top k most frequent words in a given list of words.

    Parameters:
    words: List[str] - A list of words.
    k: int - The number of top frequent words to return.

    Returns:
    List[str] - A list of the top k most frequent words.

    >>> find_top_k_frequent_words(["apple", "banana", "apple", "cherry", "banana", "apple"], 2)
    ["apple", "banana"]
    >>> find_top_k_frequent_words(["dog", "cat", "dog", "fish", "cat", "dog", "dog"], 1)
    ["dog"]
    >>> find_top_k_frequent_words(["a", "b", "c", "d"], 3)
    ["a", "b", "c"]
    '''
```

OUTPUT:
```python
from typing import List

# Skeleton (Implemented)
def find_top_k_frequent_words(words: List[str], k: int) -> List[str]:
    '''
    Find the top k most frequent words in a given list of words.

    Parameters:
    words: List[str] - A list of words.
    k: int - The number of top frequent words to return.

    Returns:
    List[str] - A list of the top k most frequent words.

    >>> find_top_k_frequent_words(["apple", "banana", "apple", "cherry", "banana", "apple"], 2)
    ["apple", "banana"]
    >>> find_top_k_frequent_words(["dog", "cat", "dog", "fish", "cat", "dog", "dog"], 1) 
    ["dog"]
    >>> find_top_k_frequent_words(["a", "b", "c", "d"], 3)
    ["a", "b", "c"]
    '''
    word_counts = count_word_frequencies(words)  # Helper function 1
    sorted_word_counts = sort_word_counts(word_counts)  # Helper function 2
    top_k_words = get_top_k_words(sorted_word_counts, k)  # Helper function 3
    return top_k_words

# Helper function 1 (Not implemented)
def count_word_frequencies(words: List[str]) -> Dict[str, int]:
    '''
    Count the frequency of each word in a list of words.
    
    Parameters:
    words: List[str] - A list of words.

    Returns:
    Dict[str, int] - A dictionary mapping each unique word to its frequency count.

    >>> count_word_frequencies(["apple", "banana", "apple", "cherry", "banana", "apple"])
    {"apple": 3, "banana": 2, "cherry": 1}
    >>> count_word_frequencies(["dog", "cat", "dog", "fish", "cat", "dog", "dog"])
    {"dog": 4, "cat": 2, "fish": 1}
    >>> count_word_frequencies(["a", "b", "c", "d"])
    {"a": 1, "b": 1, "c": 1, "d": 1}
    '''
    pass

# Helper function 2 (Not implemented)
def sort_word_counts(word_counts: Dict[str, int]) -> List[Tuple[str, int]]:
    '''
    Sort the word counts dictionary by frequency in descending order.

    Parameters:
    word_counts: Dict[str, int] - A dictionary mapping each unique word to its frequency count.

    Returns:
    List[Tuple[str, int]] - A list of tuples, where each tuple contains a word and its frequency count, sorted by frequency in descending order.

    >>> sort_word_counts({"apple": 3, "banana": 2, "cherry": 1})
    [("apple", 3), ("banana", 2), ("cherry", 1)]
    >>> sort_word_counts({"dog": 4, "cat": 2, "fish": 1}) 
    [("dog", 4), ("cat", 2), ("fish", 1)]
    >>> sort_word_counts({"a": 1, "b": 1, "c": 1, "d": 1})
    [("a", 1), ("b", 1), ("c", 1), ("d", 1)]
    '''
    pass

# Helper function 3 (Not implemented)
def get_top_k_words(sorted_word_counts: List[Tuple[str, int]], k: int) -> List[str]:
    '''
    Get the top k most frequent words from the sorted word counts list.

    Parameters:
    sorted_word_counts: List[Tuple[str, int]] - A list of tuples, where each tuple contains a word and its frequency count, sorted by frequency in descending order.
    k: int - The number of top frequent words to return.

    Returns:
    List[str] - A list of the top k most frequent words.

    >>> get_top_k_words([("apple", 3), ("banana", 2), ("cherry", 1)], 2)
    ["apple", "banana"]
    >>> get_top_k_words([("dog", 4), ("cat", 2), ("fish", 1)], 1)
    ["dog"]
    >>> get_top_k_words([("a", 1), ("b", 1), ("c", 1), ("d", 1)], 3)
    ["a", "b", "c"]
    '''
    pass
```



### Example3 ###
INPUT:
```python
{function}
```

OUTPUT:
"""


PROMPT_TEMPLATES["generate_code"] = """
You will be given a function's docstring. Follow these steps to implement the function:

1. Copy the entire documentation string (docstring) from the provided function and paste it at the beginning of your implementation. Make sure not to omit any part of the docstring.

2. Implement the function according to the specifications described in the docstring. Your implementation should fulfill all the requirements and constraints mentioned.

### Example 1 ###
INPUT:
```python
from typing import List

def sort_list(numbers: List[int]) -> List[int]:
    '''
    Sorts a given list of integers.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    List[int] - The sorted list.
    
    >>> sort_list([3, 1, 2])
    [1, 2, 3]
    >>> sort_list([-1, -2, -3, 0])
    [-3, -2, -1, 0]
    >>> sort_list([5])
    [5]
    '''
    pass
```

OUTPUT:
```python
from typing import List

def sort_list(numbers: List[int]) -> List[int]:
    '''
    Sorts a given list of integers.

    Parameters:
    numbers: List[int] - A list of integers.
    
    Returns:
    List[int] - The sorted list.
    
    >>> sort_list([3, 1, 2])
    [1, 2, 3]
    >>> sort_list([-1, -2, -3, 0])
    [-3, -2, -1, 0]
    >>> sort_list([5])
    [5]
    '''
    return sorted(numbers)
```

### Example2 ###
INPUT:
```python
{function}
```

OUTPUT:
"""



PROMPT_TEMPLATES["generate_feedback_for_root_mother"] = '''
You are an engineer tasked with providing suggestions for improving Python code. Analyze the given function and test results in detail to identify issues.
- For each failed test case, specify the function name, input values, current output, and expected output.
- Extract and organize the specifications, rules, and conditions from the function's docstring.

Present concrete suggestions for addressing the identified issues.
- For each function that needs modification, provide examples of ideal behavior with input-output pairs.
- If necessary, propose updates to the documentation as well.

Please note the following:
- Focus on writing the "Cause" and "Improvement Direction" sections only.

###### Example1 ######
[Function]:
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = sum(numbers)
    count = count_numbers(numbers)
    return total / count
```

[Test Results]:

****************************************

Success Tests:
assert calculate_average([1, 2, 3, 4, 5]) == 3.0

Failed Tests:
assert calculate_average([]) == 0  # Output: ZeroDivisionError
assert calculate_average([1, 2, 3]) == 2.0  # Output: 1.5

****************************************
```

[Cause]:
1. The `count_numbers` function may not be returning 0 for an empty list. This leads to a `ZeroDivisionError` when an empty list is passed.
2. In the `calculate_average` function, when dividing the total by the count, the result is not being converted to `float`, resulting in integer division.

[Improvement Direction]:
1. Modify the `count_numbers` function to return 0 for an empty list.
2. In the `calculate_average` function, convert the total to `float` before dividing by the count.

###### Example2 ######
[Function]:
```python
{code}
```

[Test Results]:
```
{test_result}
```
'''


PROMPT_TEMPLATES["generate_feedback"] = '''
You are an engineer tasked with providing suggestions for improving Python code. Analyze the given function and test results in detail to identify issues.
- For each failed test case, specify the function name, input values, current output, and expected output.
- Extract and organize the specifications, rules, and conditions from the function's docstring.

Present concrete suggestions for addressing the identified issues.
- For each function that needs modification, provide examples of ideal behavior with input-output pairs.
- If necessary, propose updates to the documentation as well.

Please note the following:
- Focus on writing the "Cause" and "Improvement Direction" sections only.


###### Example1 ######
[Function]:
```python
def calculate_grades(student_scores: List[float]) -> List[str]:
    """
    Given a list of student scores, calculate the corresponding grades.
    Grades are assigned based on the following scale:
    - 90-100: A
    - 80-89: B
    - 70-79: C
    - 60-69: D
    - Below 60: F
    """
    grades = []
    for score in student_scores:
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        grades.append(grade)
    
    average = calculate_average(student_scores)
    print(f"Class average: {average}")
    
    return grades
```

[Test Results]:
```
****************************************

Success Tests:
assert calculate_grades([95, 87, 92, 98]) == ["A", "B", "A", "A"]
assert calculate_grades([75, 66, 84, 71]) == ["C", "D", "B", "C"]

Failed Tests:
assert calculate_grades([]) == []  # Output: ZeroDivisionError
assert calculate_grades([82, 93, 77]) == ["B", "A", "C"]  # Output: ZeroDivisionError

****************************************
```

[Cause]:
1. The `calculate_grades` function calls `calculate_average` with the `student_scores` list. If `student_scores` is empty, it will lead to a `ZeroDivisionError` in the `calculate_average` function.
2. The `calculate_average` function itself has issues when dealing with an empty list and integer division, as identified in the previous example.

[Improvement Direction]:
1. Modify the `calculate_grades` function to handle the case when `student_scores` is empty. You can skip the average calculation and printing if the list is empty.
2. Apply the improvements suggested for the `calculate_average` function to handle empty lists and integer division correctly.


###### Example2 ######
[Function]:
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = sum(numbers)
    count = count_numbers(numbers)
    return total / count
```

[Test Results]:
```
****************************************

Success Tests:
assert calculate_average([1, 2, 3, 4, 5]) == 3.0

Failed Tests:
assert calculate_average([]) == 0  # Output: ZeroDivisionError
assert calculate_average([1, 2, 3]) == 2.0  # Output: 1.5

****************************************
```

[Cause]:
1. The `count_numbers` function may not be returning 0 for an empty list. This leads to a `ZeroDivisionError` when an empty list is passed.
2. In the `calculate_average` function, when dividing the total by the count, the result is not being converted to `float`, resulting in integer division.

[Improvement Direction]:
1. Modify the `count_numbers` function to return 0 for an empty list.
2. In the `calculate_average` function, convert the total to `float` before dividing by the count.


###### Example3 ######
[Function]:
```python
{mother_old_code}
```

```
{mother_feedback}
```


###### Example4 ######
[Function]:
```python
{code}
```

[Test Results]:
```
{test_result}
```
'''



PROMPT_TEMPLATES["modify_code"] = '''
You are an engineer responsible for implementing the suggested improvements to the Python code while preserving the existing functionality. 
Your goal is to address the identified issues and implement the suggested improvements while adhering to the following guidelines: 1.

Please note the following:
- Focus on writing the "Updated Code" section only.
- Ensure that you utilize all the helper functions that were originally present in the code. Do not remove or replace any of these helper functions, as they play a vital role in the overall functionality of the program.

###### Example1 ######
[Function]:
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = sum(numbers)
    count = count_numbers(numbers)
    return total / count
```

[Test Results]:

****************************************

Success Tests:
assert calculate_average([1, 2, 3, 4, 5]) == 3.0

Failed Tests:
assert calculate_average([]) == 0  # Output: ZeroDivisionError
assert calculate_average([1, 2, 3]) == 2.0  # Output: 1.5

****************************************
```

[Cause]:
1. The `count_numbers` function may not be returning 0 for an empty list. This leads to a `ZeroDivisionError` when an empty list is passed.
2. In the `calculate_average` function, when dividing the total by the count, the result is not being converted to `float`, resulting in integer division.

[Improvement Direction]:
1. Modify the `count_numbers` function to return 0 for an empty list.
2. In the `calculate_average` function, convert the total to `float` before dividing by the count.

[Updated Code]
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = float(sum(numbers))
    count = count_numbers(numbers) # Do not remove or replace any of these helper functions.
    # count = new_func(numbers) # Do not add new helper functions.
    return total / count
```

###### Example2 ######
[Function]:
```python
{code}
```

[Test Results]:
```
{test_result}
```

{feedback}

[Updated Code]
'''


PROMPT_TEMPLATES["generate_unit_tests"] = '''
You are an AI assistant tasked with generating unit tests for a given Python function (called function). To create effective tests, consider the following:

1. The called function's docstring, which provides an overview of its purpose and behavior.
2. Feedback on the calling function's implementation, which may highlight issues or areas for improvement in the called function.
3. The code of the calling function before and after modification, which can provide insights into the expected behavior of the called function.

Use this information to generate a set of unit tests that verify the called function's behavior and address any issues mentioned in the feedback or implied by the changes in the calling function's code.


### Example 1 ###
[Calling Function's Code Before Modification]
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = sum(numbers)
    count = count_numbers(numbers)
    return total / count
```

[Test Results for Calling Function]:
```
****************************************

Success Tests:
assert calculate_average([1, 2, 3, 4, 5]) == 3.0

Failed Tests:
assert calculate_average([]) == 0  # Output: ZeroDivisionError
assert calculate_average([1, 2, 3]) == 2.0  # Output: 1.5

****************************************
```

[Cause]:
1. The `count_numbers` function may not be returning 0 for an empty list. This leads to a `ZeroDivisionError` when an empty list is passed.
2. In the `calculate_average` function, when dividing the total by the count, the result is not being converted to `float`, resulting in integer division.

[Improvement Direction for Calling Function]:
1. Modify the `count_numbers` function to return 0 for an empty list.
2. In the `calculate_average` function, convert the total to `float` before dividing by the count.


[Calling Function's Code After Modification]
```python
def calculate_average(numbers: List[int]) -> float:
    """
    Given a list of integers, calculate the average value.
    If the list is empty, return 0.
    """
    if not numbers:
        return 0
    
    total = float(sum(numbers))
    count = count_numbers(numbers) 
    return total / count
```

[Called Function]
```python
def count_numbers(numbers: List[int]) -> int:
    """
    Count the number of elements in a list of integers.
    If the list is empty, return 0.
    """
```

[Unit Tests for Called Function]
assert count_numbers([]) == 0 # Modify the `count_numbers` function to return 0 for an empty list. Generate unit tests based on failed tests of the calling function.


### Example 2 ###
[Calling Function's Code Before Modification]
```python
{mother_old_code}
```

[Test Results for Calling Function]:
```
{mother_test_result}
```

{mother_feedback}


[Calling Function's Code After Modification]
```python
{mother_new_code}
```

[Called Function]
```python
{code}
```

[Unit Tests for Called Function]
'''
