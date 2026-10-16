# Smart Virtual Assistant

A collaborative smart virtual assistant project .

## Prerequisites
- Python $\ge 3.10$
- Git

## Setup
Clone the repository and set up the local development environment:

```bash
git clone https://github.com/<your-org>/assistant-teamNN.git
cd assistant-teamNN
python -m venv .venv
# macOS / Linux / Git Bash:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install -e .
```

## Run
Run the assistant application:
```bash
python -m assistant "where is the training office?"
```

## Test
Run automated tests using pytest:
```bash
pytest -q
```

## Project Structure
```text
assistant-teamNN/
├── README.md           # Onboarding contract and documentation
├── .gitignore          # Files and folders to ignore in Git
├── requirements.txt    # Pinned Python dependencies
├── pyproject.toml      # Project metadata
├── src/                # Backend application code
├── ui/                 # User interface design and planning
├── data/               # Sample data sources (e.g., offices.csv)
├── tests/              # Automated tests
├── docs/               # Team documentation and logs
└── scripts/            # Helper scripts (e.g., check_env.py)
```

## Troubleshooting
- **`No module named assistant`**: Ensure your virtual environment is active and you have run `pip install -e .`.
- **PowerShell script execution error**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.