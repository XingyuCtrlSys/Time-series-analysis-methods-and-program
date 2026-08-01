# Migration notes

The cleaned repository intentionally does not carry forward the following legacy content:

- `.idea/` project settings;
- the local `Myenv/` virtual environment;
- redundant `.xlsx` copies of the same data;
- nested ZIP archives of generated results;
- empty placeholder files and generated console output;
- public phone numbers and personal contact details;
- filenames encoded as literal `#Uxxxx` sequences;
- the 933-line monolithic script with import-time execution.

The original analysis intent is retained through a modular pipeline, cleaned demonstration data, reproducible outputs, and documented methods.
