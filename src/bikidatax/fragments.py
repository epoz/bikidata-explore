from fasthtml.common import *
from monsterui.all import *
from .app import rt, PROPS
import bikidata
import json, traceback


def query_block():
    op = Div(
        Select(
            Option("must", value="must", selected=True),
            Option("should", value="should"),
            Option("not", value="not"),
            cls="op",
            style="margin: 1ch; padding: 0.5ch;",
        ),
        style="display: inline-block; margin: 0.1ch;",
    )
    predicate = Div(
        Select(
            Option("fts", value="fts"),
            Option(" - ", value="_", title="No value"),
            Option("id", value="id", selected=True),
            Option("semantic", value="semantic"),
            *[Option(f"{c} {p}", value=p) for c, p in PROPS],
            cls="pred",
            style="margin: 1ch; padding: 0.5ch;",
        ),
        style="display: inline-block; margin: 0.1ch;",
    )
    obj = Div(
        Input(type="text", style="width: 30vw", cls="obj"),
        style="display: inline-block; margin: 0.1ch;",
    )
    return DivHStacked(
        Div(
            Button(
                "-",
                style="padding: 0.2ch; border: 1px solid #ccc; border-radius: 8px;",
                cls="block_remove btn-sm",
            ),
            Button(
                "+",
                style="padding: 0.2ch; border: 1px solid #ccc; border-radius: 8px;",
                cls="block_add  btn-sm",
            ),
            cls="mr-1",
        ),
        op,
        predicate,
        obj,
    )


def obj_to_cell(obj, p_labels={}):
    buf = []
    for k, v in obj.items():
        if k in ("id", "graph"):
            continue
        buf.append(
            Div(
                Div(Span(k, cls="text-lg font-bold"), Span(p_labels.get(k, None))),
                Div(*[P(vv) for vv in v], cls="p-1 pl-4"),
            )
        )
    return Div(*buf)


@rt
def fragments_query_block():
    return Html(query_block())


@rt(methods=["POST"])
async def fragments_query(request: Request):

    # Parse JSON data from request body
    try:
        incoming = await request.body()
        data = json.loads(incoming)
    except json.JSONDecodeError:
        return Div("Invalid JSON data", cls="error")

    try:
        data["size"] = 20
        r = bikidata.query(data)
    except Exception as e:
        return Div(
            Pre(f"Error: {traceback.format_exc()}", cls="error"),
            Pre(json.dumps(data, indent=2)),
        )

    # For all the properties, we also want there labels for a friendlier display
    all_obj_properties = set(
        [
            piri
            for obj in r.get("results", {}).values()
            for piri in list(obj.keys())
            if piri.startswith("<")
        ]
    )
    filters = [{"op": "or", "p": "id", "o": piri} for piri in all_obj_properties]
    #    filters.append({"p": "<http://www.w3.org/2000/01/rdf-schema#label>"})

    piri_r = bikidata.query({"filters": filters})
    p_labels = {}
    for obj_iri, obj in piri_r.get("results", {}).items():
        label = obj.get("<http://www.w3.org/2000/01/rdf-schema#label>", [""])[0]
        if label:
            p_labels[obj_iri] = label

    aggregates = Div(
        *[
            Div(Strong(aggregate), *[P(agg_value) for agg_value in agg_values])
            for aggregate, agg_values in r.get("aggregates", {}).items()
        ]
    )

    # Create table with headers and rows
    table = Table(
        Thead(Tr(Th("ID"), Th("Obj"))),
        Tbody(
            *[
                Tr(
                    Td(str(uid)),
                    Td(obj_to_cell(obj, p_labels=p_labels)),
                )
                for uid, obj in r["results"].items()
            ]
        ),
        cls="table table-striped",
    )

    return Html(Div(H4(f"{r['total']} Results"), aggregates, table, cls="mt-4"))


@rt(methods=["POST"])
async def fragments_sql(request: Request):
    try:
        incoming = await request.body()
        data = json.loads(incoming)
    except json.JSONDecodeError:
        return Div("Invalid JSON data", cls="error")
    try:
        DB = bikidata.raw()
        results = DB.execute(data["query"]).fetch_df()

        table = TableFromLists(
            header_data=results.columns, body_data=results.itertuples(index=False)
        )

        return Div(H4("Search results"), table, cls="mt-4")

    except Exception as e:
        return Div(
            Pre(f"Error: {traceback.format_exc()}", cls="error"),
        )
