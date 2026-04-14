#!/usr/bin/env python3
"""
MillionVerifier Bulk Email Verification

Usage:
    python verify_emails.py <input_csv> [--email-column Email] [--output <path>]

Extracts emails from a CSV, uploads to MillionVerifier bulk API,
polls for completion, downloads results, and merges verification
status back into the original CSV as an "Email Status" column.

Requires MILLIONVERIFIER_API_KEY environment variable.
"""

import argparse
import csv
import io
import os
import sys
import time
import requests


def get_api_key():
    key = os.environ.get("MILLIONVERIFIER_API_KEY")
    if not key:
        print("Error: MILLIONVERIFIER_API_KEY environment variable not set.")
        print("Get your API key from https://app.millionverifier.com/api")
        sys.exit(1)
    return key


def check_credits(api_key):
    resp = requests.get(f"https://api.millionverifier.com/api/v3/credits?api={api_key}")
    if resp.status_code == 200:
        data = resp.json()
        credits = data.get("credits", data.get("data", "unknown"))
        print(f"MillionVerifier credits remaining: {credits}")
        return credits
    else:
        print(f"Warning: Could not check credits (HTTP {resp.status_code})")
        return None


def extract_emails(csv_path, email_column):
    emails = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if email_column not in reader.fieldnames:
            print(f"Error: Column '{email_column}' not found in CSV.")
            print(f"Available columns: {', '.join(reader.fieldnames)}")
            sys.exit(1)
        for row in reader:
            email = row[email_column].strip()
            if email:
                emails.append(email)
    return emails


def upload_emails(api_key, emails):
    email_content = "\n".join(emails)
    email_file = io.BytesIO(email_content.encode("utf-8"))

    resp = requests.post(
        "https://bulkapi.millionverifier.com/bulkapi/v2/upload",
        data={"key": api_key, "remove_duplicates": 1},
        files={"file_contents": ("emails.csv", email_file, "text/csv")},
    )

    data = resp.json()
    if data.get("error"):
        print(f"Upload error: {data['error']}")
        sys.exit(1)

    file_id = data["file_id"]
    print(f"Uploaded {len(emails)} emails. File ID: {file_id}")
    return file_id


def poll_until_done(api_key, file_id):
    while True:
        resp = requests.get(
            f"https://bulkapi.millionverifier.com/bulkapi/v2/fileinfo",
            params={"key": api_key, "file_id": file_id},
        )
        data = resp.json()
        status = data.get("status", "unknown")
        percent = data.get("percent", 0)

        print(f"  Status: {status}  Progress: {percent}%", end="\r", flush=True)

        if status in ("finished", "canceled"):
            print()
            return status

        time.sleep(2)


def download_results(api_key, file_id):
    resp = requests.get(
        "https://bulkapi.millionverifier.com/bulkapi/v2/download",
        params={"key": api_key, "file_id": file_id, "filter": "all"},
    )

    if resp.status_code != 200:
        print(f"Download error: HTTP {resp.status_code}")
        sys.exit(1)

    results = {}
    content = resp.content.decode("utf-8")
    # MV returns CSV with headers: email,quality,result,free,role
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames and "result" in reader.fieldnames:
        for row in reader:
            email = row["email"].strip().lower()
            results[email] = row["result"].strip()
    else:
        # Fallback: assume email,status format
        reader2 = csv.reader(io.StringIO(content))
        for row in reader2:
            if len(row) >= 2:
                email = row[0].strip().lower()
                results[email] = row[1].strip()

    return results


def merge_results(csv_path, email_column, results, output_path):
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    if "Email Status" not in fieldnames:
        fieldnames.append("Email Status")

    verified = 0
    for row in rows:
        email = row.get(email_column, "").strip().lower()
        status = results.get(email, "not_checked")
        row["Email Status"] = status
        if status == "ok":
            verified += 1

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    ok = sum(1 for r in rows if r["Email Status"] == "ok")
    catch_all = sum(1 for r in rows if r["Email Status"] == "catch_all")
    invalid = sum(1 for r in rows if r["Email Status"] == "invalid")
    unknown = sum(1 for r in rows if r["Email Status"] == "unknown")
    disposable = sum(1 for r in rows if r["Email Status"] == "disposable")

    print(f"\nVerification Results:")
    print(f"  Total:      {total}")
    print(f"  OK:         {ok}")
    print(f"  Catch-all:  {catch_all}")
    print(f"  Unknown:    {unknown}")
    print(f"  Invalid:    {invalid}")
    print(f"  Disposable: {disposable}")
    print(f"\nSafe to send: {ok + catch_all} / {total}")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Verify emails via MillionVerifier bulk API")
    parser.add_argument("input_csv", help="Path to CSV file containing emails")
    parser.add_argument("--email-column", default="Email", help="Name of the email column (default: Email)")
    parser.add_argument("--output", help="Output CSV path (default: overwrites input)")
    args = parser.parse_args()

    output_path = args.output or args.input_csv
    api_key = get_api_key()

    print("Checking credits...")
    check_credits(api_key)

    print(f"\nExtracting emails from '{args.email_column}' column...")
    emails = extract_emails(args.input_csv, args.email_column)
    print(f"Found {len(emails)} emails to verify.")

    if not emails:
        print("No emails to verify.")
        sys.exit(0)

    print("\nUploading to MillionVerifier...")
    file_id = upload_emails(api_key, emails)

    print("Waiting for verification...")
    status = poll_until_done(api_key, file_id)

    if status == "canceled":
        print("Verification was canceled.")
        sys.exit(1)

    print("Downloading results...")
    results = download_results(api_key, file_id)

    print(f"Merging results into CSV...")
    merge_results(args.input_csv, args.email_column, results, output_path)


if __name__ == "__main__":
    main()
