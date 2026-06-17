import uuid

from fastapi import Request


def ensure_correlation_id(request: Request, header_name: str = "X-Correlation-ID") -> str:
    correlation_id = request.headers.get(header_name) or str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    return correlation_id
