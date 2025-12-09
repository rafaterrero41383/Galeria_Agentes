from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
import shutil

app = FastAPI()

# Carpeta donde guardar archivos temporales
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# ============================
#   SUBIDA DE ARCHIVOS
# ============================
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    saved_path = f"{TEMP_DIR}/{file_id}_{file.filename}"

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_id": file_id, "filename": file.filename, "path": saved_path}


# ============================
#   GENERAR ZIP DEL AGENTE
# ============================
@app.post("/api/generate/{agent}")
async def generate_project(agent: str, file_id: str):
    """
    agent = mule | apigee | java | raml | dtm
    file_id = id retornado por /upload
    """
    # Aquí va la integración REAL con tu generador.
    # De momento generamos un ZIP vacío para probar.
    zip_id = str(uuid.uuid4())
    zip_path = f"{TEMP_DIR}/{zip_id}.zip"

    # Crear archivo ZIP ficticio
    with open(zip_path, "wb") as zip_file:
        zip_file.write(b"ZIP DE PRUEBA DEL AGENTE: " + agent.encode())

    return {"zip_id": zip_id, "download_url": f"/api/download/{zip_id}"}


# ============================
#   DESCARGA DEL ZIP
# ============================
@app.get("/api/download/{zip_id}")
async def download(zip_id: str):
    zip_path = f"{TEMP_DIR}/{zip_id}.zip"

    if not os.path.exists(zip_path):
        return JSONResponse({"error": "Archivo no encontrado"}, status_code=404)

    return FileResponse(zip_path, filename=f"{zip_id}.zip", media_type="application/zip")
