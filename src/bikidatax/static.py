from fasthtml.common import FileResponse
from .app import rt


@rt
def main_js():
    return FileResponse("javascript/main.js")
