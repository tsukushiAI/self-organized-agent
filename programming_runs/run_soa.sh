python main.py \
  --run_name "soa" \
  --root_dir "human-eval-results" \
  --dataset_path benchmarks/humaneval-py.jsonl \
  --strategy "self-org-agent" \
  --language "py" \
  --model "gpt-3.5-turbo-1106" \
  --pass_at_k "1" \
  --max_iters "5" \
  --max_depth "2" \
  --verbose

