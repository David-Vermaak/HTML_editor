# Live HTML Editor
This is a Live HTML Editor written in Python 

I am using the sun valley ttk theme from https://github.com/rdbende/Sun-Valley-ttk-theme

Feel free to use this project to build nice looking python programs!

## Compiling the .exe

make sure that pyinstaller is installed:

```bash
pip install pyinstaller
```

Then run this command in the termainal (within the project folder)
Make sure that the path of the sv_ttk dependency is correct. (replace USERNAME)

```bash
pyinstaller -w -F -i "email.ico" --add-data "C:\Users\USERNAME\Desktop\HTML_editor\sv_ttk;sv_ttk" main.py
```

