@echo off
echo ===============================
echo Running Unit Tests...
python -m unittest discover tests -v

echo.
echo ===============================
echo Running Pytest...
pytest -v

pause