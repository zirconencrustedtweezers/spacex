#!/usr/bin/env python3
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
import httpx

DATABASE_URL = "postgresql://admin:password@localhost:25432/biometriq"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

async def fetch_rockets_batch(page=1, limit=100):
    url = "https://api.spacexdata.com/v4/rockets/query"
    query = {
        "options": {
            "page": page,
            "limit": limit,
            "sort": {"first_flight": "asc"}
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=query)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None

def map_rocket_data(api_rocket):
    mass = api_rocket.get("mass", {})
    weight = mass.get("kg") if mass else None
    
    return {
        'name': api_rocket.get("name") or "Unknown",
        'type': api_rocket.get("type") or "Unknown",
        'weight': weight,
        'description': api_rocket.get("description")
    }

def save_rockets_batch(conn, rockets):
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM rockets")
    existing_names = {row[0] for row in cursor.fetchall()}
    
    new_rockets = [r for r in rockets if r['name'] not in existing_names]
    
    if not new_rockets:
        return 0
    
    try:
        cursor.executemany("""
            INSERT INTO rockets (name, type, weight, description)
            VALUES (%(name)s, %(type)s, %(weight)s, %(description)s)
        """, new_rockets)
        conn.commit()
        return len(new_rockets)
    except psycopg2.Error:
        conn.rollback()
        return 0

async def fetch_all_rockets():
    conn = get_db_connection()
    total_saved = 0
    page = 1
    batch_size = 100
    
    try:
        while True:
            api_response = await fetch_rockets_batch(page=page, limit=batch_size)
            if not api_response:
                break
            
            rockets_data = api_response.get("docs", [])
            has_next_page = api_response.get("hasNextPage", False)
            
            if not rockets_data:
                break
            
            rockets = []
            for api_rocket in rockets_data:
                try:
                    rocket = map_rocket_data(api_rocket)
                    rockets.append(rocket)
                except Exception:
                    continue
            
            saved_count = save_rockets_batch(conn, rockets)
            total_saved += saved_count
            
            if not has_next_page or len(rockets_data) < batch_size:
                break
            
            page += 1
        
        print(f"Saved {total_saved} rockets")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import asyncio
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)
    
    asyncio.run(fetch_all_rockets())
