import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_pages():
    '''
    Returns a list of all names of encyclopedia pages.
    '''
    _, filenames = default_storage.listdir('entries')
    return list(sorted(re.sub(r'\.md$', '', filename)
                for filename in filenames if filename.endswith('.md')))


def save_page(title, content):
    '''
    Saves an encyclopedia page, given its title and Markdown
    content. If an existing page with the same title already exists,
    it is replaced.
    '''
    filename = f'entries/{title}.md'
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_page(title):
    '''
    Retrieves an encyclopedia page by its title. If no such
    page exists, the function returns None.
    '''
    try:
        f = default_storage.open(f'entries/{title}.md')
        return f.read().decode('utf-8')
    except FileNotFoundError:
        return None
