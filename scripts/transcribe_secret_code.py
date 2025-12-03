#!/usr/bin/env python3
"""Transcribe the secret code audio via AssemblyAI and store the numeric code."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.request
from typing import Dict, Optional

ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
UPLOAD_ENDPOINT = f"{ASSEMBLYAI_API_BASE}/upload"
TRANSCRIPT_ENDPOINT = f"{ASSEMBLYAI_API_BASE}/transcript"

DEFAULT_POLL_INTERVAL = 3
DEFAULT_TIMEOUT = 300

WORD_TO_DIGIT: Dict[str, str] = {
    "zero": "0",
    "ноль": "0",
    "нуль": "0",
    "нолик": "0",
    "one": "1",
    "один": "1",
    "одна": "1",
    "одно": "1",
    "unit": "1",
    "two": "2",
    "два": "2",
    "две": "2",
    "pair": "2",
    "three": "3",
    "три": "3",
    "чет": "4",
    "four": "4",
    "четыре": "4",
    "chetire": "4",
    "пять": "5",
    "five": "5",
    "шесть": "6",
    "six": "6",
    "семь": "7",
    "семерка": "7",
    "семёрка": "7",
    "seven": "7",
    "восемь": "8",
    "eight": "8",
    "девять": "9",
    "девятка": "9",
    "nine": "9",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe test audio with AssemblyAI and extract the numeric code."
    )
    parser.add_argument(
        "--input",
        default="test-audio/secret-code-ru.ogg",
        type=pathlib.Path,
        help="Path to the input audio file (default: test-audio/secret-code-ru.ogg)",
    )
    parser.add_argument(
        "--output",
        default="test-results/secret-code.txt",
        type=pathlib.Path,
        help="Path to the file that will store the extracted code (default: test-results/secret-code.txt)",
    )
    parser.add_argument(
        "--language",
        default="ru",
        help="AssemblyAI language code to help transcription accuracy (default: ru)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help=f"Seconds between polling AssemblyAI for transcript status (default: {DEFAULT_POLL_INTERVAL})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Maximum seconds to wait for transcription before failing (default: {DEFAULT_TIMEOUT})",
    )
    return parser.parse_args()


def load_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise SystemExit("Environment variable ASSEMBLYAI_API_KEY is required to call AssemblyAI.")
    return api_key


def upload_audio(audio_path: pathlib.Path, api_key: str) -> str:
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/octet-stream",
    }
    with audio_path.open("rb") as audio_file:
        data = audio_file.read()

    request = urllib.request.Request(UPLOAD_ENDPOINT, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read())
    upload_url = payload.get("upload_url")
    if not upload_url:
        raise RuntimeError("AssemblyAI upload response did not include upload_url.")
    return upload_url


def create_transcript(audio_url: str, api_key: str, language: Optional[str]) -> str:
    payload = {"audio_url": audio_url}
    if language:
        payload["language_code"] = language

    request = urllib.request.Request(
        TRANSCRIPT_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read())
    transcript_id = data.get("id")
    if not transcript_id:
        raise RuntimeError("AssemblyAI transcript response did not include id.")
    return transcript_id


def poll_transcript(
    transcript_id: str,
    api_key: str,
    poll_interval: int,
    timeout: int,
) -> str:
    url = f"{TRANSCRIPT_ENDPOINT}/{transcript_id}"
    headers = {"Authorization": api_key}
    start = time.monotonic()
    last_status = None

    while True:
        request = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read())

        status = data.get("status")
        if status != last_status:
            print(f"Transcript status: {status}")
            last_status = status

        if status == "completed":
            return data.get("text", "")
        if status == "error":
            raise RuntimeError(f"AssemblyAI reported an error: {data.get('error')}")

        elapsed = time.monotonic() - start
        if elapsed > timeout:
            raise TimeoutError(f"Timed out waiting for transcript {transcript_id}.")
        time.sleep(max(1, poll_interval))


def extract_numeric_code(transcript_text: str) -> str:
    digit_groups = re.findall(r"\d+", transcript_text)
    if digit_groups:
        return "".join(digit_groups)

    normalized_tokens = re.findall(r"[0-9A-Za-zА-Яа-яЁё]+", transcript_text.lower())
    digits = [WORD_TO_DIGIT[token] for token in normalized_tokens if token in WORD_TO_DIGIT]
    if digits:
        return "".join(digits)

    raise ValueError("Could not extract a numeric code from the transcript text.")


def ensure_input(audio_path: pathlib.Path) -> None:
    if not audio_path.is_file():
        raise SystemExit(f"Input audio file not found: {audio_path}")


def store_code(code: str, output_path: pathlib.Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{code}\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    ensure_input(args.input)
    api_key = load_api_key()

    try:
        print(f"Uploading audio file: {args.input}")
        upload_url = upload_audio(args.input, api_key)
        print("Audio uploaded successfully.")

        print("Creating transcript job...")
        transcript_id = create_transcript(upload_url, api_key, args.language)
        print(f"Transcript job created with id: {transcript_id}")

        transcript_text = poll_transcript(
            transcript_id,
            api_key,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )
        print("Transcript completed.")

        code = extract_numeric_code(transcript_text)
        store_code(code, args.output)
        print(f"Secret code extracted and saved to: {args.output}")
    except urllib.error.HTTPError as error:
        message = error.read().decode() if error.fp else ""
        raise SystemExit(f"HTTP error {error.code}: {error.reason} {message}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Network error while calling AssemblyAI: {error.reason}") from error
    except Exception as error:  # noqa: broad-except - CLI feedback
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
