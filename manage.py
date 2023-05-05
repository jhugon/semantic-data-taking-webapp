from db import DBInterface, graph_store_post, graph_store_get
from enum import Enum
from pathlib import Path
import logging
import typer

DATA_URI_BASE = ("http://data-webapp.hugonlabs.com/test1/",)


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
    data_uri_base: Path = DATA_URI_BASE,
    content_type: str = "text/turtle",
):
    """
    Dumps the contents of the RDF database at DBPATH to OUTFILE.
    """
    data = graph_store_get(dbpath, graph_uri=data_uri_base, content_type=content_type)
    with outfile.open("w") as outf:
        outf.write(data)


@app.command()
def write(
    dbpath: str,
    infile: Path,
    data_uri_base: Path = DATA_URI_BASE,
    content_type: str = "text/turtle",
):
    """
    Writes the contents of INFILE into the RDF database at DBPATH.
    """
    with infile.open() as inf:
        graph_store_post(
            dbpath, inf.read(), graph_uri=data_uri_base, content_type=content_type
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
