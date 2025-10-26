#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting database seeding process...${NC}"

# Activate virtual environment
echo -e "\n${BLUE}Activating virtual environment...${NC}"
source myenv/Scripts/activate

# Navigate to project directory
cd HRIS

# Flush the database to start fresh
echo -e "\n${BLUE}Flushing the database...${NC}"
python manage.py flush --noinput

# Load fixtures in order
echo -e "\n${BLUE}Loading Auth fixtures...${NC}"
python manage.py loaddata seeders/auth/01_groups.json && \
python manage.py loaddata seeders/auth/02_users.json

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Auth fixtures loaded successfully${NC}"
else
    echo -e "${RED}✗ Failed to load Auth fixtures${NC}"
    exit 1
fi

echo -e "\n${BLUE}Loading Employee fixtures...${NC}"
python manage.py loaddata seeders/employee/01_departments.json && \
python manage.py loaddata seeders/employee/02_job_titles.json && \
python manage.py loaddata seeders/employee/03_employee_profiles.json && \
python manage.py loaddata seeders/employee/04_emergency_contacts.json

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Employee fixtures loaded successfully${NC}"
else
    echo -e "${RED}✗ Failed to load Employee fixtures${NC}"
    exit 1
fi

echo -e "\n${BLUE}Loading Time-off Management fixtures...${NC}"
python manage.py loaddata seeders/time_off_management/01_leave_types.json && \
python manage.py loaddata seeders/time_off_management/02_shifts.json && \
python manage.py loaddata seeders/time_off_management/03_leave_allocations.json && \
python manage.py loaddata seeders/time_off_management/04_leave_requests.json

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Time-off Management fixtures loaded successfully${NC}"
else
    echo -e "${RED}✗ Failed to load Time-off Management fixtures${NC}"
    exit 1
fi

echo -e "\n${GREEN}Database seeding completed successfully!${NC}"
echo -e "\n${BLUE}Test Credentials:${NC}"
echo -e "SuperAdmin: admin / Pass@123"
echo -e "HR Admin: sarah.hr / Pass@123"
echo -e "Manager: john.manager / Pass@123"
echo -e "Employee: mary.dev / Pass@123"
echo -e "Dept Head: robert.head / Pass@123"