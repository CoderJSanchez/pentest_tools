import os
import re
import argparse

# Keywords to search for
keywords = [
    "ssh-rsa",
    "ssh-dss",
    "ssh-ed25519",
    "ecdsa-sha2-nistp256",
    "ecdsa-sha2-nistp384",
    "ecdsa-sha2-nistp521",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN DSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN ECDSA PRIVATE KEY",
    "BEGIN ED25519 PRIVATE KEY"
]

# Function to search for keywords in a file
def search_keywords_in_file(file_path, keywords):
    try:
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read()
            for keyword in keywords:
                if re.search(keyword, content):
                    return True
    except (IOError, OSError):
        pass
    return False

# Function to recursively scan directories
def scan_directory(dir_to_scan, keywords):
    file_paths = []
    for root, _, files in os.walk(dir_to_scan):
        for file in files:
            file_paths.append(os.path.join(root, file))

    total_files = len(file_paths)
    found_files = []

    for idx, file_path in enumerate(file_paths):
        if search_keywords_in_file(file_path, keywords):
            found_files.append(file_path)
            print(file_path)
        progress = (idx + 1) * 100 / total_files
        print(f"Progress: {progress:.2f}% ({idx + 1}/{total_files})", end='\r')

    print('\n')
    return found_files

# Main function
def main():
    parser = argparse.ArgumentParser(description="Scan directories for SSH key related terms.")
    parser.add_argument("directory", nargs="?", default="/", help="Directory to scan (default is root '/').")
    args = parser.parse_args()

    print(f"Scanning directory {args.directory} for SSH key related terms...")
    scan_directory(args.directory, keywords)
    print("Scan complete.")

if __name__ == "__main__":
    main()
