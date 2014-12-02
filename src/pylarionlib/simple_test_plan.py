# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .document import Document

class SimpleTestPlan(Document):

    # A temporary implementation for "simple" (Pylarion-friendly) test plans.
    # TODO: Reimplement when we configure Polarion, eventually. I guess
    #       we should dedicate one or more custom fields to declare "simple"
    #       plans and their hierarchy.

    # TODO: references to test cases etc. See interface.txt for more.

    _typeId = 'testspecification'

    def __init__(self, session):

        Document.__init__(self, session)

        self.type = SimpleTestPlan._typeId

        self.text = TrackerText(session, content=_SimpleTestPlanTextEmbedding.instantiateFromParentURI(None).toText())

        self.workItemTypes = [ tcls._wiType for tcls in [ FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite ] ]


    @classmethod
    def _isConvertible(cls, suds_object):
        if not Document._isConvertible(suds_object):
            return False
        if not hasattr(suds_object, 'type'):
            return False
        if not hasattr(suds_object, 'id'):
            return False
        if suds_object.type.id != SimpleTestPlan._typeId:
            return False
        if not SimpleTestPlan._hasParentPlanEmbedding(suds_object):
            return False
        # TODO: check all the test inside are linked only
        return True


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        simpleTestPlan = SimpleTestPlan(session)
        SimpleTestPlan._mapSpecificAttributesFromSUDS(suds_object, simpleTestPlan)
        if not SimpleTestPlan._hasParentPlanEmbedding(suds_object):
            raise PylarionLibException('No valid SimpleTestPlan embedding'.format(suds_object))
        return simpleTestPlan


    def _mapToSUDS(self):
        suds_object = self.session.tracker_client.factory.create('tns3:Module')
        SimpleTestPlan._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


    def _crudCreate(self, project=None, namespace=None):
        # Work around a chicken-and-egg problem introduced by the two-steps
        # process needed to create a Document (Hint: by Polarion's design)
        tempDocument = Document(self.session)
        self._copy(tempDocument)
        tempDocument._crudCreate(project=project, namespace=namespace)
        self.puri = tempDocument.puri
        return self._crudRetrieve()


    @classmethod
    def _hasParentPlanEmbedding(cls, suds_object):
        if not hasattr(suds_object, 'homePageContent'):
            return False
        if not hasattr(suds_object.homePageContent, 'content'):
            return False
        return None != _SimpleTestPlanTextEmbedding.instantiateFromText(suds_object.homePageContent.content)


    def _getParentPlanURI(self):
        return _SimpleTestPlanTextEmbedding.getParentPlanURI(self.text.content)


    def _setParentPlanURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        self.text.content = _SimpleTestPlanTextEmbedding.setParentPlanURI(self.text.content, uri)


    def _getTestCaseURIs(self):
        # NOTE: Not persisted until _crudUpdate()
        retval = []
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        for wipid in wipids:
            wi = self.session.getWorkItemByPID(wipid, self.project)
            if wi:
                retval.append(wi.puri)
        return retval


    def _addTestCaseURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        wi = self.session.getWorkItemByPURI(uri)
        if wi.project != self.project:
            # TODO: is that really so?
            raise PylarionLibException('Work Item {} and Document {} are in different projects'.format(uri, self.puri))
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wi.pid not in wipids:
            wipids.append(wi.pid)
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, wipids)


    def _deleteTestCaseURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        wi = self.session.getWorkItemByPURI(uri)
        if wi.project != self.project:
            # not in the same project, kinda "unreachable"
            raise PylarionLibException('Work Item {} and Document {} are in different projects'.format(uri, self.puri))
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wi.pid in wipids:
            wipids.remove(wi.pid)
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, wipids)


    def _deleteAllTestCaseURIs(self):
        # NOTE: Not persisted until _crudUpdate()
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wipids:
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, [])


from .exceptions import PylarionLibException
from .test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite
from .tracker_text import TrackerText
from .embedding import _SimpleTestPlanTextEmbedding
