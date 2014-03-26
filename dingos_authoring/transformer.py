#!/usr/bin/python2.7

import sys, datetime 
import json, whois, pytz
import importlib, uuid

from cybox.core import Observable, Observables
from cybox.common import Hash, String, Time, ToolInformation, ToolInformationList, ObjectProperties, DateTime
import cybox.utils

from stix.indicator import Indicator
from stix.campaign import Campaign, AssociatedCampaigns, Names, Name
from stix.threat_actor import ThreatActor
from stix.core import STIXPackage, STIXHeader
from stix.common import InformationSource, Confidence, Identity, Activity, DateTimeWithPrecision, StructuredText as StixStructuredText, VocabString as StixVocabString
from stix.common.identity import RelatedIdentities
from stix.common.related import RelatedCampaign
from stix.extensions.marking.tlp import TLPMarkingStructure
from stix.data_marking import Marking, MarkingSpecification
from stix.bindings.extensions.marking.tlp import TLPMarkingStructureType
import stix.utils


class stixTransformer:
    """
    Implements the transformer used to transform the JSON produced by
    the MANTIS Authoring GUI into a valid STIX document.
    """
    
    # Some defaults
    jsn = None
    namespace_name = "cert.siemens.com"
    namespace_prefix = "siemens_cert"
    stix_header = {}
    stix_indicators = []
    campaign = None
    threatactor = None
    indicators = {}
    observables = {}
    old_observable_mapping = {}
    cybox_observable_list = None

    def __init__(self, jsn):
        # Set the namespace
        # TODO: make adjustable (user dependend?)
        self.namespace = cybox.utils.Namespace(self.namespace_name, self.namespace_prefix)
        cybox.utils.set_id_namespace(self.namespace)
        stix.utils.set_id_namespace({self.namespace_name: self.namespace_prefix})

        if type(jsn) == dict:
            self.jsn = jsn
        else:
            try:
                self.jsn = json.loads(jsn)
            except:
                print 'Error parsing provided JSON'
                return None

        if not self.jsn:
            return None

        # Now process the parts
        self.__process_observables()
        self.__process_indicators()
        self.__process_campaigns()
        self.__create_stix_package()



    def __process_campaigns(self):
        """
        Processes the campaigns JSON part
        """
        try:
            campaign = self.jsn['campaign']
        except:
            print "Error. No threat campaigns passed."
            return


        try:
            threatactor = campaign['threatactor']
        except:
            print "Error. No threat actor passed."
            return

        if not campaign['name'] or not threatactor['identity_name']:
            return

        camp = Campaign()
        camp.names =  Names(Name(campaign['name']))
        camp.title = campaign['title']
        camp.description = campaign['description']
        camp.confidence = Confidence(campaign['confidence'])
        camp.handling = TLPMarkingStructure()
        camp.handling.color = campaign['handling']
        camp.information_source = InformationSource()
        camp.information_source.description = campaign['information_source']
        camp.status = StixVocabString(campaign['status'])
        afrom = Activity()
        afrom.date_time = DateTimeWithPrecision(value=campaign['activity_timestamp_from'], precision="minute")
        afrom.description = StixStructuredText('from timestamp')
        ato = Activity()
        ato.date_time = DateTimeWithPrecision(value=campaign['activity_timestamp_to'], precision="minute")
        ato.description = StixStructuredText('to timestamp')
        camp.activity = [afrom, ato]
        self.campaign = camp


        tac = ThreatActor()
        related_identities = []
        for ia in threatactor['identity_aliases'].split('\n'):
            related_identities.append(Identity(None, None, ia))
        tac.identity = Identity(None, None, threatactor['identity_name'])
        tac.identity.related_identities = RelatedIdentities(related_identities)
        tac.title = String(threatactor['title'])
        tac.description = StixStructuredText(threatactor['description'])
        tac.information_source = InformationSource()
        tac.information_source.description = threatactor['information_source']
        tac.confidence = Confidence(threatactor['confidence'])
        tac.associated_campaigns = camp

        self.threatactor = tac

        
        

    def __process_observables(self):
        """
        Processes the observables JSON part and produces a list of observables.
        """
        try:
            observables = self.jsn['observables']
        except:
            print "Error. No observables passed."
            return

        cybox_observable_dict = {}
        relations = {}


        # First collect all object relations.
        for obs in observables:
            relations[obs['observable_id']] = obs['related_observables']
            
        for obs in observables:
            object_type = obs['observable_properties']['object_type']
            try:
                im = importlib.import_module('dingos_authoring.transformer_classes.' + object_type.lower())
                cls = im.transformer_class()
                cybox_obs = cls.process(obs['observable_properties'])
            except Exception as e:
                print 'Error in module %s:' % object_type.lower(), e
                continue

            if type(cybox_obs)==list: # We have multiple objects as result. We now need to create new ids and update the relations
                old_id = obs['observable_id']
                new_ids = []
                translations = {} # used to keep track of which new __ id was translated
                for no in cybox_obs:
                    _tmp_id = '__' + str(uuid.uuid4())
                    cybox_observable_dict[_tmp_id] = no
                    new_ids.append(_tmp_id)
                    translations[_tmp_id] = old_id

                # Now find references to the old observable_id and replace with relations to the new ids.
                # Instead of manipulation the ids, we just generate a new array of relations
                    
                new_relations = {}
                for obs_id, obs_rel in relations.iteritems():
                    if obs_id==old_id: # our old object has relations to other objects
                        for ni in new_ids: # for each new key ...
                            new_relations[ni] = {}
                            for ork, orv in obs_rel.iteritems(): # ... we insert the new relations
                                if ork==old_id: # skip entries where we reference ourselfs
                                    continue
                                new_relations[ni][ork] = orv
                    else: # our old object might be referenced by another one
                        new_relations[obs_id] = {} #create old key
                        #try to find relations to our old object...
                        for ork, orv in obs_rel.iteritems():
                            if ork==old_id: # Reference to our old key...
                                for ni in new_ids: #..insert relation to each new key
                                    new_relations[obs_id][ni] = orv
                            else: #just insert. this has nothing to do with our old key
                                new_relations[obs_id][ork] = orv
                        pass
                relations = new_relations

            else: # only one object. No need to adjust relations or ids
                cybox_observable_dict[obs['observable_id']] = cybox_obs


        # Observables and relations are now processed. The only
        # thing left is to include the relation into the actual
        # objects.
        self.cybox_observable_list = []
        for obs_id, obs in cybox_observable_dict.iteritems():
            for rel_id, rel_type in relations[obs_id].iteritems():
                related_object = cybox_observable_dict[rel_id]
                if not related_object: # This might happen if a observable was not generated(because data was missing); TODO!
                    continue
                obs.add_related(related_object, rel_type, inline=False)
            if not obs_id.startswith('__'): # If this is not a generated object we keep the observable id!
                obs = Observable(obs, obs_id)
            else:
                obs = Observable(obs)
                self.old_observable_mapping[obs.id_] = translations[obs_id]

            self.cybox_observable_list.append(obs)

        return self.cybox_observable_list


    def __create_stix_indicator(self, indicator):
        """
        Helper function to create an Indicator object
        """
        stix_indicator = Indicator(indicator['indicator_id'])
        stix_indicator.title = String(indicator['indicator_title'])
        stix_indicator.description = String(indicator['indicator_description'])
        stix_indicator.confidence = Confidence(indicator['indicator_confidence'])
        stix_indicator.indicator_types = String(indicator['object_type'])
        return stix_indicator, indicator['related_observables']



    def __process_indicators(self):
        """
        Processes the indicator JSON part. Sets the stix_indicators
        which be picked up by the create_stix_package. (observables
        referenced in an indicator will be included there while loose
        observables are not inlcluded in any indicator and will just
        be appended to the package by create_stix_package)
        """
        if not self.cybox_observable_list:
            print "Error. Cybox observables not prepared"
            return

        indicators = self.jsn['indicators']
        observable_list = self.cybox_observable_list

        self.stix_indicators = []

        for indicator in indicators:
            stix_indicator, related_observables = self.__create_stix_indicator(indicator)
            for observable in observable_list:
                check_obs_id = observable.id_
                # if we have autogenerated observables, we check against the OLD id the item had before generating new ones
                if check_obs_id in self.old_observable_mapping.keys(): 
                    check_obs_id = self.old_observable_mapping[observable.id_]
                    
                if check_obs_id in related_observables:
                    obs_rel = Observable()
                    obs_rel.idref=observable.id_
                    obs_rel.id_ = None
                    stix_indicator.add_observable(obs_rel)

            self.stix_indicators.append(stix_indicator)


    def __create_stix_package(self):
        """
        Creates the STIX XML. __process_observables and __process_indicators must be called before
        """
        try:
            stix_properties = self.jsn['stix_header']
            observables = self.jsn['observables']
        except:
            print "Error. No header passed."
            return

        stix_indicators = self.stix_indicators

        stix_id_generator = stix.utils.IDGenerator(namespace={"cert.siemens.com": "siemens_cert"})
        stix_id = stix_id_generator.create_id()
        #spec = MarkingSpecificationType(idref=stix_id)
        spec = MarkingSpecification()
        spec.idref = stix_id
        #spec.set_Controlled_Structure("//node()")
        spec.controlled_structure = "//node()"
        #tlpmark = TLPMarkingStructureType()
        #tlpmark.set_color(stix_properties['stix_header_tlp'])
        tlpmark = TLPMarkingStructure()
        tlpmark.color = stix_properties['stix_header_tlp']
        #spec.set_Marking_Structure([tlpmark])
        spec.marking_structure = [tlpmark]
        stix_package = STIXPackage(indicators=stix_indicators, observables=Observables(self.cybox_observable_list), id_=stix_id, threat_actors=self.threatactor)
        stix_header = STIXHeader()
        stix_header.title = stix_properties['stix_header_title']
        stix_header.description = stix_properties['stix_header_description']
        stix_header.handling = Marking([spec])
        stix_information_source = InformationSource()
        stix_information_source.time = Time(produced_time=datetime.datetime.now(pytz.timezone('Europe/Berlin')).isoformat())
        stix_information_source.tools = ToolInformationList([ToolInformation(tool_name="Mantis Authoring GUI", tool_vendor="Siemens CERT")])
        stix_header.information_source = stix_information_source
        stix_package.stix_header = stix_header
        self.stix_package = stix_package.to_xml(ns_dict={'http://data-marking.mitre.org/Marking-1': 'stixMarking'})
        return self.stix_package



    def getStix(self):
        try:
            return self.stix_package
        except:
            return None



if __name__ == '__main__':
    fn = sys.argv[1]
    with open(fn) as fp:
        jsn = json.load(fp)

    if jsn:
        t = stixTransformer(jsn)
        print t.run()
