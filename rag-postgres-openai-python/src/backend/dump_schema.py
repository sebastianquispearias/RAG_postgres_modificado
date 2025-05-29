import json
from fastapi_app.api_models import ChatRequest

schema = ChatRequest.schema()
print(json.dumps(schema, indent=2))
