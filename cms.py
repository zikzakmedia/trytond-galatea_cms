#This file is part galatea_cms module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.cache import Cache
from trytond.pyson import Eval, Not, Equal, In
from .tools import slugify

__all__ = ['Menu', 'Article', 'Block', 'Carousel', 'CarouselItem']


class Menu(ModelSQL, ModelView):
    "Menu CMS"
    __name__ = 'galatea.cms.menu'
    name = fields.Char('Name', translate=True,
        required=True, on_change=['name', 'code', 'slug'])
    code = fields.Char('Code', required=True,
        help='Internal code.')
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

    def on_change_name(self):
        res = {}
        if self.name and not self.code:
            res['code'] = slugify(self.name)
        if self.name and not self.slug:
            res['slug'] = slugify(self.name)
        return res

    @classmethod
    def validate(cls, menus):
        super(Menu, cls).validate(menus)
        cls.check_recursion(menus)

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
    name = fields.Char('Title', translate=True,
        required=True, on_change=['name', 'slug'])
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
    galatea_website = fields.Many2One('galatea.website', 'Website',
        domain=[('active', '=', True)], required=True)
    _slug_langs_cache = Cache('galatea_cms_article.slug_langs')

    @staticmethod
    def default_active():
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

    def on_change_name(self):
        res = {}
        if self.name and not self.slug:
            res['slug'] = slugify(self.name)
        return res

    @classmethod
    def copy(cls, posts, default=None):
        new_posts = []
        for post in posts:
            default['slug'] = '%s-copy' % post.slug
            new_post, = super(Article, cls).copy([post], default=default)
            new_posts.append(new_post)
        return new_posts

    @classmethod
    def delete(cls, posts):
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
    name = fields.Char('Name', required=True,
        on_change=['name', 'code', 'slug'])
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

    @staticmethod
    def default_active():
        'Return True'
        return True

    @staticmethod
    def default_type():
        'Return Image'
        return 'image'

    def on_change_name(self):
        res = {}
        if self.name and not self.code:
            res['code'] = slugify(self.name)
        return res


class Carousel(ModelSQL, ModelView):
    "Carousel CMS"
    __name__ = 'galatea.cms.carousel'
    name = fields.Char('Name', translate=True,
        required=True, on_change=['name', 'code'])
    code = fields.Char('Code', required=True,
        help='Internal code. Use characters az09')
    active = fields.Boolean('Active', select=True)
    items = fields.One2Many('galatea.cms.carousel.item', 'carousel', 'Items')

    @staticmethod
    def default_active():
        return True

    def on_change_name(self):
        res = {}
        if self.name and not self.code:
            res['code'] = slugify(self.name)
        return res


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
