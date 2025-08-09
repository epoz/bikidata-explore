from fasthtml.common import *
from monsterui.all import *
from .app import rt, PROPS
import os
from .fragments import query_block
from .static import main_js


def bx_navbar():
    return Div(
        Container(
            NavBar(
                A("Home", href=index),
                A("SQL", href=raw_sql),
                A("About", href=about),
                brand=DivLAligned(
                    UkIcon("mountain-snow", height=30, width=30),
                    A(H3("bikiDATA Explorer", cls="text-stone-400"), href=index),
                ),
            )
        ),
        cls="bg-green-800 text-white",
    )


def main_container(content, extra_script=None):
    return (
        Title("Bikidata Explorer"),
        extra_script,
        Div(bx_navbar(), Container(content)),
    )


@rt
def index():
    aggregates_chooser = DivHStacked(
        Div(
            Button(
                "-",
                style="padding: 0.2ch; border: 1px solid #ccc; border-radius: 8px;",
                cls="agg_remove btn-sm",
            ),
            Button(
                "+",
                style="padding: 0.2ch; border: 1px solid #ccc; border-radius: 8px;",
                cls="agg_add btn-sm",
            ),
        ),
        Select(
            Option(" - ", value="-"),
            *[Option(p, value=p) for c, p in PROPS],
            cls="agg",
            style="margin: 1ch; padding: 0.5ch;",
        ),
        style="margin: 0.1ch;",
    )

    return main_container(
        Div(
            H4("Filters"),
            query_block(),
            H4("Aggregates"),
            aggregates_chooser,
            H4("Exclude properties"),
            Div(
                Input(
                    type="text",
                    id="excludes",
                    placeholder="<http://schema.org/dataFeedElement>",
                    style="width: 30vw",
                )
            ),
            Div(
                Button(
                    "Go",
                    id="go",
                    cls=(ButtonT.primary, "mt-4"),
                    # style="background-color: #999; color: white; border-radius: 8px; padding: 4px",
                ),
                Div(id="results"),
                cls="mt-2",
            ),
        ),
        extra_script=Script(src=main_js),
    )


@rt
def raw_sql():
    return main_container(
        Div(
            H1("SQL Queries"),
            Textarea(
                "SELECT * FROM iris LIMIT 10",
                cls="uk-textarea",
                rows=10,
                id="sql_query",
            ),
            Button("Run SQL", id="run_sql", cls=(ButtonT.primary, "mt-4")),
            Div(id="sql_results"),
            Script(
                """
document.getElementById("run_sql").addEventListener("click", function (event) {
    event.preventDefault();
    const sqlQuery = document.getElementById("sql_query").value;
    fetch("/fragments_sql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: sqlQuery })
    })
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("sql_results").innerHTML = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
})    

"""
            ),
        )
    )


@rt
def about():
    BIKIDATA_DB = os.environ.get("BIKIDATA_DB")

    return main_container(
        Div(
            H1("About"),
            P(f"Your bikidata database is at: ", cls="mt-2"),
            P(BIKIDATA_DB, cls=TextT.xl),
        )
    )
