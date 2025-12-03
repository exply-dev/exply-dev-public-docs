#!/usr/bin/env python3
"""Transcribe the sample audio file with AssemblyAI and store the result.

The script submits the hosted audio file to AssemblyAI, polls until the
transcription finishes, and writes the transcript to
`test-audio/transcription-result.txt`. Set the ASSEMBLYAI_API_KEY environment
variable before running the script. Optionally override ASSEMBLYAI_API_BASE_URL
to point at an AssemblyAI-compatible mock for testing.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict
from urllib import error, request

AUDIO_SOURCE_URL = (
    "https://raw.githubusercontent.com/exply-dev/"
    "exply-dev-public-docs/main/test-audio/secret-code.ogg"
)
API_BASE_URL = os.getenv("ASSEMBLYAI_API_BASE_URL", "https://api.assemblyai.com/v2").rstrip("/")
TRANSCRIPT_ENDPOINT = f"{API_BASE_URL}/transcript"
POLL_INTERVAL_SECONDS = 3
POLL_TIMEOUT_SECONDS = 8 * 60  # ample time for AssemblyAI to finish

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT_DIR / "test-audio" / "transcription-result.txt"


class AssemblyAIError(RuntimeError):
    """Raised when the AssemblyAI API reports an error."""


def main() -> int:
    """Kick off the transcription flow."""
    api_key = _require_api_key()
    transcript_id = _create_transcription_request(api_key)
    transcript_text = _wait_for_transcript(api_key, transcript_id)
    _write_transcript_file(transcript_text)
    print(
        f"Transcript saved to {OUTPUT_PATH.relative_to(ROOT_DIR)} "
        f"({len(transcript_text)} characters)."
    )
    return 0


def _require_api_key() -> str:
    key = os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise SystemExit(
            "Missing ASSEMBLYAI_API_KEY environment variable. "
            "Set it to your AssemblyAI API token and retry."
        )
    return key.strip()


def _create_transcription_request(api_key: str) -> str:
    payload = {"audio_url": AUDIO_SOURCE_URL}
    response = _perform_request("POST", TRANSCRIPT_ENDPOINT, api_key, payload)
    transcript_id = response.get("id")
    if not transcript_id:
        raise AssemblyAIError(
            f"AssemblyAI response missing transcript id: {json.dumps(response, indent=2)}"
        )
    print(f"Submitted transcription job {transcript_id}.")
    return transcript_id


def _wait_for_transcript(api_key: str, transcript_id: str) -> str:
    """Poll AssemblyAI until the transcript is ready or an error occurs."""
    deadline = time.time() + POLL_TIMEOUT_SECONDS
    while True:
        response = _perform_request(
            "GET", f"{TRANSCRIPT_ENDPOINT}/{transcript_id}", api_key
        )
        status = response.get("status")
        if status == "completed":
            text = response.get("text") or ""
            if not text.strip():
                raise AssemblyAIError("AssemblyAI returned an empty transcript.")
            return text
        if status == "error":
            error_message = response.get("error", "AssemblyAI reported an error.")
            raise AssemblyAIError(error_message)
        if time.time() > deadline:
            raise AssemblyAIError(
                f"Timed out waiting for transcript. Last status payload: {response}"
            )
        print(f"Current status: {status}. Waiting {POLL_INTERVAL_SECONDS}s...")
        time.sleep(POLL_INTERVAL_SECONDS)


def _write_transcript_file(transcript_text: str) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(transcript_text.strip() + "\n", encoding="utf-8")


def _perform_request(
    method: str, url: str, api_key: str, payload: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    data: bytes | None = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, data=data, method=method)
    req.add_header("Authorization", api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except error.HTTPError as exc:  # pragma: no cover - for clarity
        body = exc.read().decode("utf-8", errors="replace")
        raise AssemblyAIError(
            f"AssemblyAI returned HTTP {exc.code}: {body}"
        ) from exc
    except error.URLError as exc:  # pragma: no cover - for clarity
        raise AssemblyAIError(f"Unable to reach AssemblyAI: {exc}") from exc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssemblyAIError as err:
        print(f"Transcription failed: {err}", file=sys.stderr)
        sys.exit(1)
