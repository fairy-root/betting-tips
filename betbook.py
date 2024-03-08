import requests
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64decode

class Security:
    ALGORITHM = 'AES'
    EncryptionKey = '1BBE0E5E-4DAE-4B83-BF9A-C4029077B0BE'.encode('utf-8')
    key_iv = EncryptionKey[:16]  # Use the first 16 bytes for both key and IV
    
    @staticmethod
    def Decrypt(token):
        try:
            backend = default_backend()
            cipher = Cipher(algorithms.AES(Security.key_iv), modes.CBC(Security.key_iv), backend=backend)
            decryptor = cipher.decryptor()
            ct = b64decode(token)
            padded_data = decryptor.update(ct) + decryptor.finalize()
            
            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data.decode('utf-8')
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None
        
    @staticmethod
    def is_base64(sb):
        try:
            if isinstance(sb, str):
                # If there's any unicode that's not ASCII, this will raise an error
                sb_bytes = bytes(sb, 'ascii')
            elif isinstance(sb, bytes):
                sb_bytes = sb
            else:
                raise ValueError("Argument must be string or bytes")
            return b64decode(sb_bytes, validate=True)
        except Exception:
            return False

    @staticmethod
    def decrypt_json(data):
        if isinstance(data, str) and data.endswith('=='):
            # Attempt to decrypt only if the string ends with '=='
            decrypted_data = Security.Decrypt(data)
            return decrypted_data if decrypted_data is not None else data  # Return original data if decryption fails
        elif isinstance(data, dict):
            return {k: Security.decrypt_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [Security.decrypt_json(item) for item in data]
        else:
            return data  # Non-string, non-iterable types are returned as-is
        
    def decrypt_text(encrypted_text):
        try:
            backend = default_backend()
            cipher = Cipher(algorithms.AES(Security.key_iv), modes.CBC(Security.key_iv), backend=backend)
            decryptor = cipher.decryptor()
            ct = b64decode(encrypted_text)
            padded_data = decryptor.update(ct) + decryptor.finalize()
            
            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data.decode('utf-8')
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

def main(url):
    # URL and headers based on your description
    headers = {
        "Host": "bettingtips-api.azurewebsites.net",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }

    # Send the request
    response = requests.get(url, headers=headers)

    # Ensure the request was successful
    # Ensure the request was successful
    if response.status_code == 200:
        # Load JSON data from the response
        json_data = response.json()

        # Convert the JSON data to a string to check for '='
        json_str = json.dumps(json_data)
        
        # Apply decrypt_json repeatedly until there are no '=' signs in the string representation of the JSON
        if '=' in json_str:
            json_data = Security.decrypt_json(json_data)
            json_str = json.dumps(json_data)
            response_json = Security.decrypt_json(json_str)

            try:
                data = json.loads(response_json)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                data = {}
            
        
        # Check if the 'CategoryList' key is in the data and it's not empty
    if 'CategoryList' in data and data['CategoryList']:
        for category in data['CategoryList']:
            if 'CouponList' in category and category['CouponList']:
                for coupon in category['CouponList']:
                    print(f"\nDate: {coupon.get('Date', 'N/A')}\n")
                    if 'MatchList' in coupon and coupon['MatchList']:
                        for match in coupon['MatchList']:
                            if "=" in f"{match.get('Visitor', 'N/A')}":
                                visit = f"{match.get('Visitor', 'N/A')}"
                                visitor = Security.decrypt_text(visit)
                            else:
                                visitor = f"{match.get('Visitor', 'N/A')}"
                            if "=" in f"{match.get('Home', 'N/A')}":
                                ho = f"{match.get('Home', 'N/A')}"
                                home = Security.decrypt_text(ho)
                            else:
                                home = f"{match.get('Home', 'N/A')}"
                            if "=" in f"{match.get('League', 'N/A')}":
                                leag = f"{match.get('League', 'N/A')}"
                                league = Security.decrypt_text(leag)
                            else:
                                league = f"{match.get('League', 'N/A')}"
                            if "=" in f"{match.get('Bet', 'N/A')}":
                                be = f"{match.get('Bet', 'N/A')}"
                                bet = Security.decrypt_text(be)
                            else:
                                bet = f"{match.get('Bet', 'N/A')}"
                            if "=" in f"{match.get('HomeScore', 'N/A')}":
                                hosc = f"{match.get('HomeScore', 'N/A')}"
                                homescore = Security.decrypt_text(hosc)
                            else:
                                homescore = f"{match.get('HomeScore', 'N/A')}"
                            if "=" in f"{match.get('VisitorScore', 'N/A')}":
                                visc = f"{match.get('VisitorScore', 'N/A')}"
                                visitorscore = Security.decrypt_text(visc)
                            else:
                                visitorscore = f"{match.get('VisitorScore', 'N/A')}"
                            if "=" in f"{match.get('Rate', 'N/A')}":
                                rat = f"{match.get('Rate', 'N/A')}"
                                rate = Security.decrypt_text(rat)
                            else:
                                rate = f"{match.get('Rate', 'N/A')}"
                            if "=" in f"{match.get('Time', 'N/A')}":
                                tim = f"{match.get('Time', 'N/A')}"
                                time = Security.decrypt_text(tim)
                            else:
                                time = f"{match.get('Time', 'N/A')}"
                            match_details = (
                                f"League: {league.strip()}\n"
                                f"Time: {time.strip()}\n"
                                f"{home.strip()} VS {visitor.strip()}\n"
                                f"{homescore.strip()} - {visitorscore.strip()}\n"
                                f"Bet: {bet.strip()}\n"
                                f"Rate: {rate.strip()}\n"
                            )
                            print(match_details)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    user = input("1- Elite VIP\n2- Fixed VIP\n3- Single & Double VIP\n4- Correct Score VIP\n5- HT-FT VIP\n6- Jack Pot VIP\n7- Daily 10+ Odds VIP\n8- Combine VIP\n\nEnter your Choice: ")
    if user == "1":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Elite%20VIP&day=true&page=0"
    elif user == "2":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Fixed%20VIP&day=true&page=0"
    elif user == "3":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Single%2BDouble%20VIP&day=true&page=0"
    elif user == "4":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Correct%20Score%20VIP&day=true&page=0"
    elif user == "5":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=HT-FT%20VIP&day=true&page=0"
    elif user == "6":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Jack%20Pot%20VIP&day=true&page=0"
    elif user == "7":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Daily%2010%2B%20Odds%20VIP&day=true&page=0"
    elif user == "8":
        url = "https://bettingtips-api.azurewebsites.net/Mobile/WithPage?id=946012DA-2AFB-4DC8-B8CA-6895CFF361F0&cat=Combine%20VIP&day=true&page=0"
    else:
        print("Invalid Choice")
        exit()
    main(url)