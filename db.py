from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SSN, SOSA
import os.path

SDTW = Namespace("http://ontology.hugonlabs.com/sdtw#")
QUDT = Namespace("http://qudt.org/schema/qudt/")

data_prefix = "http://data-webapp.hugonlabs.com/test1/"

class DBInterfaceError(Exception):
    pass

class FeatureAlreadyExistsError(DBInterfaceError):
    pass

class ObservablePropertyExistsError(DBInterfaceError):
    pass

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

    def convertToURIRef(self,x):
        """
        A URI, in string form, doesn't match with anything in rdflib
        This method converts URI strings to rdflib.URIRef, which does match
        """
        if isinstance(x,URIRef):
            return x
        else:
            return URIRef(x)

    def getLabel(self,x):
        x = self.convertToURIRef(x)
        return self.graph.value(x,RDFS.label).value

    def getComment(self,x):
        x = self.convertToURIRef(x)
        return self.graph.value(x,RDFS.comment).value

    def getListLabels(self,l):
        return [self.getLabel(x) for x in l]

    def listFeatures(self):
        return self.graph.subjects(RDF.type, SOSA.FeatureOfInterest)

    def addNewFeature(self,label,comment):
        featureURI = os.path.join(data_prefix,"features",label.lower())
        feature = URIRef(featureURI)
        if (feature,None,None) in self.graph:
            raise FeatureAlreadyExistsError(f"Feature with label '{label}' is already in graph")
        self.graph.add((feature,RDF.type,SOSA.FeatureOfInterest))
        self.graph.set((feature,RDFS.label,Literal(label)))
        self.graph.set((feature,RDFS.comment,Literal(comment)))

    def listObservableProperties(self,featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = sorted(self.graph.subjects(SSN.isPropertyOf,featureOfInterest),key=lambda x: self.graph.value(x,RDFS.label).value)
        return props

    def addNewObservableProperty(self,label,comment,feature,quantityKind,unit):
        feature = self.convertToURIRef(feature)
        featureName = self.getLabel(feature)
        propURI = os.path.join(data_prefix,"properties",featureName.lower(),label.lower())
        prop = URIRef(propURI)
        if (prop,None,None) in self.graph:
            raise ObservablePropertyExistsError(f"Prop with label '{label}' and feature '{featureName}' is already in graph")
        quantityKind = self.convertToURIRef(quantityKind)
        unit = self.convertToURIRef(unit)
        label = Literal(label)
        comment = Literal(comment)
        self.graph.add((prop,RDF.type,SOSA.ObservableProperty))
        self.graph.set((prop,RDFS.label,label))
        self.graph.set((prop,RDFS.comment,comment))
        self.graph.set((prop,SSN.isPropertyOf,feature))
        self.graph.set((prop,SDTW.hasQuantityKind,quantityKind))
        self.graph.set((prop,SDTW.hasUnit,unit))

    def getPrettyTitle(self,observedProperty):
        observedProperty = self.convertToURIRef(observedProperty)
        label = self.getLabel(observedProperty)
        unit = self.graph.value(observedProperty,SDTW.hasUnit)
        unit_label = self.graph.value(unit,QUDT.symbol)
        result = f"{label} [{unit_label}]"
        return result

    def getColumnHeadings(self,featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = list(self.listObservableProperties(featureOfInterest))
        headings = [self.getPrettyTitle(x) for x in props]
        return props, headings

    def getData(self,featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
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

    def enterData(self,feature,t,sensor,comment,datadict):
        featureName = self.getLabel(feature)
        stimulusURI = os.path.join(data_prefix,"stimuli",featureName.lower(),t.upper())
        stimulus = self.convertToURIRef(stimulusURI)


if __name__ == "__main__":
    db = DBInterface("car-example.ttl")
    db.addNewFeature("joke1","nock, nock: who's there?")
    #db.addNewFeature("car1","bad car")
    db.addNewObservableProperty("I1","Current through R1","http://data-webapp.hugonlabs.com/test1/features/joke1","http://qudt.org/vocab/quantitykind/ElectricCurrent","http://qudt.org/vocab/unit/A")
    #db.addNewObservableProperty("odometer","Odometer reading","http://data-webapp.hugonlabs.com/test1/features/car1","http://qudt.org/vocab/quantitykind/ElectricCurrent","http://qudt.org/vocab/unit/A")
    for feature in db.listFeatures():
        print(feature,db.getLabel(feature),db.getComment(feature))
        print(db.getColumnHeadings(feature))
        #print(db.getData(feature))
