from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data import recommend_books_by_genres  # Import recommendation function

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    print(templates)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
async def submit_form(request: Request, genres: str = Form(...)):
    # Process form submission and get recommendations
    recommendations = recommend_books_by_genres(genres.split(','))
    print(recommendations)

    return templates.TemplateResponse("results.html", {"request": request, "recommendations": recommendations})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
