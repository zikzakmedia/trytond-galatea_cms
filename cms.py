# This file is part galatea_cms module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, tree
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.cache import Cache
from trytond.pyson import Eval, Not, Equal, In
from .tools import slugify

__all__ = ['Menu', 'Article', 'Block', 'Carousel', 'CarouselItem']


class Menu(tree(), ModelSQL, ModelView):
    "Menu CMS"
    __name__ = 'galatea.cms.menu'
    name = fields.Char('Name', translate=True, required=True)
    code = fields.Char('Code', required=True,
        help='Internal code.')
    icon = fields.Char('Icon',
        help='Icon name show in menu.')
    css = fields.Char('CSS',
        help='Class CSS in menu.')
    slug = fields.Char('Slug', translate=True, required=True,
        help='Cannonical uri.')
    active = fields.Boolean('Active', select=True)
    parent = fields.Many2One("galatea.cms.menu", "Parent", select=True)
    left = fields.Integer('Left', required=True, select=True)
    right = fields.Integer('Right', required=True, select=True)
    childs = fields.One2Many('galatea.cms.menu', 'parent', 'Children')
    sequence = fields.Integer('Sequence')
    login = fields.Boolean('Login', help='Allow login users')
    manager = fields.Boolean('Manager', help='Allow manager users')
    nofollow = fields.Boolean('Nofollow',
        help='Add attribute in links to not search engines continue')

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_left():
        return 0

    @staticmethod
    def default_right():
        return 0

    @staticmethod
    def default_sequence():
        return 1

    @classmethod
    def __setup__(cls):
        super(Menu, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))
        cls._order.insert(1, ('id', 'ASC'))

    @fields.depends('name', 'code', 'slug')
    def on_change_name(self):
        if self.name:
            az09 = slugify(self.name)
            if not self.code:
                self.code = az09
            if not self.slug:
                self.slug = az09

    @classmethod
    def copy(cls, menus, default=None):
        if default is None:
            default = {}

        default['left'] = 0
        default['right'] = 0

        new_menus = []
        for menu in menus:
            default['slug'] = '%s-copy' % menu.slug
            new_menu, = super(Menu, cls).copy([menu], default=default)
            new_menus.append(new_menu)
        return new_menus


class Article(ModelSQL, ModelView):
    "Article CMS"
    __name__ = 'galatea.cms.article'
    name = fields.Char('Title', translate=True, required=True)
    slug = fields.Char('Slug', required=True, translate=True,
        help='Cannonical uri.')
    slug_langs = fields.Function(fields.Dict(None, 'Slug Langs'), 'get_slug_langs')
    uri = fields.Function(fields.Char('Uri'), 'get_uri')
    description = fields.Text('Description', required=True, translate=True,
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    metadescription = fields.Char('Meta Description', translate=True,
        help='Almost all search engines recommend it to be shorter ' \
        'than 155 characters of plain text')
    metakeywords = fields.Char('Meta Keywords',  translate=True,
        help='Separated by comma')
    metatitle = fields.Char('Meta Title',  translate=True)
    template = fields.Char('Template', required=True)
    active = fields.Boolean('Active',
        help='Dissable to not show content article.')
    visibility = fields.Selection([
            ('public','Public'),
            ('register','Register'),
            ('manager','Manager'),
            ], 'Visibility', required=True)
    galatea_website = fields.Many2One('galatea.website', 'Website',
        domain=[('active', '=', True)], required=True)
    _slug_langs_cache = Cache('galatea_cms_article.slug_langs')
    attachments = fields.One2Many('ir.attachment', 'resource', 'Attachments')
    wikimarkup = fields.Boolean('WikiMarkup',
        help='Article use wiki markups')

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_visibility():
        return 'public'

    @staticmethod
    def default_wikimarkup():
        return True

    @staticmethod
    def default_template():
        return 'cms-article.html'

    @classmethod
    def default_galatea_website(cls):
        Website = Pool().get('galatea.website')
        websites = Website.search([('active', '=', True)])
        if len(websites) == 1:
            return websites[0].id

    @classmethod
    def __setup__(cls):
        super(Article, cls).__setup__()
        cls._error_messages.update({
            'delete_articles': ('You can not delete '
                'articles because you will get error 404 NOT Found. '
                'Dissable active field.'),
            })

    @fields.depends('name', 'slug')
    def on_change_name(self):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

    @fields.depends('slug')
    def on_change_slug(self):
        if self.slug:
            self.slug = slugify(self.slug)

    @classmethod
    def create(cls, vlist):
        for values in vlist:
            values = values.copy()
            if values.get('slug'):
                slug = slugify(values.get('esale_slug'))
                values['slug'] = slug
        return super(Article, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for articles, values in zip(actions, actions):
            values = values.copy()
            if values.get('slug'):
                slug = slugify(values.get('slug'))
                values['slug'] = slug
            args.extend((articles, values))
        return super(Article, cls).write(*args)

    @classmethod
    def copy(cls, articles, default=None):
        new_articles = []
        for article in articles:
            default['slug'] = '%s-copy' % article.slug
            new_article, = super(Article, cls).copy([article], default=default)
            new_articles.append(new_article)
        return new_articles

    @classmethod
    def delete(cls, articles):
        cls.raise_user_error('delete_articles')

    def get_slug_langs(self, name):
        '''Return dict slugs by all languaes actives'''
        pool = Pool()
        Lang = pool.get('ir.lang')
        Article = pool.get('galatea.cms.article')

        article_id = self.id
        langs = Lang.search([
            ('active', '=', True),
            ('translatable', '=', True),
            ])

        slugs = {}
        for lang in langs:
            with Transaction().set_context(language=lang.code):
                article, = Article.read([article_id], ['slug'])
                slugs[lang.code] = article['slug']

        return slugs

    def get_uri(self, name):
        if self.galatea_website:
            locale = Transaction().context.get('language', 'en')
            return '%s%s/%s' % (
                self.galatea_website.uri,
                locale[:2],
                self.slug,
                )
        return ''


class Block(ModelSQL, ModelView):
    "Block CMS"
    __name__ = 'galatea.cms.block'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, help='Internal code.')
    type = fields.Selection([
        ('image', 'Image'),
        ('remote_image', 'Remote Image'),
        ('custom_code', 'Custom Code'),
        ], 'Type', required=True)
    file = fields.Many2One('galatea.static.file', 'File',
        states = {
            'required': Equal(Eval('type'), 'image'),
            'invisible': Not(Equal(Eval('type'), 'image'))
            })
    remote_image_url = fields.Char('Remote Image URL',
        states = {
            'required': Equal(Eval('type'), 'remote_image'),
            'invisible': Not(Equal(Eval('type'), 'remote_image'))
            })
    custom_code = fields.Text('Custom Code', translate=True,
        states={
            'required': Equal(Eval('type'), 'custom_code'),
            'invisible': Not(Equal(Eval('type'), 'custom_code'))
            },
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    height = fields.Integer('Height',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    width = fields.Integer('Width',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    alternative_text = fields.Char('Alternative Text',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    click_url = fields.Char('Click URL', translate=True,
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    active = fields.Boolean('Active', select=True)
    attachments = fields.One2Many('ir.attachment', 'resource', 'Attachments')
    visibility = fields.Selection([
            ('public','Public'),
            ('register','Register'),
            ('manager','Manager'),
            ], 'Visibility', required=True)

    @staticmethod
    def default_active():
        'Return True'
        return True

    @staticmethod
    def default_type():
        'Return Image'
        return 'image'

    @staticmethod
    def default_visibility():
        return 'public'

    @fields.depends('name', 'code')
    def on_change_name(self):
        if self.name and not self.code:
            self.code = slugify(self.name)

class Carousel(ModelSQL, ModelView):
    "Carousel CMS"
    __name__ = 'galatea.cms.carousel'
    name = fields.Char('Name', translate=True, required=True)
    code = fields.Char('Code', required=True,
        help='Internal code. Use characters az09')
    active = fields.Boolean('Active', select=True)
    items = fields.One2Many('galatea.cms.carousel.item', 'carousel', 'Items')

    @staticmethod
    def default_active():
        return True

    @fields.depends('name', 'code')
    def on_change_name(self):
        if self.name and not self.code:
            self.code = slugify(self.name)


class CarouselItem(ModelSQL, ModelView):
    "Carousel Item CMS"
    __name__ = 'galatea.cms.carousel.item'
    carousel = fields.Many2One("galatea.cms.carousel", "Carousel", required=True)
    name = fields.Char('Label', translate=True, required=True)
    link = fields.Char('Link', translate=True,
        help='URL absolute')
    image = fields.Char('Image', translate=True,
        help='Image with URL absolute')
    sublabel = fields.Char('Sublabel', translate=True,
        help='In case text carousel, second text')
    description = fields.Char('Description', translate=True,
        help='In cas text carousel, description text')
    html = fields.Text('HTML', translate=True,
        help='HTML formated item - Content carousel-inner')
    active = fields.Boolean('Active', select=True)
    sequence = fields.Integer('Sequence')

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_sequence():
        return 1

    @classmethod
    def __setup__(cls):
        super(CarouselItem, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))
        cls._order.insert(1, ('id', 'ASC'))
