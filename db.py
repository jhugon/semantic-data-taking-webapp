from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, SSN, SOSA

SDTW = Namespace("http://ontology.hugonlabs.com/sdtw#")
QUDT = Namespace("http://qudt.org/schema/qudt/")


class DBInterface:
    def __init__(self,graph_uri):
        self.graph = Graph()
        self.graph.parse(graph_uri)
        #self.graph.parse("http://qudt.org/schema/qudt")
        #self.graph.parse("http://qudt.org/vocab/quantitykind")
        #self.graph.parse("http://qudt.org/vocab/unit")
        self.graph.parse("cache/qudt")
        self.graph.parse("cache/quantitykind")
        self.graph.parse("cache/unit")

    def getLabel(self,x):
        return self.graph.value(x,RDFS.label).value

    def getListLabels(self,l):
        return [self.graph.value(x,RDFS.label).value for x in l]

    def listFeatures(self,):
        return self.graph.subjects(RDF.type, SOSA.FeatureOfInterest)

    def listObservableProperties(self,featureOfInterest):
        return self.graph.subjects(SSN.isPropertyOf,featureOfInterest)

    def getPrettyTitle(self,observedProperty):
        label = db.getLabel(observedProperty)
        unit = self.graph.value(observedProperty,SDTW.hasUnit)
        print(unit)
        for p in self.graph.predicates(unit):
            print("        ",p)
        unit_label = self.graph.value(unit,QUDT.symbol)
        result = f"{label} [{unit_label}]"
        return result

if __name__ == "__main__":
    db = DBInterface("car-example.ttl")
    for feature in db.listFeatures():
        print(db.getLabel(feature))
        for prop in db.listObservableProperties(feature):
            print(db.getPrettyTitle(prop))
    db.graph.serialize(destination="silly.ttl")
