import dataclasses
import typing as t

from django import http, template
from wagtail.core.models import Page, Site

register = template.Library()


@dataclasses.dataclass
class MenuEntry:
    title: str
    url: str
    is_active: bool

    @classmethod
    def for_page(
        cls,
        page: Page,
        request: http.HttpRequest,
        active_path: str,
    ) -> "MenuEntry":
        url = page.get_url(request=request)
        return cls(title=str(page), url=url, is_active=(active_path.startswith(url)))


@register.inclusion_tag('tags/site_menu.html', takes_context=True)
def site_menu(context, active_path: t.Optional[str] = None):
    request = context['request']
    if active_path is None:
        active_path = request.path

    site = Site.find_for_request(request)
    home_page = site.root_page.specific

    menu_items = [
        MenuEntry(title='Homepage', url=home_page.get_url(request=request), is_active=active_path=='/')
    ] + [
        MenuEntry.for_page(page, request, active_path=active_path)
        for page in home_page.get_children().live().in_menu().specific()
    ]

    return {'menu_items': menu_items}


@dataclasses.dataclass
class PageTree:
    page: Page
    parent: t.Optional["PageTree"]
    children: t.Sequence[Page]


def _as_tree(root: Page, pages: t.Sequence[Page]) -> PageTree:
    root = PageTree(page=root, parent=None, children=[])
    current_parent = root

    for page in pages:
        while not page.is_descendant_of(current_parent.page):
            current_parent = current_parent.parent
        current_node = PageTree(page=page, parent=current_parent, children=[])
        current_parent.children.append(current_node)
        current_parent = current_node

    return root


@register.inclusion_tag('tags/table_of_contents.html', takes_context=True)
def table_of_contents(context, active_page: Page):
    request = context['request']
    site = Site.find_for_request(request)
    home_page = site.root_page

    tree_base = home_page.get_children().ancestor_of(active_page, inclusive=True).specific().get()
    descendants = tree_base.get_descendants().in_menu().live().specific()
    page_tree = _as_tree(tree_base, descendants)
    print('base:', tree_base)
    print('descendants:', list(descendants.all()))
    print('page_tree:', page_tree)

    return {'node': page_tree, 'active_page': active_page}


@register.inclusion_tag('tags/pagination.html', takes_context=True)
def paginate(context, paginator, page):
    return {
        'request': context['request'], 'paginator': paginator, 'page': page,
    }
