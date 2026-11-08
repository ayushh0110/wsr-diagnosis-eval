# Capture summary: 15_code_temperature_decoy

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, temp_07, penalty_off; 4 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 3.5, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(): \n     for i in range(1, 6):  # Rows (or one factor) from 1 to 5 \n       |
| failing | 2 | `{"temperature": 3.5, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=5): \n     """Prints an n x n multiplication table.""" \n  \n # Create  |
| failing | 3 | `{"temperature": 3.5, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n for i in range(1, 6):  # Rows from 1 to 5 (the multiplicand) \n     row_output = [] \n     if len(i * [0])  |
| failing | 4 | `{"temperature": 3.5, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n  \n def print_multiplication(size=3): # Changed to make it easy for others, but user asked specifically for |
| temp_07 | 1 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(n=1): \n     """Prints an n x n multiplication table.""" \n  \n # Define siz |
| temp_07 | 2 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(n=5): \n     """Prints an n x n multiplication table.""" \n  \n     for i in |
| temp_07 | 3 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=5): \n     """Prints an n x n multiplication table.""" \n  \n     print |
| temp_07 | 4 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=10): \n     """Prints a square size (n x n) multiplication table.""" \n |
| penalty_off | 1 | `{"temperature": 3.5, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(): \n     """Prints a 5x5 multiplication table.""" \n     for i in range(1,  |
| penalty_off | 2 | `{"temperature": 3.5, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n for i in range(1, 6): \n     for j in range(1, 6): \n         print(f"{i}x{j}={i*j}", end=" ") \n     print |
| penalty_off | 3 | `{"temperature": 3.5, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(n=5): \n     """ \n     Prints a square (n x n) multiplication table. \n     |
| penalty_off | 4 | `{"temperature": 3.5, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n for i in range(1, 6): \n     for j in range(1, 6): \n         print(i * j, end="\t") \n     print() \n ``` |

## Flip check

- temp_07: mixed (failing: 0/4 failed, temp_07: 0/4 failed). Not usable as a clean flip; read the replies
- penalty_off: mixed (failing: 0/4 failed, penalty_off: 0/4 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
