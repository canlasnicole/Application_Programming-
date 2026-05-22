"""
======================================================
 FastAPI 강의: Request & Response 완전판
======================================================

강의 순서
─────────────────────────────────────────────────────
 1부. Response 기초       — dict 반환, 상태코드, 커스텀 헤더
 2부. Response 타입       — JSONResponse, HTMLResponse, FileResponse
 3부. RedirectResponse    — GET→GET, POST→GET 리다이렉트
 4부. Request 객체        — 메타정보, 경로/쿼리 파라미터
 5부. Request Body 처리   — Raw bytes, 헤더+Body 종합
 6부. 입출력 모델 분리    — response_model, Form() 타입힌트
======================================================
"""

from fastapi import FastAPI, Form, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# ======================================================
# 1부. Response 기초
# ======================================================
# FastAPI는 딕셔너리를 반환하면 자동으로 JSONResponse(200 OK)로 감쌉니다.
# 상태코드나 헤더를 바꾸고 싶을 때는 Response 객체를 매개변수로 받아 직접 제어합니다.
# ── 1-0. 가장 기본: Request 객체 사용 ───────────────────────

@app.get("/request-info-intro/")
async def get_request_info(request: Request): # 👈 Request 객체를 주입받음
    """
    들어온 HTTP 요청의 다양한 정보를 반환하는 엔드포인트입니다.
    """
    # 1. 클라이언트 정보 가져오기 (IP 주소)
    client_host = request.client.host if request.client else "Unknown"
    
    # 2. 요청 메소드와 전체 URL 가져오기
    method = request.method
    full_url = str(request.url)
    
    # 3. 특정 헤더 값 가져오기 (예: User-Agent)
    user_agent = request.headers.get("user-agent", "N/A")
    
    # 4. 쿼리 매개변수 직접 접근
    # 'q'라는 쿼리 매개변수가 있다면 가져오고, 없으면 None
    custom_query = request.query_params.get("custom_q")
    
    return {
        "client_host": client_host,
        "http_method": method,
        "request_url": full_url,
        "user_agent": user_agent,
        "custom_query_param": custom_query,
        "message": "Request 객체를 통해 요청의 세부 정보에 접근했습니다."
    }
    
@app.get("/response-info-intro/")
async def get_response_info(response: Response): # 👈 Response 객체를 주입받음
    """
    클라이언트에게 보낼 HTTP 응답(Response)의 다양한 정보를 
    직접 설정하고, 그 변경 사항을 확인하여 반환하는 엔드포인트입니다.
    """
    # 1. HTTP 상태 코드(Status Code) 직접 변경하기
    # 기본값은 200 OK이지만, 임의로 202 Accepted로 변경합니다.
    response.status_code = status.HTTP_202_ACCEPTED
    
    # 2. 커스텀 헤더(Custom Header) 추가하기
    # 헤더 이름은 대소문자를 구분하지 않는 것이 일반적입니다.
    response.headers["X-Custom-Server-Version"] = "FastAPI-v1.0"
    response.headers["X-Processed-By"] = "MLOps-Pipeline"
    
    # 3. 쿠키(Cookie) 설정하기
    # 클라이언트 브라우저에 저장될 쿠키를 심어줍니다. (만료 시간 3600초)
    response.set_cookie(
        key="user_session_token", 
        value="abc123xyz789", 
        max_age=3600, 
        httponly=True
    )
    
    # 4. 설정한 응답 정보들을 딕셔너리로 취합하여 반환 (확인용)
    # 실제 클라이언트에게는 이 JSON 데이터와 함께 위에서 설정한 상태코드, 헤더, 쿠키가 전달됩니다.
    return {
        "modified_status_code": response.status_code,
        "applied_headers": {
            "X-Custom-Server-Version": response.headers.get("x-custom-server-version"),
            "X-Processed-By": response.headers.get("x-processed-by"),
            "Content-Type": response.headers.get("content-type") # FastAPI가 자동 생성하는 헤더
        },
        "set_cookie_info": {
            "key": "user_session_token",
            "value": "abc123xyz789",
            "note": "HttpOnly 쿠키가 응답 헤더(Set-Cookie)에 포함되었습니다."
        },
        "message": "Response 객체를 통해 상태 코드, 헤더, 쿠키를 성공적으로 조작했습니다."
    }

# ── 1-1. 가장 기본: 딕셔너리 반환 ───────────────────────
# FastAPI가 자동으로 200 OK + Content-Type: application/json 설정
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI World"}

# ── 1-2. Response 객체로 상태코드 & 커스텀 헤더 제어 ────
# Response를 매개변수로 받으면 헤더/쿠키를 직접 설정할 수 있습니다.
# 반환값(딕셔너리)은 FastAPI가 여전히 JSON으로 변환합니다.
@app.get("/custom-response", status_code=status.HTTP_201_CREATED)
def custom_response(response: Response):
    # response.headers["X-Custom-Header"] = "This is a custom header"
    return {"status": "success"}

# ======================================================
# 2부. Response 타입
# ======================================================
# response_class: OpenAPI(Swagger) 문서에 반환 타입을 명시하는 역할도 합니다.
# 직접 Response 객체를 생성하면 status_code·헤더를 세밀하게 제어할 수 있습니다.

# ── 2-1. JSONResponse 명시적 반환 ────────────────────────
# 기본값이 JSONResponse이므로 생략 가능하지만, 명시하면 의도가 명확해집니다.
@app.get("/resp-json/{item_id}", response_class=JSONResponse)
async def response_json(item_id: int, q: str | None = None):
    return JSONResponse(
        content={"item_id": item_id, "q": q},
        status_code=status.HTTP_200_OK
    )

# ── 2-2. HTMLResponse ────────────────────────────────────
# response_class=HTMLResponse 로 선언하면 Swagger 문서에도 HTML 반환으로 표시됩니다.
@app.get("/resp-html/{item_id}", response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None):
    html_str = f"""
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    """
    return HTMLResponse(html_str, status_code=status.HTTP_200_OK)

# ── 2-3. FileResponse (바이너리/파일 반환) ───────────────
# Content-Disposition 등 파일 관련 헤더를 자동으로 설정합니다.
@app.get("/image")
def get_image():
    return FileResponse(path="parrot.jpg", media_type="image/jpeg", filename="parrot.jpg")

# ======================================================
# 3부. RedirectResponse
# ======================================================
# 307 Temporary Redirect : 기본값. 원래 HTTP 메서드(POST 등)를 유지합니다.
# 302 Found              : POST → GET 전환 시 반드시 명시해야 합니다.
#                          302 없이 307이면 브라우저가 POST를 유지해 오류 발생!

# ── 3-1. GET → GET 리다이렉트 (기본 307) ─────────────────
@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect: {comment}")
    return RedirectResponse(url=f"/resp-html/3?item_name={comment}")


# ── 3-2. POST → GET 리다이렉트 (302 필수) ────────────────
# Form() 타입힌트: Content-Type이 form인 요청 본문에서 필드를 자동 추출합니다.
# int, str 등 타입이 맞지 않으면 FastAPI가 422 Unprocessable Entity를 자동 반환합니다.
@app.post("/create-redirect")
async def create_redirect(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id: {item_id}, item_name: {item_name}")
    return RedirectResponse(
        url=f"/resp-html/{item_id}?item_name={item_name}",
        status_code=status.HTTP_302_FOUND   # ← POST→GET 전환의 핵심
    )

# ======================================================
# 4부. Request 객체로 요청 정보 읽기
# ======================================================
# Request 객체는 매개변수에 타입 힌트만 지정하면 FastAPI가 자동으로 주입합니다.
# 클라이언트 IP, 메서드, URL, 헤더, 쿼리/경로 파라미터에 접근할 수 있습니다.

# ── 4-1. 기본 요청 메타정보 읽기 ─────────────────────────
@app.get("/request-info/")
async def get_request_info(request: Request):
    return {
        "client_host":        request.client.host if request.client else "Unknown",
        "http_method":        request.method,
        "request_url":        str(request.url),
        "user_agent":         request.headers.get("user-agent", "N/A"),
        # ?custom_q=값 형태로 전달된 쿼리 파라미터를 직접 꺼냅니다.
        "custom_query_param": request.query_params.get("custom_q"),
    }

# ── 4-2. 경로 파라미터 + 요청 메타정보 함께 읽기 ─────────
# 경로 파라미터가 있어도 Request 객체를 함께 사용할 수 있습니다.
@app.get("/items/{item_group}")
async def read_item_with_path_param(request: Request, item_group: str):
    return {
        "client_host":  request.client.host if request.client else "N/A",
        "http_method":  request.method,
        "url":          str(request.url),
        "path_params":  request.path_params,        # {"item_group": "..."}
        "query_params": dict(request.query_params),
        "user_agent":   request.headers.get("user-agent", "N/A"),
    }

# ======================================================
# 5부. Request 객체로 Body 처리하기
# ======================================================
# request.body()는 비동기(await) 함수이며 요청 본문을 bytes로 반환합니다.
# Pydantic 모델 없이 Raw 바이트를 직접 다룰 때 사용합니다.

# ── 5-1. Raw Body 읽기 ────────────────────────────────────
@app.post("/request-raw-body/")
async def process_raw_body(request: Request):
    try:
        raw_body: bytes = await request.body()
    except Exception as e:
        return {"error": f"Failed to read body: {e}"}

    return {
        "received_data_type":      "Raw Bytes",
        "body_length_bytes":       len(raw_body),
        # bytes → 문자열 변환 (비UTF-8 문자는 무시)
        "decoded_content_preview": raw_body.decode("utf-8", errors="ignore")[:100],
    }

# ── 5-2. 헤더 + Body 종합 처리 ───────────────────────────
# 실전 패턴: 클라이언트 정보·헤더·본문을 한 번에 분석합니다.
@app.post("/request-process/")
async def process_full_request(request: Request):
    try:
        raw_body: bytes = await request.body()
    except Exception:
        raw_body = b""  # 본문이 없거나 실패 시 빈 bytes 처리

    return {
        "status": "success",
        "client_info": {
            "ip":     request.client.host if request.client else "N/A",
            "method": request.method,
            "url":    str(request.url),
        },
        "request_data": {
            # Content-Type: 클라이언트가 보낸 데이터 형식
            # (application/json, multipart/form-data 등)
            "content_type":    request.headers.get("content-type", "N/A"),
            "user_agent":      request.headers.get("user-agent", "N/A"),
            "body_length":     len(raw_body),
            "body_preview":    raw_body.decode("utf-8", errors="ignore")[:100],
        },
    }

# ======================================================
# 6부. 입출력 모델 분리 & Form() 타입힌트
# ======================================================

# ── 6-1. Pydantic 모델로 JSON Body 자동 파싱 ─────────────
# FastAPI가 Content-Type: application/json 본문을 Item 모델로 자동 역직렬화합니다.
# 유효성 검사 실패 시 422 Unprocessable Entity를 자동으로 반환합니다.
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None    # 선택 필드

# ── 6-2. 입력(Item) / 출력(ItemResp) 모델 분리 ───────────
# response_model: 반환 전 이 모델로 필터링 → 불필요하거나 민감한 필드 노출 방지
# 예) 내부 계산값(price_with_tax)만 노출하고 tax 원본은 숨깁니다.
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

@app.post(
    "/create-item/",
    response_model=ItemResp,                    # 반환 필드를 ItemResp로 제한
    status_code=status.HTTP_201_CREATED         # 생성 성공은 200이 아닌 201
)
async def create_item_model(item: Item):
    price_with_tax = item.price + (item.tax or 0)

    return ItemResp(
        name=item.name,
        description=item.description,
        price_with_tax=price_with_tax,
    )

# ── 6-3. Form() 타입힌트 vs request.form() Raw 처리 비교 ──
#
# [request.form() — 5부 방식]
#   유효성 검사 없음, 뭐가 들어와도 그냥 처리
#   → 자유도 높지만 타입 오류를 개발자가 직접 처리해야 함
#
# [Form() 타입힌트 — 이 방식]
#   타입이 맞지 않으면 FastAPI가 422를 자동 반환
#   Swagger UI에서 form 필드로 자동 문서화
@app.post("/items-form/")
async def create_item_form(
    item_id:   int = Form(),    # int가 아니면 422 자동 반환
    item_name: str = Form(),
):
    print(f"item_id: {item_id}, item_name: {item_name}")
    return {"item_id": item_id, "item_name": item_name}
