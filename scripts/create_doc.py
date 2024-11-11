import json
from apispec import APISpec
from flask_smorest import Api
from walkingpadfitbit.interfaceadapters.restapi import server

app = server.create_app()

api: Api = app.extensions["flask-smorest"]["apis"][""]["ext_obj"]
openapi_spec: APISpec = api.spec
openapi_spec_dict = openapi_spec.to_dict()
openapi_spec_json = json.dumps(openapi_spec_dict, indent=2)
print(openapi_spec_json)
