from db import DBInterface, graph_store_post, graph_store_get
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse
import logging
import typer
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff


class DBType(str, Enum):
    BerkelyDB = "BerkelyDB"
    SPARQLUpdateStore = "SPARQLUpdateStore"


app = typer.Typer()


@app.command()
def init(dbpath: str, dbtype: DBType = DBType.SPARQLUpdateStore):
    """
    Initializes the RDF database at DBPATH with standard quantities and units.
    """
    DBInterface.initialize_store(dbpath, dbtype.value)


@app.command()
def dump(
    dbpath: str,
    outfile: Path,
    content_type: str = "application/trig",
):
    """
    Dumps the contents of the RDF database at DBPATH to OUTFILE.
    """
    data = graph_store_get(dbpath, content_type=content_type)
    with outfile.open("w") as outf:
        outf.write(data)


@app.command()
def write(
    dbpath: str,
    infile: Path,
    data_uri_base: Path = None,
    content_type: str = "application/trig",
):
    """
    Writes the contents of INFILE into the RDF database at DBPATH.
    """
    with infile.open() as inf:
        graph_store_post(
            dbpath, inf.read(), graph_uri=data_uri_base, content_type=content_type
        )


@app.command()
def compare(graph1: Path, graph2: Path):
    """
    Compare the RDF graph, GRAPH1 to the RDF graph, GRAPH2. They must both be local files
    """

    graph1loc = graph1
    graph2loc = graph2

    graph1 = Graph()
    graph1.parse(graph1loc)
    graph2 = Graph()
    graph2.parse(graph2loc)
    graph1iso = to_isomorphic(graph1)
    graph2iso = to_isomorphic(graph2)
    if graph1iso == graph2iso:
        print("Graphs are isomorphic")
    else:
        print("Graphs are not isomorphic")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
