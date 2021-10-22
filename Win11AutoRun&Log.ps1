$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue"
Start-Transcript -path log.txt -append

while (1) {
venv\Scripts\activate
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
py -m flask run
}

$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue" # or "Stop"