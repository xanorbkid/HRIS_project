@echo off
setlocal enabledelayedexpansion

@REM echo [94mStarting database seeding process...[0m

:: Activate virtual environment
@REM echo.
@REM echo [94mActivating virtual environment...[0m
@REM call myenv\Scripts\activate

:: Navigate to project directory
@REM cd HRIS

:: Flush the database to start fresh
echo.
echo [94mFlushing the database...[0m
python manage.py flush --noinput

:: Load fixtures in order
echo.
echo [94mLoading Auth fixtures...[0m
python manage.py loaddata seeders/auth/01_groups.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/auth/02_users.json
if errorlevel 1 goto :error
echo [92m✓ Auth fixtures loaded successfully[0m

echo.
echo [94mLoading Employee fixtures...[0m
python manage.py loaddata seeders/employee/01_departments.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/employee/02_job_titles.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/employee/03_employee_profiles.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/employee/04_emergency_contacts.json
if errorlevel 1 goto :error
echo [92m✓ Employee fixtures loaded successfully[0m

echo.
echo [94mLoading Time-off Management fixtures...[0m
python manage.py loaddata seeders/time_off_management/01_leave_types.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/time_off_management/02_shifts.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/time_off_management/03_leave_allocations.json
if errorlevel 1 goto :error
python manage.py loaddata seeders/time_off_management/04_leave_requests.json
if errorlevel 1 goto :error
echo [92m✓ Time-off Management fixtures loaded successfully[0m

echo.
echo [92mDatabase seeding completed successfully![0m
echo.
echo [94mTest Credentials:[0m
echo SuperAdmin: admin / Pass@123
echo HR Admin: sarah.hr / Pass@123
echo Manager: john.manager / Pass@123
echo Employee: mary.dev / Pass@123
echo Dept Head: robert.head / Pass@123

goto :end

:error
echo.
echo [91m✗ Error: Fixture loading failed[0m
exit /b 1

:end
endlocal