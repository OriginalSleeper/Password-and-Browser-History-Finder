BASED ON THE YICONG'S TUTORIAL : TO SEE IT [Click here](https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d) <br>
THANKS TO HIM 😀
AND LIMERBOY'S PASSWORDS STEALER (on Firefox) : TO SEE IT [Cick Here](https://github.com/LimerBoy/FireFox-Thief)

# Decrypt Chrome Passwords 🗝
This program scan your browser's files to get the browser history and the passwords saved <br>
This program works with the following browsers: **Opera, ~~Firefox~~ (actually doesn't work, because it's not based on Chromium), Brave, Edge and Chrome,** but you can add other browsers using the *Browsers* dictionary in the code (*line 142*). Just put the browser name and path to the *User Data* folder (may be called differently) <br>
This code has only been tested on windows, so it may not work on other OS.<br>
If you have an idea for improvement, do let me know!<br>

## OS support 💻
- Windows
- (Others can work if you change filepath format)

##
## Dependencies (see requirements.txt)
Install the requirements :
```pip3 install -r requirements.txt``` <br>
Or install manually :
- **sqlite** with pip : ```pip install sqlite```
- **pycryptodomex**  with pip : ```pip install pycryptodomex```
- **pywin32** with pip : ```pip install pywin32```

## Usage 📖
You can run it on the terminal :
**⚠** Depending on how you installed Python, it can be : **⚠**
```python finder.py```
```python.exe finder.py```
```python3 finder.py```

## Output 
Saved in many files like: **history<*BROWSER_NAME*>.txt** or **passwords<*BROWSER_NAME*>.txt**

## How it works ? 🤔
To understand the how this program works, read ***yicong***'s Medium article. <br>
[Click here](https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d)


## ❗ **DISCLAIMER** ❗
 DO NOT USE FOR MALICIOUS PURPOSES 

## Credits
The original password finder and decrypter was written by **LimerBoy** 👏
Browser History search and cross-browser support were added by **OriginalSleeper**... 💤


