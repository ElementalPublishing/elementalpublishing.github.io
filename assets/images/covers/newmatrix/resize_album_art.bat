@echo off
echo Album Art Batch Resizer
echo ====================

REM Check if ImageMagick is installed
magick -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: ImageMagick not found! 
    echo Please install ImageMagick from: https://imagemagick.org/script/download.php#windows
    pause
    exit /b 1
)

REM Check if file was provided
if "%~1"=="" (
    echo Usage: Drag and drop an image file onto this batch file
    echo OR: resize_album_art.bat "image_file.png"
    pause
    exit /b 1
)

set input=%1
set basename=%~n1
echo Processing: %basename%

REM Create folders
echo Creating folders...
mkdir "3000x3000" 2>nul
mkdir "2000x2000" 2>nul
mkdir "1400x1400" 2>nul
mkdir "1000x1000" 2>nul
mkdir "800x800" 2>nul
mkdir "640x640" 2>nul
mkdir "600x600" 2>nul
mkdir "500x500" 2>nul
mkdir "400x400" 2>nul
mkdir "300x300" 2>nul
mkdir "200x200" 2>nul
mkdir "150x150" 2>nul
mkdir "100x100" 2>nul

REM Resize images
echo Resizing images...
magick "%input%" -resize 3000x3000 "3000x3000/%basename%_3000x3000.jpg"
magick "%input%" -resize 2000x2000 "2000x2000/%basename%_2000x2000.jpg"
magick "%input%" -resize 1400x1400 "1400x1400/%basename%_1400x1400.jpg"
magick "%input%" -resize 1000x1000 "1000x1000/%basename%_1000x1000.jpg"
magick "%input%" -resize 800x800 "800x800/%basename%_800x800.jpg"
magick "%input%" -resize 640x640 "640x640/%basename%_640x640.jpg"
magick "%input%" -resize 600x600 "600x600/%basename%_600x600.jpg"
magick "%input%" -resize 500x500 "500x500/%basename%_500x500.jpg"
magick "%input%" -resize 400x400 "400x400/%basename%_400x400.jpg"
magick "%input%" -resize 300x300 "300x300/%basename%_300x300.jpg"
magick "%input%" -resize 200x200 "200x200/%basename%_200x200.jpg"
magick "%input%" -resize 150x150 "150x150/%basename%_150x150.jpg"
magick "%input%" -resize 100x100 "100x100/%basename%_100x100.jpg"

echo Done! All sizes created.
echo Check the folders: 3000x3000, 2000x2000, etc.
pause