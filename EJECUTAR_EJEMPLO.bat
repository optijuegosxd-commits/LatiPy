@echo off
cd /d "%~dp0"
echo Ejecutando el ejemplo de LatiPy...
where py >nul 2>&1
if %errorlevel%==0 (
  py latipy.py ejemplos\hola_facil.lpy
) else (
  python latipy.py ejemplos\hola_facil.lpy
)
echo.
pause
