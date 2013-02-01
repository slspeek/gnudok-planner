class NlpostcodeRouter(object):
    """
    A router to control all database operations on models in the
    nlpostcode application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read nlpostcode models go to nlpostcode_db.
        """
        if model._meta.app_label == 'nlpostalcode':
            return 'nlpostcode'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write nlpostcode models go to nlpostcode_db.
        """
        if model._meta.app_label == 'nlpostalcode':
            return 'nlpostcode'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the nlpostcode app is involved.
        """
        if obj1._meta.app_label == 'nlpostalcode' or obj2._meta.app_label == 'nlpostalcode':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the nlpostcode app only appears in the 'nlpostcode_db'
        database.
        """
        if db == 'nlpostcode':
            return model._meta.app_label == 'nlpostalcode'
        elif model._meta.app_label == 'nlpostalcode':
            return False
        return None
