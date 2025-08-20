from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional

class DatabaseService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:25432/biometriq")
    
    def get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def execute_query(self, query: str, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class SpaceXAPIService:
    def __init__(self):
        self.base_url_v4 = "https://api.spacexdata.com/v4"
        self.base_url_v5 = "https://api.spacexdata.com/v5"
    
    async def make_request(self, method: str, url: str, **kwargs):
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, **kwargs)
                else:
                    response = await client.post(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=500, detail=f"Error fetching SpaceX data: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def format_launch_data(self, launch: Dict) -> Dict:
        launch_year = None
        if launch.get("date_utc"):
            launch_year = launch.get("date_utc")[:4]
        
        return {
            "flight_number": launch.get("flight_number"),
            "mission_name": launch.get("name"),
            "launch_year": launch_year,
            "launch_date_utc": launch.get("date_utc"),
            "launch_date_local": launch.get("date_local"),
            "launch_success": launch.get("success"),
            "upcoming": launch.get("upcoming"),
            "rocket": {
                "rocket_id": launch.get("rocket"),
                "rocket_name": "Falcon 9",
                "rocket_type": "FT"
            },
            "launch_site": {
                "site_id": launch.get("launchpad"),
                "site_name": "Launch Site",
                "site_name_long": "Launch Site"
            },
            "links": {
                "mission_patch": launch.get("links", {}).get("patch", {}).get("large"),
                "mission_patch_small": launch.get("links", {}).get("patch", {}).get("small"),
                "video_link": launch.get("links", {}).get("webcast"),
                "wikipedia": launch.get("links", {}).get("wikipedia")
            },
            "details": launch.get("details"),
            "crew": launch.get("crew", [])
        }
    
    def format_crew_data(self, crew_member: Dict) -> Dict:
        return {
            "id": crew_member.get("id"),
            "name": crew_member.get("name"),
            "agency": crew_member.get("agency"),
            "image": crew_member.get("image"),
            "status": crew_member.get("status"),
            "wikipedia": crew_member.get("wikipedia")
        }

db_service = DatabaseService()
spacex_service = SpaceXAPIService()

app = FastAPI(title="BiometrIQ SpaceX App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/launches")
async def get_launches(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    withCrew: bool = Query(False, description="Filter launches with crew members only")
):
    """
    Get SpaceX launches with pagination (5 results per page)
    """
    per_page = 5
    offset = (page - 1) * per_page
    
    query_json = {
        "options": {
            "offset": offset,
            "limit": per_page,
            "sort": {"flight_number": "desc"}
        }
    }
    
    if withCrew:
        query_json["query"] = {"crew": {"$ne": []}}
    
    response_data = await spacex_service.make_request(
        "POST", 
        f"{spacex_service.base_url_v5}/launches/query",
        json=query_json
    )
    
    launches_data = response_data.get("docs", [])
    formatted_launches = [spacex_service.format_launch_data(launch) for launch in launches_data]
    
    return {
        "launches": formatted_launches,
        "page": page,
        "per_page": per_page,
        "has_more": len(formatted_launches) == per_page
    }

@app.get("/api/crew")
async def get_crew():
    """
    Get all SpaceX crew members with essential information
    """
    crew_data = await spacex_service.make_request("GET", f"{spacex_service.base_url_v4}/crew")
    formatted_crew = [spacex_service.format_crew_data(crew_member) for crew_member in crew_data]
    
    return {
        "crew": formatted_crew,
        "total": len(formatted_crew)
    }

@app.get("/api/rockets")
async def get_rockets():
    """
    Get all rockets from database
    """
    rockets_data = db_service.execute_query("""
        SELECT id, name, type, weight, description 
        FROM rockets 
        ORDER BY name ASC
    """)
    
    formatted_rockets = [
        {
            "id": str(rocket["id"]),
            "name": rocket["name"],
            "type": rocket["type"],
            "weight": rocket["weight"],
            "description": rocket["description"]
        }
        for rocket in rockets_data
    ]
    
    return {
        "rockets": formatted_rockets,
        "total": len(formatted_rockets)
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api"):
        raise exc
    
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    
    return {"message": "Vue app not built yet. Run 'npm run build' in frontend directory."}

@app.get("/")
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Vue app not built yet. Run 'npm run build' in frontend directory."}
