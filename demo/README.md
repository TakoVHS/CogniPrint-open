# CogniPrint Streamlit Demo

This is a local-only interactive demo for exploring CogniPrint profiles.

## Install

From the repository root:

```bash
python -m pip install -e '.[demo]'
```

or:

```bash
python -m pip install -r demo/requirements.txt
```

## Run

```bash
streamlit run demo/app.py
```

The demo supports:

- single-text profile extraction;
- two-text profile comparison;
- optional distance from the bundled sample-corpus mean when sample data is present.

## Boundary

The demo is a descriptive research interface. It does not store input text, call
model APIs, or provide identity, provenance, AI-origin, legal, forensic, or
final decision outputs.
