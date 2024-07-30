#!/bin/bash

# Keywords to search for
keywords=(
  "ssh-rsa"
  "ssh-dss"
  "ssh-ed25519"
  "ecdsa-sha2-nistp256"
  "ecdsa-sha2-nistp384"
  "ecdsa-sha2-nistp521"
  "BEGIN RSA PRIVATE KEY"
  "BEGIN DSA PRIVATE KEY"
  "BEGIN OPENSSH PRIVATE KEY"
  "BEGIN ECDSA PRIVATE KEY"
  "BEGIN ED25519 PRIVATE KEY"
)

# Function to search for keywords in a file
search_keywords_in_file() {
  local file=$1
  for keyword in "${keywords[@]}"; do
    if grep -q "$keyword" "$file" 2>/dev/null; then
      echo "$file"
      break
    fi
  done
}

# Function to recursively scan directories with a progress bar
scan_directory() {
  local dir=$1

  # Get the total number of files to be scanned
  total_files=$(find "$dir" -type f 2>/dev/null | wc -l)
  scanned_files=0

  # Process each file and update progress
  find "$dir" -type f 2>/dev/null | while read -r file; do
    search_keywords_in_file "$file"
    scanned_files=$((scanned_files + 1))
    progress=$((scanned_files * 100 / total_files))
    echo -ne "Progress: $progress% ($scanned_files/$total_files)\r"
  done
  echo -ne '\n'
}

# Check if a directory was provided as an argument, default to root if not
dir_to_scan=${1:-/}

echo "Scanning directory $dir_to_scan for SSH key related terms..."

# Start scanning
scan_directory "$dir_to_scan"

echo "Scan complete."
