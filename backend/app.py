from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from typing import List, Dict, Any, Optional

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
    
    async with httpx.AsyncClient() as client:
        try:
            # Build query object
            query_json = {
                "options": {
                    "offset": offset,
                    "limit": per_page,
                    "sort": {
                        "flight_number": "desc"
                    }
                }
            }
            
            # Add crew filter if requested
            if withCrew:
                query_json["query"] = {
                    "crew": {"$ne": []}
                }
            
            response = await client.post(
                "https://api.spacexdata.com/v5/launches/query",
                json=query_json
            )
            response.raise_for_status()
            response_data = response.json()
            launches_data = response_data.get("docs", [])
            
            # Filter and format the data for frontend use
            formatted_launches = []
            for launch in launches_data:
                # Extract year from date_utc
                launch_year = None
                if launch.get("date_utc"):
                    launch_year = launch.get("date_utc")[:4]
                
                formatted_launch = {
                    "flight_number": launch.get("flight_number"),
                    "mission_name": launch.get("name"),  # v5 uses "name" instead of "mission_name"
                    "launch_year": launch_year,
                    "launch_date_utc": launch.get("date_utc"),
                    "launch_date_local": launch.get("date_local"),
                    "launch_success": launch.get("success"),
                    "upcoming": launch.get("upcoming"),
                    "rocket": {
                        "rocket_id": launch.get("rocket"),  # v5 has rocket ID directly
                        "rocket_name": "Falcon 9",  # We'll need to fetch this separately or set default
                        "rocket_type": "FT"  # Default for now
                    },
                    "launch_site": {
                        "site_id": launch.get("launchpad"),  # v5 uses "launchpad"
                        "site_name": "Launch Site",  # We'll need to fetch this separately or set default
                        "site_name_long": "Launch Site"
                    },
                    "links": {
                        "mission_patch": launch.get("links", {}).get("patch", {}).get("large"),
                        "mission_patch_small": launch.get("links", {}).get("patch", {}).get("small"),
                        "video_link": launch.get("links", {}).get("webcast"),
                        "wikipedia": launch.get("links", {}).get("wikipedia")
                    },
                    "details": launch.get("details"),
                    "crew": launch.get("crew", [])  # v5 has crew as array of IDs
                }
                formatted_launches.append(formatted_launch)
            
            return {
                "launches": formatted_launches,
                "page": page,
                "per_page": per_page,
                "has_more": len(formatted_launches) == per_page
            }
            
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching SpaceX data: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/api/crew")
async def get_crew():
    """
    Get all SpaceX crew members with essential information
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.spacexdata.com/v4/crew")
            response.raise_for_status()
            crew_data = response.json()
            
            # Filter and format crew data to only include essential information
            formatted_crew = []
            for crew_member in crew_data:
                formatted_crew_member = {
                    "id": crew_member.get("id"),
                    "name": crew_member.get("name"),
                    "agency": crew_member.get("agency"),
                    "image": crew_member.get("image"),
                    "status": crew_member.get("status"),
                    "wikipedia": crew_member.get("wikipedia")
                }
                formatted_crew.append(formatted_crew_member)
            
            return {
                "crew": formatted_crew,
                "total": len(formatted_crew)
            }
            
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching crew data: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

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
