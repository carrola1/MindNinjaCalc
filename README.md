# MonsterCalc
## Using with Linux
To create a shortcut launcher with Ubuntu Jammy Jellyfish create a file called MonsterCalc.desktop in /usr/share/applications directory. Enter the following text into the newly created file.

[Desktop Entry]
Type=Application
Terminal=false
Name=MonsterCalc
Icon=[MonsterCalc Directory]/Monster.png
Exec=python3 [MonsterCalc Directory]/MonsterCalc.py -platform wayland

MonsterCalc will now showup in the quick launcher.
