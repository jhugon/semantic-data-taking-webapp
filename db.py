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

    def listFeatures(self):
        return self.graph.subjects(RDF.type, SOSA.FeatureOfInterest)

    def listObservableProperties(self,featureOfInterest):
        props = sorted(self.graph.subjects(SSN.isPropertyOf,featureOfInterest),key=lambda x: self.graph.value(x,RDFS.label).value)
        return props

    def getPrettyTitle(self,observedProperty):
        label = db.getLabel(observedProperty)
        unit = self.graph.value(observedProperty,SDTW.hasUnit)
        unit_label = self.graph.value(unit,QUDT.symbol)
        result = f"{label} [{unit_label}]"
        return result

    def getColumnHeadings(self,featureOfInterest):
        props = list(self.listObservableProperties(featureOfInterest))
        headings = [self.getPrettyTitle(x) for x in props]
        return props, headings

    def getData(self,featureOfInterest):
        props = list(self.listObservableProperties(featureOfInterest))
        stimuli = set()
        for prop in props:
            for stimulus in self.graph.subjects(SSN.isProxyFor,prop):
                stimuli.add(stimulus)
        stimuli = sorted(list(stimuli),key=lambda t: self.graph.value(t,SDTW.hasTime).value)
        stim_times = [self.graph.value(stimulus,SDTW.hasTime).value for stimulus in stimuli]
        data = []
        for stimulus in stimuli:
            stim_data = []
            observations = list(self.graph.subjects(SSN.wasOriginatedBy,stimulus))
            for prop in props:
                val = None
                for observation in observations:
                    if (observation,SOSA.observedProperty,prop) in self.graph:
                        if val is None:
                            res = self.graph.value(observation,SOSA.hasResult)
                            val = self.graph.value(res,QUDT.value).value
                        else:
                            print(f"Warning: {stimulus} {prop} has more than one observation!")
                stim_data.append(val)
            data.append(stim_data)
        return stim_times, data


if __name__ == "__main__":
    db = DBInterface("car-example.ttl")
    for feature in db.listFeatures():
        print(db.getLabel(feature))
        print(db.getColumnHeadings(feature))
        print(db.getData(feature))
