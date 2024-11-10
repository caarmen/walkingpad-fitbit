import json
from walkingpadfitbit.interfaceadapters.restapi import server

app = server.create_app()

with app.app_context():
    openapi_spec = app.swag.get_apispecs("apispec_1")

openapi_spec_json = json.dumps(openapi_spec, indent=2)
print(openapi_spec_json)
