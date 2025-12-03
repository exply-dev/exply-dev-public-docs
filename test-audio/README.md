# Test Audio Files

Audio files for E2E testing of Orchid + Cursor Cloud integration.

## secret-code.ogg
Russian audio containing a secret numeric code for transcription tests.

Expected result: The transcription should extract a 7-digit number.

Use `python3 scripts/transcribe_secret_code.py` to process the audio with AssemblyAI and store the digits in `test-results/secret-code.txt`.
