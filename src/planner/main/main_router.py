class MainRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen slave.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to master.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the nlpostcode app is involved.
        """
        if obj1._meta.app_label == 'main' or \
           obj2._meta.app_label == 'main':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True