"""
Qumata Technical Test

Author: Byan Teo
Date: 18 January 2023
"""
import requests
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

meta = [
    {
        "name": "github_orgs",
        "description": "Retrieves GitHub organisations through GitHub REST API."
    }
]

qumata_technical_test = FastAPI(
    title="Qumata Technical Test",
    description="For GitHub REST API",
    version="1.0.0",
    openapi_tags=meta,
)

qumata_technical_test.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@qumata_technical_test.get("/github_orgs", tags=["github_orgs"])
async def github_orgs(name: str = None) -> List[str]:
    orgs = []
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    # call the rest api for organisations
    try: 
        resp = requests.get('https://api.github.com/organizations', headers=headers)
        if resp.status_code == 200:
            resp = resp.json()
        elif resp.status_code == 403:
            raise HTTPException(403, detail="Unauthorized. It might be that API access is restricted due to rate limits.")
        else:
            raise HTTPException(500, detail="Failed to call GitHub API.")
    except Exception as e:
        raise e
    
    # parse the response and add it to output
    if name is None:
        name = ""
    
    orgs.extend(parse_response(resp, name.lower()))

    # Byan: I originally assumed there was a need to fetch ALL organisations but
    # I hit the API rate limit, so I reverted to fetching only 1 page. If there
    # is a need to fetch all organisations without rate limits, the code block
    # below can be uncommented to achieve this purpose.
    '''
    while 'url' in response.links.get('next'):
        try: 
            resp = requests.get('https://api.github.com/organizations', headers=headers)
            resp = resp.json()
        except Exception as e:
            raise e

        orgs.extend(parse_response(resp))
    '''
    
    orgs = sorted(orgs, key=str.casefold)

    return {"result": orgs}


def parse_response(resp: list, filter: str = None) -> list:
    '''
    Parses response from GitHub API endpoint for organisations. Returns a
    list of names that match the provided filter, or all if filter is not
    defined.
    '''
    orgs = []

    if filter is None:
        filter == ""
    
    for org in resp:
        try:
            name = parse_org(org)
        except Exception as e:
            raise e
        
        if name is not None:
            if filter == "":
                orgs.append(name)
            elif name.lower().find(filter) != -1:
                orgs.append(name)
    
    return orgs


def parse_org(data: dict):
    '''
    Parses each organisation by retrieving the organisation URL, followed by
    organisation name. Returns name of organisation if found, else none.
    '''
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    if "url" in data:
        try:
            resp = requests.get(data["url"], headers=headers)
            if resp.status_code == 200:
                resp = resp.json()
            elif resp.status_code == 403:
                raise HTTPException(403, detail="Unauthorized. It might be that API access is restricted due to rate limits.")
            else:
                raise HTTPException(500, detail="Failed to call GitHub API.")
        except Exception as e:
            raise e

        if "name" in resp:
            return resp["name"]
        else:
            return None
    else:
        return None
