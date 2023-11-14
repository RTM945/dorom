for /f "tokens=* delims= " %%a in ('dir /s/b/a-d "*.png"') do (
identify "%%a"
convert "%%a" -strip "%%a"
identify "%%a")