python3 makeBuildDate.py 
:: pyinstaller --noconfirm --onefile --console --icon "d:/daten/python/photo-photography-image-picture_108525.ico"  "d:\daten\python\blendPics.py"
:: die obige Zeile macht kein icon?????
auto-py-to-exe -c compileBlendPics.json
del builddate.py
