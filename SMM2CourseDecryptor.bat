@echo off
if not "%~2"=="" (
    C:\Users\User1\AppData\Local\Programs\Python\Python37\python.exe SMM2CourseDecryptor.py %1 %2
) else (
    if not "%~1"=="" (
        C:\Users\User1\AppData\Local\Programs\Python\Python37\python.exe SMM2CourseDecryptor.py %1
    ) else (
        echo Usage: %0 ^<input^> [output]
    )
)
pause