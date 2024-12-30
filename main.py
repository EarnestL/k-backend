from fastapi import FastAPI
from routes import album, search, photocards
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000", "http://localhost:3000", "https://k-atalog.vercel.app"],  # Replace with your domains
    allow_credentials=True,  # Enable cookies or authentication headers if needed
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Authorization, Content-Type)
)

# Register routes
app.include_router(album.router, prefix="/album", tags=["Albums"])
app.include_router(search.router, prefix="/search", tags=["Search General"])
app.include_router(photocards.router, prefix="/photocards", tags=["SPhotocards"])

@app.get("/")
def read_root():
    return {"message": "k-backend"}
