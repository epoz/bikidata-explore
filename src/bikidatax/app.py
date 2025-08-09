from fasthtml.common import *
from monsterui.all import *
import bikidata
import os, json, traceback

app, rt = fast_app(hdrs=Theme.blue.headers())


PROPS = bikidata.query({"aggregates": ["properties"]})
PROPS = sorted(
    [
        (count, piri)
        for count, piri in PROPS.get("aggregates", {}).get("properties", [])
    ],
    reverse=True,
)

from .layout import index, raw_sql, about

from .fragments import (
    fragments_query_block,
    fragments_query,
    fragments_sql,
)

from .static import main_js
