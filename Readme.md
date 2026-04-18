# Project Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git (optional, for cloning repository)

## Installation Steps

### 1. Clone Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Project

```bash
python main.py
```

## Deactivate Virtual Environment

```bash
deactivate
```

## Troubleshooting

- Ensure Python is added to PATH
- Use `python3` instead of `python` if needed
- Verify pip is installed: `pip --version`
