# Mark
Easy-to-use bulk image watermarking tool

# Using the Windows executable
- Download `mark-windows-latest.zip` from the latest [release](https://github.com/CristianEduardMihai/Mark/releases)
- Unzip the archive, make sure to keep all its items in one folder
- Replace `watermark.png` with your transparent watermark
- Edit `config.json` as per your needs
- Run `mark-windows-latest.exe`, ignore the Windows unsigned warning
- Select the photos you want to watermark and click on `Open`. Once the process finishes, you will find a `watermarked` subfolder to your original photo location

*The executable is built publicly via [GitHub actions](https://github.com/CristianEduardMihai/Mark/actions). The only reason you may get a security warning is because it is not signed by any known developer

# Using Python directly
Any Python release from 3.8 to 3.12 should work

Use this if you are on Linux.

- Clone the repo
```
git clone https://github.com/CristianEduardMihai/Mark
```
- Install requirements
```
pip install -r requirements.txt
```
- Replace `watermark.png` with your transparent watermark
- Edit `config.json` as per your needs

- Run
```
python3 main.py
```