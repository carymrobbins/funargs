from django.template import Library


register = Library()


@register.filter
def arg(f, x):
    return TemplateFunction.unit(f).arg(x)


@register.filter
def kw(f, x):
    return TemplateFunction.unit(f).kw(x)


@register.filter
def unpack_args(f, xs):
    return TemplateFunction.unit(f).unpack_args(xs)


@register.filter
def call(f):
    return TemplateFunction.unit(f).call()


@register.filter
def method(obj, attr):
    return TemplateFunction(getattr(obj, attr))


class TemplateFunction(object):
    def __init__(self, f):
        self._function = f
        self._args = []
        self._kwargs = {}
        self._pending_kwarg = False
        self._kw = None

    @classmethod
    def unit(cls, f):
        if not isinstance(f, cls):
            f = cls(f)
        return f

    def arg(self, x):
        if self._pending_kwarg:
            self._kwargs[self._kw] = x
            self._pending_kwarg = False
        else:
            self._args.append(x)
        return self

    def args(self, xs):
        self._args += list(xs)
        return self

    def kw(self, x):
        self._pending_kwarg = True
        self._kw = x
        return self

    def unpack_args(self, xs):
        try:
            args = dict(**xs)
        except TypeError:
            args = list(xs)
        if isinstance(args, dict):
            self._kwargs = dict(self._kwargs, **args)
        else:
            self._args += args
        return self

    def call(self):
        return self._function(*self._args, **self._kwargs)

    def __unicode__(self):
        return unicode(self.call())
