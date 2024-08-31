# Getting Started with Backend

## Local Setup

cd backend
psql -d real_estate_db -f init_db.sql 
python3 -m venv .venv
source .venv/bin/activate

## Running frontend

cd real-estate-frontend
npm install
npm run start


## Running scraper
cd backend
python3 scheduler.py