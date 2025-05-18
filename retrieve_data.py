# This module downloads the XML-files as determined in the variables file. It does this through the PubMed URL.

import os                # Needed to use directories in code.
import urllib.request    # For downloading files from URL.
import gzip              # Unzipping files.
from tqdm import tqdm    # Progress bar.

from variables import (
    base_url,
    destination_folder,
    first_file,
    last_file
)

def main():
    # Make the destination folder.
    os.makedirs(destination_folder, exist_ok=True)

    # Track missing files.
    missing_files = []

    # Download and extract files.
    for num in tqdm(range(first_file, last_file + 1), desc="Processing files", unit="file"):
        base_name = f"pubmed25n{num:04d}.xml.gz"
        gz_url = base_url + base_name
        md5_url = gz_url + ".md5"

        gz_path = os.path.join(destination_folder, base_name)
        md5_path = gz_path + ".md5"
        xml_path = gz_path.replace(".gz", "")

        try:
            if not os.path.exists(gz_path):
                urllib.request.urlretrieve(gz_url, gz_path)

            if not os.path.exists(md5_path):
                urllib.request.urlretrieve(md5_url, md5_path)

            if not os.path.exists(xml_path):
                with gzip.open(gz_path, 'rb') as f_in, open(xml_path, 'wb') as f_out:
                    while True:
                        chunk = f_in.read(8192)
                        if not chunk:
                            break
                        f_out.write(chunk)

            if not (os.path.exists(gz_path) and os.path.exists(md5_path) and os.path.exists(xml_path)):
                missing_files.append(base_name)

        except Exception:
            missing_files.append(base_name)

    # Final check and message
    if missing_files:
        raise Exception("Not all files were downloaded or extracted correctly.")
    else:
        print("All .GZ-files have been downloaded and extracted. All .MD5-files have been downloaded.")

if __name__ == "__main__":
    main()
