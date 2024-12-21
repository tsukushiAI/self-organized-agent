# Self-Organizing Agents

This repository contains the implementation of the paper [Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization (2024)](https://arxiv.org/abs/2404.02183). 

The self-organizing agent implementation is located in the `programming_runs/soa` directory. You can execute it using the provided script: `programming_runs/run_soa.sh`.

This repository builds upon the foundational work from [Reflexion](https://github.com/noahshinn/reflexion).

---

## Setup

### 1. Clone this repository

```sh
git clone https://github.com/yourusername/soa.git
cd soa
```

### 2. Install the required packages

```sh
pip install -r requirements.txt
```

### 3. Configure your OpenAI API key

Set your OpenAI API key as an environment variable:

```sh
export OPENAI_API_KEY=<your key>
```

---

## Execution

Run the self-organizing agents (SOA) framework using the command below:

```sh
cd programming_runs/
sh run_soa.sh
```

---

## Script Description

The execution script `run_soa.sh` simplifies running the SOA framework with pre-configured arguments. Below are the details of the script and its parameters.

### `run_soa.sh`

This script runs the main Python program with the following configuration:

```sh
python main.py \
  --run_name "soa" \
  --root_dir "human-eval-results" \
  --dataset_path benchmarks/humaneval-py.jsonl \
  --strategy "self-org-agent" \
  --language "py" \
  --model "gpt-3.5-turbo-1106" \
  --pass_at_k "1" \
  --max_iters "5" \
  --max_depth "2"
```

### Parameter Details

- **`--run_name`**: Specifies the name of the run (used for result organization).
- **`--root_dir`**: Defines the directory where the evaluation results will be saved.
- **`--dataset_path`**: Path to the dataset file (e.g., `humaneval-py.jsonl`).
- **`--strategy`**: Strategy for the framework, set as `"self-org-agent"`.
- **`--language`**: Target programming language (e.g., `"py"` for Python).
- **`--model`**: The model used (e.g., `"gpt-3.5-turbo-1106"`).
- **`--pass_at_k`**: Pass@k metric configuration.
- **`--max_iters`**: Maximum iterations for agent processing.
- **`--max_depth`**: Maximum depth of the agent tree structure.

---

## Citation

If you use this framework or reference the paper, please cite it as follows:

```bib
@article{ishibashi-and-nishimura-2024self,
  title        = {Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization},
  author       = {Yoichi Ishibashi and Yoshimasa Nishimura},
  journal      = {arXiv},
  volume       = {abs/2404.02183},
  year         = {2024},
  url          = {https://arxiv.org/abs/2404.02183}
}
```

