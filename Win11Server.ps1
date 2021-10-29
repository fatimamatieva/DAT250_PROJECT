$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue"
Start-Transcript -path log.txt -append

while (1) {
venv\Scripts\activate
py -m waitress --listen=*:5000 --url-scheme=https 'wsgi:app'
}

$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue" # or "Stop"