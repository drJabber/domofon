from typing import Sequence, Dict
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

class AllowedPathsMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        patterns: Dict[str, Sequence[str]]
    ) -> None:
        self.app = app
        self.patterns = patterns

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        host = scope["client"][0]

        valid_host_for_path = True
        for pattern, allowed_hosts in self.patterns.items():
            if (path == pattern or pattern.endswith('*') and path.startswith(pattern[:-1])) and \
              not (host in allowed_hosts or '*' in allowed_hosts):
                valid = False
                for h in allowed_hosts:
                    if h.endswith('*') and host.startswith(h[:-1]):
                        valid = True
                        break
                valid_host_for_path = valid
                if not valid:
                    break
        
        if valid_host_for_path:
            await self.app(scope, receive, send)    
        else:
            response = JSONResponse(content={"errors": [f"Host {host} does not allowed"]}, status_code=HTTP_400_BAD_REQUEST)  
            await response(scope, receive, send)  

