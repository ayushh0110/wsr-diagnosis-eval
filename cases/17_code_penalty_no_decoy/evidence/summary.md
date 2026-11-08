# Capture summary: 17_code_penalty_no_decoy

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, penalty_off; 4 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=5): \n     """Prints an N x N multiplication table.""" \n  \n     print |
| failing | 2 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=10): \n     """Prints an NxN multiplication table.""" \n  \n     # Crea |
| failing | 3 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(size=5): \n     """Prints a square size of x multiplied by itself.""" \n  \n |
| failing | 4 | `{"temperature": 0.7, "repeat_penalty": 1.4, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n def print_multiplication_table(size=10): \n     """Prints an N x N multiplication table.""" \n  \n     prin |
| penalty_off | 1 | `{"temperature": 0.7, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(size=5): \n     """Prints a square multiplication table of the given size."" |
| penalty_off | 2 | `{"temperature": 0.7, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(size=5): \n     """ \n     Prints a square multiplication table of the given |
| penalty_off | 3 | `{"temperature": 0.7, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(size=5): \n     """ \n     Prints a square multiplication table of the given |
| penalty_off | 4 | `{"temperature": 0.7, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n def print_multiplication_table(n=5): \n     """ \n     Prints an n x n multiplication table. \n     """ \n  |

## Flip check

- penalty_off: mixed (failing: 0/4 failed, penalty_off: 0/4 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
