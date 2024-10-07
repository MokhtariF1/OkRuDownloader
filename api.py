from fastapi import FastAPI
import helper
import json


app = FastAPI()


@app.post("/download")
async def download(url: str, quality: str):
    response = await helper.download(url, quality)
    print(response)
    status = response
    if status == 400:
        response_json = {
            "status": 400,
            "message": "quality error!",
        }
        return json.dumps(response_json)
    elif status == 200:
        response_json = {
            "status": 200,
            "message": "video downloaded!",
            "path": response["path"],
        }
        return json.dumps(response_json)
    else:
        response_json = {
            "status": 500,
            "message": "error in download!",
        }
        return json.dumps(response_json)