from django.db import models


# convenience annotation, added batteries
def repository(cls):
    """
    This annotation disables delays on model objects to be written to the database.
    """

    def remove_delay_on_args(fn):

        def set_delay(args, delay):
            for arg in args:
                if type(arg) is list:
                    set_delay(arg, delay)
                elif hasattr(arg, '_delay'):
                    arg._delay = delay

        def new_fn(*args, **kwargs):
            set_delay(args, False)
            r = fn(*args, **kwargs)
            set_delay(args, True)

            return r

        return new_fn

    class WrapperCls:
        def __init__(self, *args, **kwargs):

            for required_method in ['create', 'update']:
                if required_method not in cls.__dict__:
                    raise Exception(f'Repository requires a {required_method} method')

            self.instance = cls(*args, **kwargs)

        def __getattribute__(self, s):
            try:
                x = super().__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.instance.__getattribute__(s)
            return remove_delay_on_args(x)

    return WrapperCls


class DDDModel(models.Model):  # subclass so we can do super()
    class Meta:
        abstract = True

    @classmethod
    def get_repository(cls):
        if not hasattr(cls, 'repository'):
            raise Exception(f'A repository attribute is required')

        return cls.repository(cls)

    @classmethod
    def get_manager(cls):
        cls.objects._repository = cls.get_repository()
        return cls.objects

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_kwargs_save = {}
        self._cached_kwargs_delete = {}
        self._delay = True

    def save(self, **kwargs):

        is_update = self._state.adding is False

        if self._delay:
            self._cached_kwargs_save = kwargs
            if is_update:
                self.get_repository().update(self)
            else:
                self.get_repository().create(self)
        else:
            super().save(**self._cached_kwargs_save)

    def delete(self, **kwargs):
        if self._delay:
            self._cached_kwargs_delete = kwargs
        else:
            super().delete(**self._cached_kwargs_delete)


class DDDManager(models.Manager):  # or do QuerySet

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_kwargs_bulk_create = {}
        self._delay = True
        self._repository = None

    def _check_repository_set(self):
        if self._repository is None:
            raise Exception('Manager accessed without get_manager().')

    def bulk_create(self, objs, **kwargs):

        if len(objs) == len([obj for obj in objs if obj._delay]):
            self._cached_kwargs_bulk_create = kwargs
            self._check_repository_set()
            self._repository.bulk_create(objs)
        else:
            super().bulk_create(objs, **self._cached_kwargs_bulk_create)


from utils.singleton import Singleton


class DDDRepository(metaclass=Singleton):
    def __init__(self, model):
        self.model = model
