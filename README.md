# Doomsday Drive
Digital Emergency Binder to be stored on a USB that contains all critical information in case shit hits the fan

## Keep your confidential files secure
In the event of an emergency, it is a smart idea to keep a thumb drive of all important documents handy.
While you should keep a physical copy of this, it is also smart to have a backup (or two) thumb drive with
the information.

Check out [this article](https://www.primalsurvivor.net/bug-out-binder/?utm_medium=social&utm_source=pinterest&utm_campaign=tailwind_smartloop&utm_content=smartloop&utm_term=6386868)
to learn more.

## Building the Executable

### Download dependencies
```angular2html
pip install -r requirements.txt
```

### MACOSX build
Run the following command on a Mac machine to build MacOSX executable
```angular2html
cd src
pyinstaller --onefile --windowed --hidden-import=Crypto.Cipher.AES --hidden-import=Crypto.Util.Padding --icon=icon.icns main.py --name RUN_ME_MACOSX
```

### WINDOWS build
Run the following command on a Windows machine to build Windows executable
```angular2html
cd src
pyinstaller --onefile --windowed --hidden-import=Crypto.Cipher.AES --hidden-import=Crypto.Util.Padding --icon=icon.icns main.py --name RUN_ME_WINDOWS
```

### LINUX build
Run the following command on a Linux machine to build MacOSX executable
```angular2html
cd src
pyinstaller --onefile --windowed --hidden-import=Crypto.Cipher.AES --hidden-import=Crypto.Util.Padding --icon=icon.icns main.py --name RUN_ME_LINUX
```

## Building the Doomsday Thumb Drive
* Pull the project code into a separate folder on your machine
* Build the executable(s) using the script(s) above
> If you can, I HIGHLY recommend you build all three for maximum cross-platform usability
* Move the executable(s) into the root folder
> The executable will be under src/dist/...
* Fill out and/or modify your custom instructions in INSTRUCTIONS.txt
* Create folder(s) for your documents and populate them with important information
* Encrypt the folder(s) that contains the sensitive documents using the executable we made before
> DO NOT FORGET YOUR PASSCODE

> Each encrypted folder will have the postfix _encrypted in the name
* Move the following NECESSARY files to your thumb drive
  * Folders that end in _encrypted
  * The RUN_ME_... executable
  * INSTRUCTIONS.txt
  * iv_index.json
* Test the decryption to make sure that the folders decrypt properly
* Safely eject your thumb drive and store away for the apocalypse
