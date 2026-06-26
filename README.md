# pc-part-recommender
It will recommend you best 4 main pc parts (CPU, GPU, RAM, Disk memory) .
## How it works
- 10% of budget → Disk 
- 25% of budget → CPU 
- 15% of budget → RAM (DDR type auto-detected from CPU microarchitecture) 
- Remaining (~50%+) → GPU
## Usage 
```
pip install requests 
python main.py 
```
Requirements: Python 3.10+
## Data Sources
I use www.passmark.com website and https://github.com/docyx/pc-part-dataset github datasets for finding prices and the best parts of pc by performance . 
## Limitations
- RAM prices may be stale
- RAM (DDR type auto-detected from CPU microarchitecture) and CPU are compatibale but not the other parts 
- Prices are USD-based (US market only)
