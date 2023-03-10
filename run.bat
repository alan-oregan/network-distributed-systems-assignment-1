// https://stackoverflow.com/a/51319981
cd server
start "dis-sys-server" python server.py
cd ../client
start "dis-sys-client" python client.py
pause
taskkill /FI "WindowTitle eq dis-sys-server*" /T /F
taskkill /FI "WindowTitle eq dis-sys-client*" /T /F
