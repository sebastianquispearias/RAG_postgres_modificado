import json
from fastapi_app.api_models import ChatRequest

print(json.dumps(ChatRequest.schema(), indent=2))
