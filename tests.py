from django.template.loader import add_to_builtins, Template, Context
from django.test import TestCase

from funargs import TemplateFunction as TF


class FunArgsTest(TestCase):
    def setUp(self):
        add_to_builtins('funargs.templatetags.funargs')

    def render(self, template_code, **context):
        return Template(template_code).render(Context(context))

    def testArg(self):
        f = lambda x: x + 2
        self.assertEqual(f(3), 5)
        result = self.render("{{ f|arg:3|call }}", f=TF(f))
        self.assertEqual(result, '5')

    def testMultipleArgs(self):
        f = lambda x, y: x + y
        self.assertEqual(f(2, 3), 5)
        result = self.render("{{ f|arg:2|arg:3|call }}", f=TF(f))
        self.assertEqual(result, '5')

    def testKwarg(self):
        f = 'hello {name}'.format
        self.assertEqual(f(name='frank'), 'hello frank')
        result = self.render("{{ f|kw:'name'|arg:'frank'|call }}", f=TF(f))
        self.assertEqual(result, 'hello frank')

    def testMultipleKwargs(self):
        f = '{x} {y}'.format
        self.assertEqual(f(x='foo', y='bar'), 'foo bar')
        result = self.render("{{ f|kw:'x'|arg:'foo'|kw:'y'|arg:'bar'|call }}",
                             f=TF(f))
        self.assertEqual(result, 'foo bar')

    def testVariables(self):
        f = lambda x, y: x + y
        self.assertEqual(f(2, y=3), 5)
        result = self.render("{{ f|arg:a|kw:k|arg:v|call }}",
                             f=TF(f), a=2, k='y', v=3)
        self.assertEqual(result, '5')

    def testUnpackArgs(self):
        f = lambda *args: sum(args)
        xs = [1, 2, 3]
        self.assertEqual(f(*xs), 6)
        result = self.render("{{ f|unpack_args:xs|call }}", f=TF(f), xs=xs)
        self.assertEqual(result, '6')

    def testUnpackKwargs(self):
        f = lambda x, y: x + y
        ms = dict(x=1, y=2)
        self.assertEqual(f(**ms), 3)
        result = self.render("{{ f|unpack_args:ms|call }}", f=TF(f), ms=ms)
        self.assertEqual(result, '3')

    def testMethod(self):
        class Object(object):
            def __init__(self, x):
                self.x = x

            def get(self, y):
                return self.x + y

        obj = Object('foo')
        self.assertEqual(obj.get('bar'), 'foobar')
        result = self.render("{{ obj|method:'get'|arg:'bar'|call }}", obj=obj)
        self.assertEqual(result, 'foobar')
