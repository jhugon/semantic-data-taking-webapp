from rdflib import Dataset, Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD, SSN, SOSA
from rdflib.store import NO_STORE, VALID_STORE
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, _node_to_sparql
import os.path
import re
import logging
import berkeleydb
import httpx
import time
from io import StringIO
import csv

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)

QUDT = Namespace("http://qudt.org/schema/qudt/")
QUANTITYKIND = Namespace("http://qudt.org/vocab/quantitykind/")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")


def my_bnode_ext(node):
    if isinstance(node, BNode):
        return "<bnode:b%s>" % node
    return _node_to_sparql(node)


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
    def __init__(
        self,
        store_path="web-db-store.bdb",
        data_uri_base="http://data-webapp.hugonlabs.com/test1/",
        store_type="BerkeleyDB",
    ):
        if store_type == "BerkeleyDB":
            store_path = os.path.abspath(store_path)
        self.store_path = store_path
        self.store_type = store_type
        self.data_uri_base = data_uri_base
        self.store = None
        self.dataset = None

        LOGGER.info(f"DB store at: {self.store_path}")
        LOGGER.info(f"DB store type: {self.store_type}")
        LOGGER.info(f"DB data URI base: {self.data_uri_base}")

        self.dataset = self.load_dataset(self.store_path, self.store_type)
        nRetries = 3
        retryTimeout = 5
        for iTry in reversed(range(nRetries + 1)):
            try:
                self.data_graph = self.dataset.graph(self.data_uri_base)
            except Exception as e:
                LOGGER.warning(
                    f"Error while reading from dataset: {type(e)} {e}, retrying in {retryTimeout} s"
                )
                if iTry == 0:
                    raise Exception(
                        f"Couldn't access dataset after {nRetries} {type(e)} {e}"
                    )
                time.sleep(retryTimeout)
            else:
                break
        self.build_quantity_kind_list()

        self.SDTW = Namespace("http://ontology.hugonlabs.com/sdtw#")

    def __del__(self):
        try:
            self.dataset.close()
        except Exception as e:
            logging.warning(f"Exception while trying to close dataset: {type(e)}: {e}")

    def convertToURIRef(self, x):
        """
        A URI, in string form, doesn't match with anything in rdflib
        This method converts URI strings to rdflib.URIRef, which does match
        """
        if isinstance(x, URIRef):
            return x
        else:
            return URIRef(x)

    def triples(self, quad_or_triple):
        if len(quad_or_triple) == 3 or (
            len(quad_or_triple) == 4 and quad_or_triple[3] is None
        ):
            for graph in self.dataset.graphs():
                for tr in graph.triples(quad_or_triple[:3]):
                    yield tr
        elif len(quad_or_triple) == 4:
            graph_name = quad_or_triple[3]
            for tr in self.dataset.graph(graph_name).triples(quad_or_triple[:3]):
                yield tr
        else:
            raise ValueError(
                f"argument quad_or_triple: '{quad_or_triple}' should be a 3 or 4 tuple"
            )

    def quads(self, quad_or_triple):
        if len(quad_or_triple) == 3 or (
            len(quad_or_triple) == 4 and quad_or_triple[3] is None
        ):
            for graph in self.dataset.graphs():
                for tr in graph.triples(quad_or_triple[:3]):
                    yield (tr[0], tr[1], tr[2], graph.identifier)
        elif len(quad_or_triple) == 4:
            graph_name = quad_or_triple[3]
            for tr in self.dataset.graph(graph_name).triples(quad_or_triple[:3]):
                yield (tr[0], tr[1], tr[2], graph_name)
        else:
            raise ValueError(
                f"argument quad_or_triple: '{quad_or_triple}' should be a 3 or 4 tuple"
            )

    def getLabel(self, x, graph_name=None):
        x = self.convertToURIRef(x)
        labels_set = set()
        for s, p, label in self.triples((x, RDFS.label, None)):
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

    def getSubjectLabeledWithType(self, label, typ, label_lang=None, graph_name=None):
        label2 = Literal(label, lang=label_lang)
        subjects = list(graph.subjects(RDFS.label, label2))
        subjects = []
        labelFound = False
        for s, p, o, c in self.quads((None, RDFS.label, label2, graph_name)):
            labelFound = True
            if (s, RDF.type, typ, c) in self.dataset:
                subjects.append(s)
        ### Note that graph_name None means search all graphs!
        if len(subjects) < 1:
            if labelFound:
                raise GetSubjectError(
                    f"No subject with label '{label}' has type '{typ}' in graph '{graph_name}'"
                )
            else:
                raise GetSubjectError(
                    f"No subject with label '{label}' in graph '{graph_name}'"
                )
        elif len(matching_subjects) > 1:
            raise GetSubjectError(
                f"Multiple subjects with label '{label}' and type '{typ}' in graph '{graph_name}'"
            )
        return subjects[0]

    def getComment(self, x, graph_name=None):
        x = self.convertToURIRef(x)
        results = []
        for s, p, o, c in self.quads((x, RDFS.comment, None, graph_name)):
            results.append(o.value)
        if len(results) < 1:
            raise DBInterfaceError(f"No comment found for {x} in graph '{graph_name}'")
        return results[0]

    def getListLabels(self, l, graph_name=None):
        return [self.getLabel(x, graph_name=graph_name) for x in l]

    def listFeatures(self):
        results = []
        for s, p, o in self.triples(
            (None, RDF.type, SOSA.FeatureOfInterest, self.data_uri_base)
        ):
            results.append(s)
        return results

    def addNewFeature(self, label, comment):
        if not re.match(r"^\w+$", label):
            raise DataValidationError(
                "Feature label must be more than one letter, number, or _"
            )
        featureURI = os.path.join(self.data_uri_base, "features", label.lower())
        feature = URIRef(featureURI)
        if (feature, None, None) in self.data_graph:
            raise FeatureAlreadyExistsError(
                f"Feature with label '{label}' is already in graph"
            )
        self.data_graph.add((feature, RDF.type, SOSA.FeatureOfInterest))
        self.data_graph.set((feature, RDFS.label, Literal(label)))
        self.data_graph.set((feature, RDFS.comment, Literal(comment)))
        self.data_graph.commit()

    def listObservableProperties(self, featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = sorted(
            self.data_graph.subjects(SSN.isPropertyOf, featureOfInterest),
            key=lambda x: self.data_graph.value(x, RDFS.label).value,
        )
        return props

    def addNewObservableProperty(
        self, label, proptype, comment, feature, quantityKind, unit
    ):
        LOGGER.debug(
            f"addNewObservableProperty: label: {label} proptype: {proptype} feature: {feature} quantityKind: {quantityKind} unit: {unit}"
        )
        feature = self.convertToURIRef(feature)
        featureName = self.getLabel(feature)
        if not re.match(r"^\w+$", label):
            raise DataValidationError(
                "Property label must be more than one letter, number, or _"
            )
        propURI = os.path.join(
            self.data_uri_base, "properties", featureName.lower(), label.lower()
        )
        prop = URIRef(propURI)
        if (prop, None, None) in self.data_graph:
            raise ObservablePropertyExistsError(
                f"Prop with label '{label}' and feature '{featureName}' is already in graph"
            )
        label = Literal(label)
        comment = Literal(comment)
        match proptype:
            case "quantitative":
                quantityKind = self.convertToURIRef(quantityKind)
                if (
                    len(
                        [
                            quad
                            for quad in self.triples(
                                (quantityKind, RDF.type, QUDT.QuantityKind)
                            )
                        ]
                    )
                    < 1
                ):
                    raise DataValidationError(r"Quantity kind not found in database")
                unit = self.convertToURIRef(unit)
                unitType = QUDT.Unit
                if quantityKind == QUANTITYKIND.Currency:
                    unitType = (
                        QUDT.CurrencyUnit
                    )  ## Because Currency has its own unit type
                if len([quad for quad in self.triples((unit, RDF.type, unitType))]) < 1:
                    raise DataValidationError(r"Unit not found in database")
                self.data_graph.add((prop, RDF.type, SOSA.ObservableProperty))
                self.data_graph.set((prop, RDFS.label, label))
                self.data_graph.set((prop, RDFS.comment, comment))
                self.data_graph.set((prop, SSN.isPropertyOf, feature))
                self.data_graph.set(
                    (prop, self.SDTW.hasObservableType, self.SDTW.quantitative)
                )
                self.data_graph.set((prop, self.SDTW.hasQuantityKind, quantityKind))
                self.data_graph.set((prop, self.SDTW.hasUnit, unit))
                self.data_graph.commit()
            case "categorical":
                self.data_graph.add((prop, RDF.type, SOSA.ObservableProperty))
                self.data_graph.set((prop, RDFS.label, label))
                self.data_graph.set((prop, RDFS.comment, comment))
                self.data_graph.set((prop, SSN.isPropertyOf, feature))
                self.data_graph.set(
                    (prop, self.SDTW.hasObservableType, self.SDTW.categorical)
                )
                self.data_graph.commit()
            case "geographicpoint":
                self.data_graph.add((prop, RDF.type, SOSA.ObservableProperty))
                self.data_graph.set((prop, RDFS.label, label))
                self.data_graph.set((prop, RDFS.comment, comment))
                self.data_graph.set((prop, SSN.isPropertyOf, feature))
                self.data_graph.set((prop, self.SDTW.hasObservableType, GEO.point))
                self.data_graph.commit()
            case other:
                raise ValueError(f"Unknown property type: {other}")

    def getPrettyTitle(self, observedProperty):
        observedProperty = self.convertToURIRef(observedProperty)
        label = self.getLabel(observedProperty)
        proptype = self.getPropertyObservableType(observedProperty)
        match proptype:
            case self.SDTW.quantitative:
                unit = list(self.triples((observedProperty, self.SDTW.hasUnit, None)))[
                    0
                ][2]
                unit_symbols = list(self.triples((unit, QUDT.symbol, None)))
                unit_ucumCode = list(self.triples((unit, QUDT.ucumCode, None)))
                unit_label = self.getLabel(unit)
                if len(unit_symbols) > 0:
                    unit_label = unit_symbols[0][2]
                elif len(unit_ucumCode) > 0:
                    unit_label = unit_ucumCode[0][2]
                result = f"{label} [{unit_label}]"
                return result
            case self.SDTW.categorical:
                result = f"{label}"
                return result
            case GEO.point:
                result = f"{label} [Geo Point]"
                return result
            case other:
                raise ValueError(f"Unknown property type: {other}")

    def getPropertyObservableType(self, observedProperty):
        observedProperty = self.convertToURIRef(observedProperty)
        trps = list(self.triples((observedProperty, self.SDTW.hasObservableType, None)))
        LOGGER.debug(f"{observedProperty} hasObservableType {[x[2] for x in trps]}")
        match trps:
            case []:
                LOGGER.debug(
                    f"Property {observedProperty} has no ObservableType, assuming quantitative"
                )
                return self.SDTW.quantitative
            case [(s, p, o)]:
                return o
            case _:
                raise ValueError(
                    f"Property {observedProperty} has more than one ObservableType: {trips}"
                )

    def getPropertyQuantityKindAndUnit(self, observedProperty):
        observedProperty = self.convertToURIRef(observedProperty)
        trps = list(self.triples((observedProperty, self.SDTW.hasObservableType, None)))
        match trps:
            case []:
                LOGGER.info(
                    f"Property {observedProperty} has no ObservableType, assuming quantitative"
                )
                quantityKind = list(
                    self.triples((observedProperty, self.SDTW.hasQuantityKind, None))
                )[0][2]
                unit = list(self.triples((observedProperty, self.SDTW.hasUnit, None)))[
                    0
                ][2]
                return quantityKind, unit
            case [(s, p, self.SDTW.quantitative)]:
                quantityKind = list(
                    self.triples((observedProperty, self.SDTW.hasQuantityKind, None))
                )[0][2]
                unit = list(self.triples((observedProperty, self.SDTW.hasUnit, None)))[
                    0
                ][2]
                return quantityKind, unit
            case [(s, p, self.SDTW.categorical)]:
                raise ValueError(
                    f"Property {observedProperty} is categorical, there are no QK or units"
                )
            case [(s, p, GEO.point)]:
                raise ValueError(
                    f"Property {observedProperty} is geographic point, there are no QK or units"
                )
            case _:
                raise ValueError(
                    f"Property {observedProperty} has more than one ObservableType: {trips}"
                )

    def getColumnHeadings(self, featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = list(self.listObservableProperties(featureOfInterest))
        headings = [self.getPrettyTitle(x) for x in props]
        return props, headings

    def getData(self, featureOfInterest):
        featureOfInterest = self.convertToURIRef(featureOfInterest)
        props = list(self.listObservableProperties(featureOfInterest))
        proptypes = [self.getPropertyObservableType(prop) for prop in props]
        stimuli = set()
        for prop in props:
            for stimulus in self.data_graph.subjects(SSN.isProxyFor, prop):
                stimuli.add(stimulus)
        stimuli = sorted(
            list(stimuli),
            key=lambda t: self.data_graph.value(t, self.SDTW.hasTime).value,
        )
        stim_times = [
            self.data_graph.value(stimulus, self.SDTW.hasTime).value
            for stimulus in stimuli
        ]
        stim_comments = [
            self.data_graph.value(stimulus, RDFS.comment).value for stimulus in stimuli
        ]
        data = []
        for stimulus in stimuli:
            quant_query = f"""
            prefix sosa: <http://www.w3.org/ns/sosa/>
            prefix ssn: <http://www.w3.org/ns/ssn/>
            prefix qudt: <http://qudt.org/schema/qudt/>
            select ?prop ?value
            where {{
                ?obs ssn:wasOriginatedBy {stimulus.n3()} .
                ?obs sosa:observedProperty ?prop .
                ?obs sosa:hasResult ?result .
                ?result qudt:value ?value .
            }}
            """
            quant_qres = list(self.data_graph.query(quant_query))
            for row in quant_qres:
                LOGGER.debug("        " + str(row))

            other_query = f"""
            prefix sosa: <http://www.w3.org/ns/sosa/>
            prefix ssn: <http://www.w3.org/ns/ssn/>
            prefix qudt: <http://qudt.org/schema/qudt/>
            select ?prop ?result
            where {{
                ?obs ssn:wasOriginatedBy {stimulus.n3()} .
                ?obs sosa:observedProperty ?prop .
                ?obs sosa:hasResult ?result .
                filter not exists {{ ?result qudt:value ?value . }}
                filter ( datatype(?result) != '' )
            }}
            """
            other_qres = list(self.data_graph.query(other_query))
            for row in other_qres:
                LOGGER.debug("        " + str(row))
            propValueMap = dict()
            for row in quant_qres + other_qres:
                if row[0] in propValueMap:
                    LOGGER.error(f"Propery has multiple values for stimulus")
                    LOGGER.error(f"Propery {row[0]}")
                    LOGGER.error(f"Stimulus {stimulus}")
                    LOGGER.error(f"Values include:")
                    LOGGER.error(propValueMap[row[0]])
                    LOGGER.error(row[1])
                    raise Exception(f"property has multiple values for stimulus")
                else:
                    propValueMap[row[0]] = row[1]

            #### Multi-valued props

            geo_query = f"""
            prefix sosa: <http://www.w3.org/ns/sosa/>
            prefix ssn: <http://www.w3.org/ns/ssn/>
            prefix qudt: <http://qudt.org/schema/qudt/>
            prefix wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            select ?prop ?latitude ?longitude ?altitude ?accuracy ?altitudeAccuracy
            where {{
                ?obs ssn:wasOriginatedBy {stimulus.n3()} .
                ?obs sosa:observedProperty ?prop .
                ?obs sosa:hasResult ?result .
                Optional {{ ?result wgs84_pos:latitude ?latitude }} .
                Optional {{ ?result wgs84_pos:longitude ?longitude }} .
                Optional {{ ?result wgs84_pos:altitude ?altitude }} .
                Optional {{ ?result wgs84_pos:altitudeAccuracy ?altitudeAccuracy }} .
                Optional {{ ?result wgs84_pos:accuracy ?accuracy }} .
            }}
            """
            geo_qres_raw = list(self.data_graph.query(geo_query))
            for row in geo_qres_raw:
                LOGGER.debug("        " + str(row))
            propValueMapGeo = {}
            for row in geo_qres_raw:
                if row[1:].count(None) == len(row) - 1:
                    continue
                if row[0] in propValueMapGeo:
                    LOGGER.error(f"Propery has multiple values for stimulus")
                    LOGGER.error(f"Propery {row[0]}")
                    LOGGER.error(f"Stimulus {stimulus}")
                    LOGGER.error(f"Values include:")
                    LOGGER.error(propValueMap[row[0]])
                    LOGGER.error(row)
                    raise Exception(f"property has multiple values for stimulus")
                else:
                    LOGGER.debug(f"resultRow: {row}")
                    LOGGER.debug(f"resultRow: {row['latitude']}")
                    row2 = {
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                        "altitude": row["altitude"],
                        "accuracy": row["accuracy"],
                        "altitudeAccuracy": row["altitudeAccuracy"],
                    }
                    for key in row2:
                        if isinstance(row2[key], Literal):
                            row2[key] = row2[key].value
                    propValueMapGeo[row["prop"]] = row2
            LOGGER.debug(f"propValueMapGeo: {propValueMapGeo}")
            propValueMap.update(propValueMapGeo)

            data_row = []
            for prop in props:
                try:
                    value = propValueMap[prop]
                    data_row.append(value)
                    LOGGER.debug(f"  {prop}: {value}")
                except KeyError:
                    data_row.append(None)
                    continue
            data.append(data_row)
        return stim_times, data, stim_comments

    def enterData(self, feature, t, sensor, comment, datadict):
        """
        feature should be a featureOfInterest URI
        t should be a datetime ISO string
        sensor should be a sensor URI
        comment should be a comment string
        datadict should be a dict with keys the observableproperties of the feature and values the result values
        """
        if not isinstance(t, str):
            raise TypeError(f"t should be a datetime ISO string, not: {type(t)} {t}")
        feature = self.convertToURIRef(feature)
        sensor = self.convertToURIRef(sensor)
        featureName = self.getLabel(feature)
        props = list(self.listObservableProperties(feature))
        stimulusURI = os.path.join(
            self.data_uri_base, "stimuli", featureName.lower(), t.upper()
        )
        stimulus = self.convertToURIRef(stimulusURI)
        tmp_graph = Graph()
        tmp_graph.add((stimulus, RDF.type, SSN.Stimulus))
        tmp_graph.set((stimulus, RDFS.comment, Literal(comment)))
        tmp_graph.set((stimulus, self.SDTW.hasTime, Literal(t, datatype=XSD.dateTime)))

        LOGGER.debug(f"datadict: {datadict}")
        for prop in props:
            prop = self.convertToURIRef(prop)
            datum = None
            proptype = self.getPropertyObservableType(prop)
            match proptype:
                case self.SDTW.quantitative:
                    try:
                        datum = datadict[str(prop)]
                    except KeyError:
                        continue
                    if re.match(r"^\s*$", datum):
                        continue
                    try:
                        datum = float(datum)
                    except ValueError as e:
                        raise DataValidationError(e)
                    except TypeError as e:
                        raise DataValidationError(e)
                    observation = self._addObservationTriples(
                        tmp_graph, prop, stimulus, sensor, feature, featureName, t
                    )
                    unit = self.data_graph.value(prop, self.SDTW.hasUnit)
                    res = BNode()
                    tmp_graph.set((observation, SOSA.hasResult, res))
                    tmp_graph.set((res, RDF.type, SOSA.Result))
                    tmp_graph.set((res, RDF.type, QUDT.Quantity))
                    tmp_graph.set((res, QUDT.value, Literal(datum)))
                    tmp_graph.set((res, QUDT.unit, unit))
                case self.SDTW.categorical:
                    try:
                        datum = datadict[str(prop)]
                    except KeyError:
                        continue
                    if re.match(r"^\s*$", datum):
                        continue
                    observation = self._addObservationTriples(
                        tmp_graph, prop, stimulus, sensor, feature, featureName, t
                    )
                    tmp_graph.set((observation, SOSA.hasResult, Literal(datum)))
                case GEO.point:
                    res = BNode()
                    observation = None
                    subprops = [
                        "latitude",
                        "longitude",
                        "altitude",
                        "altitudeAccuracy",
                        "accuracy",
                    ]
                    for subprop in subprops:
                        try:
                            datum = datadict[subprop + "_" + str(prop)]
                        except KeyError:
                            continue
                        if re.match(r"^\s*$", datum):
                            continue
                        try:
                            datum = float(datum)
                        except ValueError as e:
                            raise DataValidationError(e)
                        except TypeError as e:
                            raise DataValidationError(e)
                        if observation is None:
                            observation = self._addObservationTriples(
                                tmp_graph,
                                prop,
                                stimulus,
                                sensor,
                                feature,
                                featureName,
                                t,
                            )
                            tmp_graph.set((observation, SOSA.hasResult, res))
                        subpropURI = getattr(GEO, subprop)
                        tmp_graph.set((res, subpropURI, Literal(datum)))
                case other:
                    raise ValueError(f"property {prop} type not recognized: {other}")
        tmp_graph.commit()
        ## Funny business with tmp_graph to only do one submission to DB rather than tons
        ## Very significant performance improvement
        tmp_graph_ttl = tmp_graph.serialize(format="ttl")
        LOGGER.debug(tmp_graph_ttl)
        graph_store_post(self.store_path, tmp_graph_ttl, graph_uri=self.data_uri_base)

    def getCSV(self, feature):
        feature = self.convertToURIRef(feature)
        props, headings = self.getColumnHeadings(feature)
        stim_times, data, stim_comments = self.getData(feature)
        result = ""
        strfile = StringIO()
        csvwriter = csv.writer(strfile)
        csvwriter.writerow(("Timestamp", *headings, "Comment"))
        for stim_time, data_row, stim_comment in zip(stim_times, data, stim_comments):
            row = (stim_time, *data_row, stim_comment)
            csvwriter.writerow(row)
        result = strfile.getvalue()
        return result

    def getDataRDF(self):
        """
        Downloads whole database in Turtle format
        """
        return graph_store_get(self.store_path)

    def getCategories(self, observedProperty):
        observedProperty = self.convertToURIRef(observedProperty)
        proptype = self.getPropertyObservableType(observedProperty)
        if proptype != self.SDTW.categorical:
            return None
        else:
            category_query = f"""
            prefix sosa: <http://www.w3.org/ns/sosa/>
            select ?category
            from <{self.data_uri_base}>
            where {{
                ?observation sosa:observedProperty {observedProperty.n3()} .
                ?observation sosa:hasResult ?category .
            }}"""  # nosec

            qres = self.dataset.query(category_query)
            result = set()
            for row in qres:
                result.add(row.category.value)
            return list(result)

    def get_quantity_kind_list(self):
        return self.quantity_kind_and_label_list

    def build_quantity_kind_list(self):
        quantity_kind_query = """
        prefix qudt: <http://qudt.org/schema/qudt/>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?qk ?qk_name
        from <http://qudt.org/vocab/quantitykind/>
        from <http://qudt.org/vocab/currency/>
        from <http://qudt.org/vocab/unit/>
        from <http://schema.hugonlabs.com/sdtw#>
        from <http://ontology.hugonlabs.com/sdtw#>
        where {
            ?qk rdf:type qudt:QuantityKind .
            ?qk rdfs:label ?qk_name .
            FILTER (lang(?qk_name) = "" || langmatches(lang(?qk_name), "en"))
        }"""

        self.quantity_kinds = []
        self.quantity_kind_and_label_list = []
        qres = self.dataset.query(quantity_kind_query)
        for row in qres:
            self.quantity_kinds.append(row.qk)
            self.quantity_kind_and_label_list.append((row.qk, row.qk_name))
        self.quantity_kind_and_label_list.sort(key=lambda x: x[1])

    def get_units_for_quantity_kind(self, quantity_kind):
        quantity_kind = self.convertToURIRef(quantity_kind)
        results = []
        for s, p, unit, c in self.quads(
            (quantity_kind, QUDT.applicableUnit, None, None)
        ):
            label = self.getLabel(unit)
            results.append((str(unit), label))
        results.sort(key=lambda x: x[1])
        return results

    @staticmethod
    def load_dataset(store_path, store_type, create=False):
        dataset = None
        if store_type == "BerkeleyDB":
            dataset = Dataset(store_type)
            try:
                opencode = dataset.open(store_path, create=create)
            except berkeleydb.db.DBNoSuchFileError:
                LOGGER.error(f"Database store {store_path} doesn't exist")
                raise DBStoreError(f"Database store at '{store_path}' doesn't exist")
            else:
                if opencode == NO_STORE:
                    LOGGER.error(f"Database store {store_path} not initialized")
                    raise DBStoreError(
                        f"Database store at '{store_path}' not initialized"
                    )
                elif opencode == VALID_STORE:
                    LOGGER.info(f"Successfully loaded store")
                    return dataset
                else:
                    LOGGER.error(f"Database store {store_path} is corrupted")
                    raise DBStoreError(f"Database store at '{store_path}' is corrupted")
        elif store_type == "SPARQLUpdateStore":
            store = SPARQLUpdateStore(
                query_endpoint=store_path,
                update_endpoint=store_path,
                node_to_sparql=my_bnode_ext,
            )
            dataset = Dataset(store)
            return dataset
        else:
            raise ValueError(f"store_type: '{store_type}' not allowed")

    @staticmethod
    def initialize_store(store_path, store_type="BerkeleyDB"):
        if store_type == "BerkeleyDB":
            dataset = DBInterface.load_dataset(store_path, store_type, create=True)
            LOGGER.info(f"Connected to DB")
            dataset.parse("http://qudt.org/schema/qudt/")
            dataset.commit()
            LOGGER.info(f"QUDT schema committed to DB")
            dataset.parse("http://qudt.org/vocab/quantitykind/")
            dataset.commit()
            LOGGER.info(f"QUDT quantity kind schema committed to DB")
            dataset.parse("http://qudt.org/vocab/unit/")
            dataset.commit()
            LOGGER.info(f"QUDT unit vocab committed to DB")
            dataset.parse("ontology/sdtw.ttl")
            dataset.commit()
            LOGGER.info(f"SDTW vocab committed to DB")
            dataset.parse("ontology/units.ttl")
            dataset.commit()
            LOGGER.info(f"SDTW units vocab committed to DB")
            dataset.close()
        elif store_type == "SPARQLUpdateStore":
            LOGGER.info(f"Using Graph Store Protocol to upload triples into DB...")
            with open("ontology/sdtw.ttl") as f:
                graph_store_post(
                    store_path, f.read(), "http://ontology.hugonlabs.com/sdtw#"
                )
            LOGGER.info(f"sdtw.ttl ontology uploaded")
            with open("ontology/units.ttl") as f:
                graph_store_post(
                    store_path, f.read(), "http://schema.hugonlabs.com/sdtw#"
                )
            LOGGER.info(f"units.ttl ontology uploaded")
            for url in [
                "http://qudt.org/schema/qudt/",
                "http://qudt.org/vocab/quantitykind/",
                "http://qudt.org/vocab/unit/",
                "http://qudt.org/vocab/currency/",
            ]:
                LOGGER.info(f"Downloading triples from {url}")
                response = httpx.get(url, follow_redirects=True)
                response.raise_for_status()
                content_type = response.headers["content-type"]
                LOGGER.info(
                    f"Uploading triples from {url} with content-type '{content_type}'"
                )
                # LOGGER.info(response.text)
                graph_store_post(
                    store_path, response.text, graph_uri=url, content_type=content_type
                )
                LOGGER.info(f"Done with {url}")

    def _addObservationTriples(
        self, tmp_graph, prop, stimulus, sensor, feature, featureName, t
    ):
        propName = self.getLabel(prop)
        observationURI = os.path.join(
            self.data_uri_base, "observations", featureName, propName, t
        )
        observation = self.convertToURIRef(observationURI)
        tmp_graph.add((stimulus, SSN.isProxyFor, prop))
        tmp_graph.add((observation, RDF.type, SOSA.Observation))
        tmp_graph.set((observation, SOSA.madeBySensor, sensor))
        tmp_graph.set((observation, SSN.wasOriginatedBy, stimulus))
        tmp_graph.set((observation, SOSA.hasFeatureOfInterest, feature))
        tmp_graph.set((observation, SOSA.observedProperty, prop))
        tmp_graph.set((observation, SOSA.resultTime, Literal(t, datatype=XSD.dateTime)))
        return observation


def graph_store_post(url, rdftext, graph_uri=None, content_type="text/turtle"):
    """
    url is the location of the server's graph store post endpoint
    rdftext is the text to send
    graph_uri is the named graph to send this to, None for default
    """

    params = {}
    if not (graph_uri is None):
        params["graph"] = graph_uri
    headers = {}
    headers["Content-Type"] = content_type
    response = httpx.post(url, params=params, headers=headers, data=rdftext)
    response.raise_for_status()


def graph_store_get(url, graph_uri=None, content_type="application/trig"):
    """
    url is the location of the server's graph store get endpoint
    graph_uri is the named graph to get, None for default
    """

    params = {}
    if not (graph_uri is None):
        params["graph"] = graph_uri
    headers = {}
    headers["Content-Type"] = content_type
    response = httpx.get(url, params=params, headers=headers)
    response.raise_for_status()
    response_content_type = response.headers["Content-Type"]
    if not (content_type is None) and content_type != response_content_type:
        raise DBInterfaceError(
            f"Response content type ({response_content_type}) doesn't match request content type ({content_type})"
        )
    return response.text
