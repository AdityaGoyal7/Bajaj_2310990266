from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import math
from functools import reduce
import typing

APP_EMAIL = os.getenv("OFFICIAL_EMAIL", "aditya0266.be23@chitkara.edu.in")

app = FastAPI(title="BFHL API", version="1.0")

# Allow public access (for deployment) but keep this minimal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.sqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def hcf_list(nums: typing.List[int]) -> int:
    return reduce(gcd, nums)


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def lcm_list(nums: typing.List[int]) -> int:
    return reduce(lcm, nums, 1)


def fibonacci(n: int) -> typing.List[int]:
    if n <= 0:
        return []
    seq = [0]
    if n == 1:
        return seq
    seq.append(1)
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"is_success": False, "official_email": APP_EMAIL, "error": "internal_server_error"},
    )


@app.get("/health")
async def health():
    return {"is_success": True, "official_email": APP_EMAIL}


@app.post("/bfhl")
async def bfhl(payload: dict):
    # Strict: exactly one top-level key
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "invalid_json"})

    keys = [k for k in payload.keys()]
    allowed = {"fibonacci", "prime", "lcm", "hcf"}
    if len(keys) != 1:
        raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "request_must_contain_exactly_one_key"})
    key = keys[0]
    if key not in allowed:
        raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "invalid_key"})

    try:
        if key == "fibonacci":
            n = payload["fibonacci"]
            if not isinstance(n, int):
                raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "fibonacci_must_be_integer"})
            if n < 0 or n > 1000:
                raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "fibonacci_out_of_bounds"})
            data = fibonacci(n)

        elif key == "prime":
            arr = payload["prime"]
            if not isinstance(arr, list) or not all(isinstance(x, int) for x in arr):
                raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "prime_must_be_integer_array"})
            data = [x for x in arr if is_prime(x)]

        elif key == "lcm":
            arr = payload["lcm"]
            if not isinstance(arr, list) or not arr or not all(isinstance(x, int) for x in arr):
                raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "lcm_must_be_nonempty_integer_array"})
            data = lcm_list(arr)

        elif key == "hcf":
            arr = payload["hcf"]
            if not isinstance(arr, list) or not arr or not all(isinstance(x, int) for x in arr):
                raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "hcf_must_be_nonempty_integer_array"})
            data = hcf_list(arr)

        # AI integration removed: external AI calls are not available in this build.
        else:
            raise HTTPException(status_code=400, detail={"is_success": False, "official_email": APP_EMAIL, "error": "unsupported_operation"})

        return {"is_success": True, "official_email": APP_EMAIL, "data": data}

    except HTTPException as he:
        # If detail is already the standardized dict, return it as response body with correct status
        detail = he.detail
        if isinstance(detail, dict) and detail.get("is_success") is False:
            return JSONResponse(status_code=he.status_code, content=detail)
        raise
