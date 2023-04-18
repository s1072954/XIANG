from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("FAKE_VALUE")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form():
    html_content = """
    <html>
        <head>
            <title>輸入表單</title>
            <link rel="stylesheet" type="text/css" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <h1>表單輸入</h1>
                <form method="post">
                    <div class="form-group">
                        <label>姓名：</label><input type="text" name="name" class="form-control"><br>
                    </div>
                    <div class="form-group">
                        <label>日期：</label><input type="date" name="date" class="form-control"><br>
                    </div>
                    <div class="form-group">
                        <label>備註：</label><input type="text" name="note" class="form-control"><br>
                    </div>
                    <input type="submit" value="送出" class="btn btn-primary">
                </form>
            </div>
        </body>
    </html>
    """
    return html_content

@app.post("/")
async def create_excel(request: Request, name: str = Form(...), date: str = Form(...), note: str = Form(...)):
    data = {'姓名': [name], '日期': [date], '備註': [note]}
    df = pd.DataFrame(data)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    response = Response(content=output.getvalue(), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers['Content-Disposition'] = 'attachment; filename=example.xlsx'
    return response
