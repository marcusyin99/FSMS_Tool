import time
import pyperclip
import requests
import re
import csv
from datetime import datetime
from tqdm import tqdm
from plyer import notification

def extract_product_name(response_text):
    # Try using regex to find productName as the structure might be nested
    match = re.search(r'"productName"\s*:\s*"([^"]+)"', response_text)
    if match:
        return match.group(1)
    return "Unknown/Not Found"

def check_warranty(serial_number):
    url = f"https://support.hp.com/wcc-services/searchresult/my-en?q={serial_number}&context=pdp&authState=anonymous&template=WarrantyLanding"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://support.hp.com/my-en/check-warranty"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return extract_product_name(response.text)
        else:
            return f"HTTP Error {response.status_code}"
    except Exception as e:
        return f"Request Error: {str(e)}"

def looks_like_serial_numbers(text):
    if not text or not text.strip():
        return False
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return False
        
    # Check if lines look like serial numbers (alphanumeric, reasonable length, no spaces)
    for line in lines:
        if " " in line or len(line) < 5 or len(line) > 20 or not line.isalnum():
            # Might not be a serial number list
            # We can be a bit more lenient, maybe just checking if space is in line, HP serials are typically ~10 chars
            return False
            
    return True

def main():
    print("Starting clipboard listener for HP Warranty Serial Numbers...")
    print("Copy a list of serial numbers (one per line) to trigger the search.")
    print("Press Ctrl+C to exit.\n")
    
    last_clipboard_data = ""

    try:
        while True:
            current_clipboard_data = pyperclip.paste()
            
            # Check if clipboard changed and looks like a list of serial numbers
            if current_clipboard_data != last_clipboard_data:
                last_clipboard_data = current_clipboard_data
                
                if looks_like_serial_numbers(current_clipboard_data):
                    serial_numbers = [line.strip() for line in current_clipboard_data.splitlines() if line.strip()]
                    print(f"\nDetected {len(serial_numbers)} serial numbers. Starting search...")
                    results = []
                    
                    for sn in tqdm(serial_numbers, desc="Checking Warranties", unit="sn"):
                        product_name = check_warranty(sn)
                        # Use tqdm.write instead of print to avoid messing up the progress bar
                        tqdm.write(f"[{sn}] : [{product_name}]")
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        results.append([timestamp, sn, product_name])
                        
                        # Add a small delay between requests to be polite and avoid rate limits
                        time.sleep(1)
                        
                    # Append results to CSV
                    csv_filename = "results.csv"
                    file_exists = False
                    try:
                        with open(csv_filename, "r", encoding="utf-8") as f:
                            file_exists = True
                    except FileNotFoundError:
                        pass
                        
                    with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(["Timestamp", "Serial Number", "Product Name"])
                        writer.writerows(results)
                        
                    try:
                        notification.notify(
                            title="HP Warranty Bulk Search",
                            message=f"Search complete for {len(serial_numbers)} serial numbers! Results saved to {csv_filename}.",
                            app_name="Warranty Checker",
                            timeout=5
                        )
                    except Exception as e:
                        print(f"Skipping notification due to error: {e}")
                        
                    print(f"\nSearch complete. Results saved to {csv_filename}. Waiting for new clipboard... \n")

            time.sleep(1) # Check clipboard every 1 second
            
    except KeyboardInterrupt:
        print("\nExiting listener.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
