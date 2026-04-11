import time
import pyperclip
import requests
import re
import csv
import json
from datetime import datetime
from tqdm import tqdm
from plyer import notification

def extract_hp_info(response_text):
    name_match = re.search(r'"productName"\s*:\s*"([^"]+)"', response_text)
    num_match = re.search(r'"productNumber"\s*:\s*"([^"]+)"', response_text)
    url_match = re.search(r'"targetUrl"\s*:\s*"([^"]+)"', response_text)
    
    return {
        "brand": "HP",
        "sn": re.search(r'"serialNumber"\s*:\s*"([^"]+)"', response_text).group(1) if re.search(r'"serialNumber"', response_text) else "N/A",
        "name": name_match.group(1) if name_match else "Unknown",
        "number": num_match.group(1) if num_match else "N/A",
        "url": f"https://support.hp.com{url_match.group(1)}" if url_match else "",
        "start": "Refer to Link", "end": "Refer to Link", "status": "Refer to Link"
    }

def detect_brand(sn):
    sn = sn.upper()
    # Lenovo pattern: 8-10 chars, often starting with PF, MJ, MJ0
    if (len(sn) >= 8 and len(sn) <= 10) and (sn.startswith('PF') or sn.startswith('MJ')):
        return "LENOVO"
    # Dell pattern: Exactly 7 characters, alphanumeric (Service Tag)
    if len(sn) == 7 and sn.isalnum():
        return "DELL"
    return "HP"

def check_hp_warranty(sn):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    # Step 1: Prime the session with the GET search (Handshake Phase)
    get_url = f"https://support.hp.com/wcc-services/searchresult/my-en?q={sn}&context=pdp&authState=anonymous&template=WarrantyLanding"
    try:
        get_response = session.get(get_url, timeout=10)
        if get_response.status_code != 200:
            return {"brand": "HP", "name": f"HTTP {get_response.status_code}", "number": "N/A", "url": "", "start": "Refer to Link", "end": "Refer to Link", "status": "Refer to Link"}
        
        info = extract_hp_info(get_response.text)
        pn = info['number']
        
        # Step 2: Precise POST Signature to fetch exact dates
        if pn != "N/A":
            post_url = "https://support.hp.com/wcc-services/profile/devices/warranty/specs?authState=anonymous&template=ProductModel"
            post_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Origin': 'https://support.hp.com',
                'Referer': 'https://www.google.com/search?q=https://support.hp.com/my-en/warrantyresult',
                'X-Requested-With': 'XMLHttpRequest'
            }
            # Match the exact payload structure required by HP
            payload = {
                "cc": "my", 
                "lc": "en", 
                "utcOffset": "P0800", 
                "devices": [
                    {"serialNumber": sn, "productNumber": pn, "countryOfPurchase": "my"}
                ], 
                "captchaToken": ""
            }
            
            post_response = session.post(post_url, headers=post_headers, json=payload, timeout=10)
            
            if post_response.status_code == 200:
                post_data = post_response.json()
                # HP returns a list of devices in the data field
                devices = post_data.get('devices', [])
                if devices:
                    dev = devices[0]
                    info["start"] = dev.get('warrantyStartDate', "Refer to Link")
                    info["end"] = dev.get('warrantyEndDate', "Refer to Link")
                    # Optionally update status based on expiration
                    from datetime import datetime
                    try:
                        end_dt = datetime.strptime(info["end"], "%Y-%m-%d")
                        if end_dt < datetime.now():
                            info["status"] = "Expired"
                        else:
                            info["status"] = "Active"
                    except:
                        info["status"] = "N/A"
        
        return info
    except Exception as e:
        return {"brand": "HP", "name": f"Error: {str(e)}", "number": "N/A", "url": "", "start": "Refer to Link", "end": "Refer to Link", "status": "Refer to Link"}

def check_lenovo_warranty(sn):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-MY,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    })
    
    try:
        # Step 1: Handshake to collect Akamai/Service cookies
        handshake_url = f"https://pcsupport.lenovo.com/my/en/products/search?query={sn}"
        session.get(handshake_url, timeout=10)
        
        # Human mimicry delay
        time.sleep(1)
        
        # Step 2: Fetch the actual warranty page
        target_url = f"https://pcsupport.lenovo.com/my/en/products/{sn}/warranty"
        response = session.get(target_url, timeout=15)
        
        if response.status_code == 403:
            # Retry once with longer delay if blocked
            time.sleep(2)
            response = session.get(target_url, timeout=15)

        if response.status_code == 200:
            # Step 3: Extract ds_warranties JSON from HTML
            # This regex handles the modern window.ds_warranties structure
            regex = r'var\s+ds_warranties\s*=\s*window\.ds_warranties\s*\|\|\s*(\{.*?\});'
            match = re.search(regex, response.text, re.DOTALL)
            
            if match:
                data = json.loads(match.group(1))
                
                # Fetch product name (often at root or in nested dict)
                # If ProductName isn't in warranties, try to find productinfo in same way
                prod_name = "Unknown Lenovo Model"
                prod_match = re.search(r'var\s+ds_productinfo\s*=\s*window\.ds_productinfo\s*\|\|\s*(\{.*?\});', response.text, re.DOTALL)
                if prod_match:
                    p_info = json.loads(prod_match.group(1))
                    prod_name = p_info.get('ProductName', prod_name)

                res = {
                    "brand": "LENOVO",
                    "sn": sn,
                    "name": prod_name,
                    "number": sn,
                    "url": f"https://pcsupport.lenovo.com/my/en/products/{sn}/warranty",
                    "start": "N/A", "end": "N/A", "status": "N/A"
                }
                
                base_warranties = data.get('BaseWarranties', [])
                if base_warranties:
                    base = base_warranties[0]
                    res["start"] = base.get('Start', 'N/A')
                    res["end"] = base.get('End', 'N/A')
                    res["status"] = base.get('StatusV2', 'N/A')
                return res

        return {"brand": "LENOVO", "name": "Not Found / Blocked", "number": sn, "url": "", "start": "N/A", "end": "N/A", "status": "N/A"}
    except Exception as e:
        return {"brand": "LENOVO", "name": f"Session Error: {str(e)}", "number": sn, "url": "", "start": "N/A", "end": "N/A", "status": "N/A"}

def check_dell_warranty(sn):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-MY,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.dell.com/support/home/en-my',
    })
    
    try:
        # Handshake: Prime the session to bypass Akamai Access Denied
        prime_url = f"https://www.dell.com/support/home/en-my/product-support/servicetag/{sn}/warranty"
        session.get(prime_url, timeout=10)
        time.sleep(1)
        
        # Identity: Fetch the MFE component page for the model name
        url = f"https://www.dell.com/support/productsmfe/en-my/productdetails?selection={sn}&assettype=svctag&appname=warranty&inccomponents=false&isolated=false"
        response = session.get(url, timeout=10)
        
        model_name = "Unknown Dell Model"
        if response.status_code == 200:
            match = re.search(r'<h4[^>]*>(.*?)</h4>', response.text, re.IGNORECASE | re.DOTALL)
            if match:
                model_name = match.group(1).strip()
        elif response.status_code == 403:
            model_name = "Access Denied (Akamai Block)"
        
        return {
            "brand": "DELL",
            "sn": sn,
            "name": model_name,
            "number": sn,
            "url": f"https://www.dell.com/support/home/en-my/product-support/servicetag/{sn}/warranty",
            "start": "Refer to Link", 
            "end": "Refer to Link", 
            "status": "Refer to Link"
        }
    except Exception as e:
        return {"brand": "DELL", "name": f"Dell Error: {str(e)}", "number": sn, "url": "", "start": "Refer to Link", "end": "Refer to Link", "status": "Refer to Link"}

def check_warranty(sn):
    # Normalize S/N to uppercase for consistency in URLs and Results
    sn = sn.strip().upper()
    brand = detect_brand(sn)
    if brand == "LENOVO":
        return check_lenovo_warranty(sn)
    if brand == "DELL":
        return check_dell_warranty(sn)
    return check_hp_warranty(sn)

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
    print("Starting clipboard listener for HP/Lenovo/Dell Warranty Serial Numbers...")
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
                        info = check_warranty(sn)
                        full_url = info['url'] if info['url'] else "None"
                        
                        tqdm.write(f"[{info['brand']}][{sn}] : {info['name']} | Status: {info['status']}")
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        results.append([timestamp, info['brand'], sn, info['name'], info['number'], info['start'], info['end'], info['status'], full_url])
                        
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
                            writer.writerow(["Timestamp", "Brand", "Serial Number", "Product Name", "Product Number", "Start Date", "End Date", "Status", "Deep Link"])
                        writer.writerows(results)
                        
                    try:
                        notification.notify(
                            title="Warranty Toolbelt Sync",
                            message=f"Search complete for {len(serial_numbers)} serials! Results added to {csv_filename}.",
                            app_name="Toolbelt",
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
