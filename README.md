# Password Security Auditor

A command-line tool that audits password strength and checks for known data breaches. Built with Python.

## What it does

Most people reuse weak passwords without realizing their credentials have already been exposed in a data breach somewhere. This tool addresses that by doing two things:

1. **Strength analysis** - scores your password based on length, complexity, and character variety
2. **Breach detection** - checks your password against the HaveIBeenPwned database, which contains over 800 million real-world leaked passwords

The breach check is done using a k-anonymity model, meaning your actual password is never sent over the internet. Only the first 5 characters of its SHA-1 hash are transmitted to the API - the rest is matched locally on your machine.

## Getting started

**Requirements**
- Python 3.x
- `requests` library

**Install dependencies**
```bash
pip3 install requests
```

**Run the tool**
```bash
python3 auditor.py
```

## Usage

**Interactive mode** - prompts you to enter passwords one at a time:
```bash
python3 auditor.py
```

**Batch mode** - pass multiple passwords directly as arguments:
```bash
python3 auditor.py password123 mysecurepass! letmein
```

## Example output
```
==================================================
  PASSWORD AUDIT REPORT
==================================================
  Strength Score : 35/100
  Strength Label : WEAK
  Breach Status  : COMPROMISED (34,521 times)

  Suggestions:
    • Add uppercase letters
    • Add special characters (!@#$% etc)
==================================================
```
## How the breach check works

Sending passwords in plaintext to any external API would be a security risk in itself. To avoid this, the tool implements k-anonymity:

- Your password is hashed using SHA-1
- Only the first 5 characters of that hash are sent to the HIBP API
- The API returns all hash suffixes that match that prefix
- Your tool checks for a match locally - your password never leaves your machine

This is the same method used by major browsers and password managers for breach detection.

## Why I built this

Credential security is one of the most overlooked areas of personal and organizational cybersecurity. Weak and reused passwords remain one of the leading causes of account compromise. I built this tool to make breach awareness accessible and to deepen my understanding of how real-world security APIs handle sensitive data without exposing it. The project was developed and tested locally before being published here as a completed, working codebase.
