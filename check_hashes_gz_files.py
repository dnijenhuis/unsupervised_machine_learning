# This module checks the integrity of the downloaded data through .MD5-files/hashes.

import hashlib               # For handling the hashes.
from pathlib import Path     # For working with file system paths.
import re                    # Used to extract hash from .MD5-files.

from variables import destination_folder

# Convert string path to Path object to prevent error in for-loop.
destination_folder = Path(destination_folder)

def main():
    # Calculate the MD5-hash of the file.
    def calculate_md5(filepath, chunk_size=8192):
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # Collect mismatches or malformed/missing files.
    problem_files = []

    # Use for-loop to go through all .md5 files and verify their corresponding .GZ-file.
    for md5_file in sorted(destination_folder.glob("*.xml.gz.md5")):
        with open(md5_file, "r") as f:
            line = f.read().strip()  # Read the line and strip it.

        match = re.match(r"MD5\((.+?)\)=\s*([a-fA-F0-9]+)", line)  # Extract filename and hash.
        if not match:
            problem_files.append(f"{md5_file.name}: malformed MD5 line")  # Invalid format, add to list of problems.
            continue

        target_name = match.group(1)         # Extracted .gz filename.
        expected_hash = match.group(2)       # Extracted expected MD5 hash.
        gz_file = destination_folder / target_name  # Full path to the .gz file.

        actual_hash = calculate_md5(gz_file)  # Compute actual hash of the file.
        if actual_hash != expected_hash:      # Compare hashes.
            problem_files.append(f"{target_name}: hash mismatch")  # Add mismatch to problems list.

    # Print statements.
    if problem_files:
        print("Some .GZ-files did not pass hash verification.\n")
        for problem in problem_files:
            print(f"- {problem}")
    else:
        print("All .GZ-files passed hash verification.")

if __name__ == "__main__":
    main()
