"""
Utility to extract Reddit submissions and comments from .zst NDJSON dumps
into CSVs suitable for sentiment analysis.

Reads the raw files under ``Data/Reddit Data/Reddit raw`` for the
democrats and republican subreddits, filters the timeframe
2020-10-15 through 2020-11-08 (inclusive), normalizes fields, and
writes one CSV per subreddit containing both submissions and comments.
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional

import zstandard
import pandas as pd

# Date window for filtering (inclusive)
DATE_FROM = date(2020, 10, 15)
DATE_TO = date(2020, 11, 8)

# Output columns aligned with the Twitter-like schema
OUTPUT_COLUMNS = [
    "id",
    "type",
    "subreddit",
    "author",
    "date",
    "score",
    "title",
    "content",
    "url",
    "parent_id",
    "link_id",
]


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def utc_date_from_timestamp(ts: str) -> date:
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).date()


def stream_zst_ndjson(path: Path, chunk_size: int = 1 << 23) -> Iterator[str]:
    """
    Stream NDJSON. If the file has zstd magic bytes, decompress; otherwise
    treat as plain UTF-8 text.
    """
    with path.open("rb") as fh:
        header = fh.peek(4) if hasattr(fh, "peek") else fh.read(4)
        if not hasattr(fh, "seek"):
            raise RuntimeError("File handle is not seekable")
        fh.seek(0)
        magic = b"\x28\xb5\x2f\xfd"
        if header.startswith(magic):
            reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(fh)
            buffer = ""
            while True:
                chunk = reader.read(chunk_size)
                if not chunk:
                    break
                decoded = chunk.decode("utf-8", errors="replace")
                lines = (buffer + decoded).split("\n")
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        yield line
                buffer = lines[-1]
            reader.close()
            if buffer.strip():
                yield buffer.strip()
        else:
            # Plain text NDJSON
            for raw_line in fh:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if line:
                    yield line


def normalize_record(obj: Dict, is_submission: bool) -> Optional[Dict]:
    """
    Normalize a Reddit JSON object to the target schema.
    Returns None if the record is outside the date window.
    """
    try:
        created = utc_date_from_timestamp(str(obj["created_utc"]))
    except Exception:
        logging.debug("Skipping record without valid created_utc: %s", obj)
        return None

    if created < DATE_FROM or created > DATE_TO:
        return None

    subreddit = obj.get("subreddit", "")
    author = obj.get("author", "")
    score = obj.get("score", 0)
    url = obj.get("permalink")

    if not url:
        if is_submission and "permalink" in obj:
            url = f"https://www.reddit.com{obj['permalink']}"
        elif not is_submission and "link_id" in obj and "id" in obj:
            link = str(obj["link_id"]).replace("t3_", "")
            url = f"https://www.reddit.com/r/{subreddit}/comments/{link}/_/{obj['id']}"
        else:
            url = ""
    else:
        if not url.startswith("http"):
            url = f"https://www.reddit.com{url}"

    title = obj.get("title", "") if is_submission else ""
    content = ""
    if is_submission:
        if obj.get("is_self"):
            content = obj.get("selftext", "") or ""
        else:
            content = obj.get("selftext", "") or ""
    else:
        content = obj.get("body", "") or ""

    record = {
        "id": obj.get("id", ""),
        "type": "submission" if is_submission else "comment",
        "subreddit": subreddit,
        "author": author,
        "date": created.isoformat(),
        "score": score,
        "title": title,
        "content": content,
        "url": url,
        "parent_id": obj.get("parent_id", "") if not is_submission else "",
        "link_id": obj.get("link_id", "") if not is_submission else "",
    }
    return record


def process_file(path: Path, is_submission: bool) -> Iterator[Dict]:
    """
    Stream a .zst NDJSON file and yield normalized records within date window.
    """
    for line in stream_zst_ndjson(path):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            logging.debug("Skipping malformed JSON line")
            continue
        record = normalize_record(obj, is_submission)
        if record:
            yield record


def find_input_file(base_dir: Path, subreddit: str, kind: str) -> Path:
    """
    Find the input file for a subreddit and kind ('submissions' or 'comments').
    Performs a case-insensitive search on filenames containing the subreddit name and kind.
    """
    candidates = []
    for path in base_dir.iterdir():
        if not path.is_file():
            continue
        name_lower = path.name.lower()
        if subreddit.lower() in name_lower and kind in name_lower:
            candidates.append(path)
    if not candidates:
        raise FileNotFoundError(
            f"No file found in {base_dir} for subreddit '{subreddit}' and kind '{kind}'"
        )
    # Prefer the shortest match to avoid surprises
    return sorted(candidates, key=lambda p: len(p.name))[0]


def write_csv(records: Iterable[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records, columns=OUTPUT_COLUMNS)
    df.to_csv(output_path, index=False, encoding="utf-8")
    logging.info("Wrote %s (%d rows)", output_path, len(df))


def process_subreddit(
    base_dir: Path, subreddit: str, output_dir: Path
) -> Path:
    """
    Process submissions and comments for one subreddit and write combined CSV.
    """
    submissions_file = find_input_file(base_dir, subreddit, "submission")
    comments_file = find_input_file(base_dir, subreddit, "comment")

    logging.info(
        "Processing subreddit '%s' from %s and %s",
        subreddit,
        submissions_file.name,
        comments_file.name,
    )

    records = list(process_file(submissions_file, is_submission=True))
    records.extend(process_file(comments_file, is_submission=False))

    output_name = f"{subreddit.lower()}_posts_{DATE_FROM.isoformat()}_{DATE_TO.isoformat()}.csv"
    output_path = output_dir / output_name
    write_csv(records, output_path)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Reddit data to CSV.")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("Data/Reddit Data/Reddit raw"),
        help="Directory containing raw Reddit .zst files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Data/Reddit Data/processed"),
        help="Directory to write CSV outputs.",
    )
    parser.add_argument(
        "--subreddits",
        nargs="+",
        default=["democrats", "republican"],
        help="List of subreddit file prefixes to process.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    args = parser.parse_args()

    configure_logging(verbose=args.verbose)

    if not args.base_dir.exists():
        raise FileNotFoundError(f"Base directory not found: {args.base_dir}")

    outputs: List[Path] = []
    for sub in args.subreddits:
        try:
            outputs.append(process_subreddit(args.base_dir, sub, args.output_dir))
        except Exception as exc:  # surface which subreddit failed
            logging.error("Failed processing %s: %s", sub, exc)
            raise

    logging.info("Completed. Outputs: %s", ", ".join(str(p) for p in outputs))


if __name__ == "__main__":
    main()

