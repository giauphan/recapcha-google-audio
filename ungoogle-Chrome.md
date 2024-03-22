You need to create a /usr/share/applications/chromium.desktop file with the location of the portable executable, eg:
```
[Desktop Entry]
Type=Application
Name=Ungoogled Chromium
Exec=/usr/local/ungoogled-chromium_122.0.6261.69-1_linux/chrome
Comment=Chrome without the spyware
Categories=WebBrowser
````
Then run the script using an X wrapper, eg
xvfb-run -a python3 script.py
