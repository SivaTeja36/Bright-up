from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from app.routes.route_entries import PROTECTED_ROUTES, PUBLIC_ROUTES
from app.utils.auth_dependencies import verify_auth_token
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask
import httpx
from starlette.requests import Request

security = HTTPBearer()


def setup_routes(app: FastAPI):
    for route in PUBLIC_ROUTES:
        app.include_router(route)

    for route in PROTECTED_ROUTES:
        dependcies = [Depends(security), Depends(verify_auth_token)]
        app.include_router(route, dependencies=dependcies)

    # adding proxy routing tonotification V1.
    app.add_route(
        "/api/v1/{path:path}", _reverse_proxy, ["GET", "POST", "PUT", "DELETE"]
    )


client = httpx.AsyncClient(base_url="http://host.docker.internal:8001")


async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(
        request.method, url, headers=request.headers.raw, content=request.stream()
    )
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )
