from zope.interface import implements
from transaction.interfaces import ISavepointDataManager
from transaction._transaction import AbortSavepoint
import transaction

class DataManager(object):

    implements(ISavepointDataManager)

    def __init__(self, op):
        self.op = op
        # Use the default thread transaction manager.
        self.transaction_manager = transaction.manager

    def tpc_begin(self, transaction):
        pass

    def tpc_finish(self, transaction):
        pass

    def tpc_abort(self, transaction):
        pass

    def commit(self, transaction):
        pass

    def abort(self, transaction):
        pass

    def tpc_vote(self, transaction):
        # We sync with the CMIS repo in tpc_vote.
        # This allows Zope to rollback it's transaction if something fails.
        self.op()

    def sortKey(self):
        # Try to sort last, so that we vote last.
        return "~ftw.cmissync:%d" % id(self)

    def savepoint(self):
        # Make it possible to enter a savepoint with this manager active.
        return AbortSavepoint(self, transaction.get())
