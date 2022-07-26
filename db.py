from rdflib import ConjunctiveGraph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD, SSN, SOSA
from rdflib.store import NO_STORE, VALID_STORE
import os.path
import re
import logging

LOGGER = logging.getLogger(__name__)

SDTW = Namespace("http://ontology.hugonlabs.com/sdtw#")
QUDT = Namespace("http://qudt.org/schema/qudt/")

data_prefix = "http://data-webapp.hugonlabs.com/test1/"
user_prefix = os.path.join(data_prefix,"users/")

units_query = """
select ?unit_name
where {
    ?unit rdf:type qudt:Unit .
    ?unit rdfs:label ?unit_name .
}"""

quantity_kind_query = """
select ?qk_name
where {
    ?qk rdf:type qudt:QuantityKind .
    ?qk rdfs:label ?qk_name .
}"""

class DBInterfaceError(Exception):
    pass

class FeatureAlreadyExistsError(DBInterfaceError):
    pass

class ObservablePropertyExistsError(DBInterfaceError):
    pass

class DataValidationError(DBInterfaceError):
    pass

class GetSubjectError(DBInterfaceError):
    pass

class DBStoreError(DBInterfaceError):
    pass

class DBInterface:
    def __init__(self,store_path="web-db-store.bdb"):
        store_path = os.path.abspath(store_path)
        LOGGER.info(f"DB store at: {store_path}")
        self.store_path = store_path
        self.graph = self.load_graph(self.store_path)
        self.build_quantity_kind_list()
        #self.graph.serialize(destination="debug.ttl")

    def __del__(self):
        try:
            self.graph.close()
        except Exception:
            pass

    def load_graph(self,store_path):
        graph = ConjunctiveGraph("BerkeleyDB")
        opencode = graph.open(store_path,create=False)
        if opencode == NO_STORE:
            LOGGER.info(f"Store not initialized, initializing now...")
            graph.open(store_path,create=True)
            graph.parse("http://qudt.org/schema/qudt/")
            graph.parse("http://qudt.org/vocab/quantitykind/")
            graph.parse("http://qudt.org/vocab/unit/")
            graph.parse("ontology/sdtw.ttl")
            graph.parse("ontology/units.ttl")
            graph.commit()
            graph.close()
            LOGGER.info(f"Store initialized")
            return self.load_graph(store_path)
        elif opencode == VALID_STORE:
            LOGGER.info(f"Successfully loaded already initialized store")
            return graph
        else:
            raise DBStoreError(f"Database store at 'store_path' is corrupted")

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
        labels_set = set()
        for label in self.graph.objects(x,RDFS.label):
            labels_set.add(label)
        labels = list(labels_set)
        if len(labels) == 0:
            raise DBInterfaceError(f"{x} has no label")
        elif len(labels) == 1:
            return labels[0].value
        else:
            label_langs = [l.language for l in labels]
            en_us_count = label_langs.count("en-us")
            if en_us_count > 0:
                return labels[label_langs.index("en-us")].value
            en_count = label_langs.count("en")
            if en_count > 0:
                return labels[label_langs.index("en")].value
            return labels[0].value

    def getSubjectLabeledWithType(self,label,typ,label_lang=None):
        label2 = Literal(label,lang=label_lang)
        print(f"label2: {label2}")
        subjects = list(self.graph.subjects(RDFS.label,label2))
        print(f"subjects: {subjects}")
        if len(subjects) < 1:
            raise GetSubjectError(f"No subject with label '{label}'")
        matching_subjects = set()
        for subject in subjects:
            if (subject,RDF.type,typ) in self.graph:
                matching_subjects.add(subject)
        if len(matching_subjects) == 0:
            raise GetSubjectError(f"No subject with label '{label}' has type '{typ}'")
        elif len(matching_subjects) > 1:
            raise GetSubjectError(f"Multiple subjects with label '{label}' and type '{typ}'")
        return subjects[0]

    def getComment(self,x):
        x = self.convertToURIRef(x)
        return self.graph.value(x,RDFS.comment).value

    def getListLabels(self,l):
        return [self.getLabel(x) for x in l]

    def listFeatures(self):
        return self.graph.subjects(RDF.type, SOSA.FeatureOfInterest)

    def addNewFeature(self,label,comment):
        if not re.match(r"^\w+$",label):
            raise DataValidationError("Feature label must be more than one letter, number, or _")
        featureURI = os.path.join(data_prefix,"features",label.lower())
        feature = URIRef(featureURI)
        if (feature,None,None) in self.graph:
            raise FeatureAlreadyExistsError(f"Feature with label '{label}' is already in graph")
        self.graph.add((feature,RDF.type,SOSA.FeatureOfInterest))
        self.graph.set((feature,RDFS.label,Literal(label)))
        self.graph.set((feature,RDFS.comment,Literal(comment)))
        self.graph.commit()

    def listObservableProperties(self,featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = sorted(self.graph.subjects(SSN.isPropertyOf,featureOfInterest),key=lambda x: self.graph.value(x,RDFS.label).value)
        return props

    def addNewObservableProperty(self,label,comment,feature,quantityKind,unit):
        feature = self.convertToURIRef(feature)
        featureName = self.getLabel(feature)
        if not re.match(r"^\w+$",label):
            raise DataValidationError("Property label must be more than one letter, number, or _")
        propURI = os.path.join(data_prefix,"properties",featureName.lower(),label.lower())
        prop = URIRef(propURI)
        if (prop,None,None) in self.graph:
            raise ObservablePropertyExistsError(f"Prop with label '{label}' and feature '{featureName}' is already in graph")
        quantityKind = self.convertToURIRef(quantityKind)
        if (quantityKind,RDF.type,QUDT.QuantityKind) not in self.graph:
            raise DataValidationError(r"Quantity kind not found in database")
        unit = self.convertToURIRef(unit)
        if (unit,RDF.type,QUDT.Unit) not in self.graph:
            raise DataValidationError(r"Unit not found in database")
        label = Literal(label)
        comment = Literal(comment)
        self.graph.add((prop,RDF.type,SOSA.ObservableProperty))
        self.graph.set((prop,RDFS.label,label))
        self.graph.set((prop,RDFS.comment,comment))
        self.graph.set((prop,SSN.isPropertyOf,feature))
        self.graph.set((prop,SDTW.hasQuantityKind,quantityKind))
        self.graph.set((prop,SDTW.hasUnit,unit))
        self.graph.commit()

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
        """
        feature should be a featureOfInterest URI
        t should be a datetime ISO string
        sensor should be a sensor URI
        comment should be a comment string
        datadict should be a dict with keys the observableproperties of the feature and values the result values
        """
        assert(type(t) == str)
        feature = self.convertToURIRef(feature)
        sensor = self.convertToURIRef(sensor)
        featureName = self.getLabel(feature)
        props = list(self.listObservableProperties(feature))
        stimulusURI = os.path.join(data_prefix,"stimuli",featureName.lower(),t.upper())
        stimulus = self.convertToURIRef(stimulusURI)
        self.graph.add((stimulus,RDF.type,SSN.Stimulus))
        self.graph.set((stimulus,RDFS.comment,Literal(comment)))
        self.graph.set((stimulus,SDTW.hasTime,Literal(t,datatype=XSD.dateTime)))
        for prop in props:
            prop = self.convertToURIRef(prop)
            datum = None
            try:
                datum = datadict[str(prop)]
            except KeyError:
                continue
            if re.match(r"^\s*$",datum):
                continue
            try:
                datum = float(datum)
            except ValueError as e:
                raise DataValidationError(e)
            except TypeError as e:
                raise DataValidationError(e)
            unit = self.graph.value(prop,SDTW.hasUnit)
            propName = self.getLabel(prop)
            observationURI = os.path.join(data_prefix,"observations",featureName,propName,t)
            observation = self.convertToURIRef(observationURI)
            self.graph.add((stimulus,SSN.isProxyFor,prop))
            self.graph.add((observation,RDF.type,SOSA.Observation))
            self.graph.set((observation,RDFS.comment,Literal(comment)))
            self.graph.set((observation,SOSA.madeBySensor,sensor))
            self.graph.set((observation,SSN.wasOriginatedBy,stimulus))
            self.graph.set((observation,SOSA.hasFeatureOfInterest,feature))
            self.graph.set((observation,SOSA.observedProperty,prop))
            self.graph.set((observation,SOSA.resultTime,Literal(t,datatype=XSD.dateTime)))
            res = BNode()
            self.graph.set((observation,SOSA.hasResult,res))
            self.graph.set((res,RDF.type,SOSA.Result))
            self.graph.set((res,RDF.type,QUDT.Quantity))
            self.graph.set((res,QUDT.value,Literal(datum)))
            self.graph.set((res,QUDT.unit,unit))
        self.graph.commit()

    def get_quantity_kind_list(self):
        return self.quantity_kind_and_label_list

    def build_quantity_kind_list(self):
        self.quantity_kinds = list(self.graph.subjects(RDF.type,QUDT.QuantityKind))
        self.quantity_kind_and_label_list = []
        for quantity_kind in self.quantity_kinds:
            label = self.getLabel(quantity_kind)
            self.quantity_kind_and_label_list.append((str(quantity_kind),label))
        self.quantity_kind_and_label_list.sort(key=lambda x: x[1])

    def get_units_for_quantity_kind(self,quantity_kind):
        quantity_kind = self.convertToURIRef(quantity_kind)
        results = []
        for unit in self.graph.objects(quantity_kind,QUDT.applicableUnit):
            label = self.getLabel(unit)
            results.append((str(unit),label))
        results.sort(key=lambda x: x[1])
        return results


if __name__ == "__main__":
    db = DBInterface()
    #db.addNewFeature("joke1","nock, nock: who's there?")
    ##db.addNewFeature("car1","bad car")
    #db.addNewObservableProperty("I1","Current through R1","http://data-webapp.hugonlabs.com/test1/features/joke1","http://qudt.org/vocab/quantitykind/ElectricCurrent","http://qudt.org/vocab/unit/A")
    #db.addNewObservableProperty("L1","Length of R1","http://data-webapp.hugonlabs.com/test1/features/joke1","http://qudt.org/vocab/quantitykind/Length","http://qudt.org/vocab/unit/M")
    ##db.addNewObservableProperty("odometer","Odometer reading","http://data-webapp.hugonlabs.com/test1/features/car1","http://qudt.org/vocab/quantitykind/ElectricCurrent","http://qudt.org/vocab/unit/A")
    #db.enterData("http://data-webapp.hugonlabs.com/test1/features/joke1","2022-01-01T00:00:00Z","http://data-webapp.hugonlabs.com/test1/users/jhugon","Test data points",{'http://data-webapp.hugonlabs.com/test1/properties/joke1/i1':'0.2','http://data-webapp.hugonlabs.com/test1/properties/joke1/l1':'0.05'})
    #db.enterData("http://data-webapp.hugonlabs.com/test1/features/joke1","2022-01-01T11:11:11Z","http://data-webapp.hugonlabs.com/test1/users/jhugon","Test data points",{'http://data-webapp.hugonlabs.com/test1/properties/joke1/i1':'0.1','http://data-webapp.hugonlabs.com/test1/properties/joke1/l1':'0.06'})
    #db.enterData("http://data-webapp.hugonlabs.com/test1/features/joke1","2022-01-01T18:00:00Z","http://data-webapp.hugonlabs.com/test1/users/jhugon","Test data points",{'http://data-webapp.hugonlabs.com/test1/properties/joke1/i1':'0.1'})
    for feature in db.listFeatures():
        print(feature,db.getLabel(feature),db.getComment(feature))
        print(db.getColumnHeadings(feature))
        print(db.getData(feature))
        print()
