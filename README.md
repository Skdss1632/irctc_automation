
# IRCTC Tatkal python Automation !

Can book Tatkal ticket within 25 seconds..

### Features
- ✓Can book Tatkal, Premium Tatkal, and Normal Tickets.
- ✓Books tickets even if opened 2-3 minutes before Tatkal time.
- ✓Books only if confirm berths are allotted.
- ✓Supports multiple passengers.
- ✓Pre-fills all necessary information.
- ✓Automated payment via IRCTC wallet or QR Code.

## How to Make this work for you?
- Make relevant changes in file located at ``` irctc_automation/automation_project/json_config```





## follow the given steps to setup the project on your system:-

#### Just copy and paste the following command on your terminal:--

Clone the code``` git clone https://github.com/Skdss1632/irctc_automation.git``` or download the code zip files.

1. Install python using winows powershell if you are on windows

```bash
  Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.5/python-3.11.0-amd64.exe" -OutFile "$env:TEMP\python-3.10.5-amd64.exe"; Start-Process -FilePath "$env:TEMP\python-3.10.5-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

```

2. Navigate to the Project Directory
Open your terminal or PowerShell and navigate to the irctc_automation directory:

```
cd path/to/your/project/irctc_automation

```

3. Install Dependencies
Once inside the directory, run the following command to install the required dependencies:

```
pip install -r requirement.txt

```

4. install extension on chrome browser from the given link

```
https://chromewebstore.google.com/detail/adblock-%E2%80%94-block-ads-acros/gighmmpiobklfepjocnamgkkbiglidom

```


    
### Passenger_data:- do not add anything inside SEAT and FOOD

```{
 "passenger_details": [
      {
        "NAME": "python auto",
        "AGE": 44,
        "GENDER": "Male",
        "SEAT": "",
        "FOOD": ""
      }
    ],
   "passenger_phn_no": "1234567890"
}
```

### You can add multiple passenger array of objects in PASSENGER_DETAILS as an example below

```{
 "passenger_details": [
       {
        "NAME": "python auto",
        "AGE": 44,
        "GENDER": "Male",
        "SEAT": "",
        "FOOD": ""
      },
         {
        "NAME": "python auto2",
        "AGE": 45,
        "GENDER": "Male",
        "SEAT": "",
        "FOOD": ""
      },
         {
        "NAME": "python auto3",
        "AGE": 46,
        "GENDER": "Male",
        "SEAT": "",
        "FOOD": ""
      },
         {
        "NAME": "python auto4",
        "AGE": 47,
        "GENDER": "Male",
        "SEAT": "",
        "FOOD": ""
      }
    ],
   "passenger_phn_no": "1234567890"
}
```
### Note

- At a time either Tatkal Or Premium Tatkal can be -> true <- not both and general should be -> false.

- set the zoom level to 80% of your chrome browser if you are using it on windows

- currently auto captcha fill is disabled bcz it takes upto 10 to 20 seconds sometimes so fill the captcha manually

- after filli ng captcha hit enter key from the keyboard always
