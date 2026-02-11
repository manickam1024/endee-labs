import os
import argparse
import requests
import time

API_URL = "http://localhost:8000/ingest"

def ingest_directory(directory_path: str):
    """
    Walks through a directory and uploads all PDF files to the ContractSentinel API.
    """
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return

    files_processed = 0
    start_time = time.time()

    print(f"🚀 Starting bulk ingestion from: {directory_path}")

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                print(f"Processing: {file}...", end=" ")
                
                try:
                    with open(file_path, "rb") as f:
                        files = {"file": (file, f, "application/pdf")}
                        response = requests.post(API_URL, files=files)
                        
                        if response.status_code == 200:
                            print(f"✅ Success (ID: {response.json().get('document_id')})")
                            files_processed += 1
                        else:
                            print(f"❌ Failed ({response.status_code}: {response.text})")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")

    duration = time.time() - start_time
    print(f"\n✨ Ingestion Complete!")
    print(f"📄 Processed {files_processed} files in {duration:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk ingest PDFs into ContractSentinel.")
    parser.add_argument("directory", help="Path to the directory containing PDFs.")
    args = parser.parse_args()
    
    ingest_directory(args.directory)
