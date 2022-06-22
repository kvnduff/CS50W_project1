from . import util, forms
from django.shortcuts import render
from random import choice
from markdown2 import Markdown
markdowner = Markdown()


# Index
def index(request):
    return render(request, 'encyclopedia/index.html', {
        'pages': util.list_pages()
    })


# Page
def page(request, name):

    # Get pages list
    pages = util.list_pages()

    # If page exists then convert page content to html and render page
    if name in pages:
        content_converted = markdowner.convert(util.get_page(name))
        return render(request, 'encyclopedia/page.html', {
            'name': name,
            'pages': util.list_pages(),
            'content': content_converted
        })

    # If page doesn't exist then display error message
    else:
        return render(request, 'encyclopedia/page.html', {
            'name': name,
        })


# Search
def search(request):

    # Get query value and pages list
    query = request.GET.get('q')
    pages = util.list_pages()

    # Intitialize matches
    matches = []

    # If exact match then convert to HTML and render page
    if query in pages:
        content_converted = markdowner.convert(util.get_page(query))
        return render(request, 'encyclopedia/page.html', {
            'name': query,
            'pages': util.list_pages(),
            'content': content_converted
        })

    # If substring match then render search
    for page in pages:
        if query in page:
            matches.append(page)
    return render(request, 'encyclopedia/search.html', {
        'query': query,
        'matches': matches
    })


# New page
def new_page(request):

    # If method is POST
    if request.method == 'POST':

        # Get pages list, new title, and new content
        pages = util.list_pages()
        title_form = forms.TitleForm(request.POST)
        content_form = forms.ContentForm(request.POST)

        # If responses are valid then clean
        if title_form.is_valid() and content_form.is_valid():
            title_clean = title_form.cleaned_data['title']
            content_clean = content_form.cleaned_data['content']

            # If page doesn't exist then create page
            if title_clean not in pages:

                # Concatenate title to start of content with heading1 tag
                content_title = f'# {title_clean}'
                new_lines = '\n\n'
                content_concat = f'{content_title}{new_lines}{content_clean}'

                # Save, convert to HTML, and display page
                util.save_page(title_clean, content_concat)
                content_converted = markdowner.convert(
                    util.get_page(title_clean))
                return render(request, 'encyclopedia/page.html', {
                    'name': title_clean,
                    'pages': util.list_pages(),
                    'content': content_converted,
                })

            # If page exists then display error message
            if title_clean in pages:
                return render(request, 'encyclopedia/new_page.html', {
                    'title_form': forms.TitleForm(
                                      initial={'title': title_clean}),
                    'content_form': forms.ContentForm(
                                      initial={'content': content_clean}),
                    'title': title_clean,
                    'duplicate': True
                })

        # If responses are invalid then try again
        else:
            return render(request, 'encyclopedia/new_page.html', {
                'title_form': forms.TitleForm(),
                'content_form': forms.ContentForm(),
            })

    # If method is GET then collect title and content
    else:
        return render(request, 'encyclopedia/new_page.html', {
            'title_form': forms.TitleForm(),
            'content_form': forms.ContentForm(),
        })


# Edit page
def edit_page(request, name):

    # Get original page content
    content_orig = util.get_page(name)

    # If method is POST then validate response
    if request.method == 'POST':
        content_form = forms.ContentForm(request.POST)

        # If response is valid then save, convert to HTML, and display page
        if content_form.is_valid():
            content_clean = content_form.cleaned_data['content']
            util.save_page(name, content_clean)
            content_converted = markdowner.convert(util.get_page(name))
            return render(request, 'encyclopedia/page.html', {
                'name': name,
                'pages': util.list_pages(),
                'content': content_converted
            })

        # If response is invalid then try again
        else:
            return render(request, 'encyclopedia/edit_page.html', {
                'name': name,
                'pages': util.list_pages(),
                'content_form':
                    forms.ContentForm(initial={'content': content_orig})
            })

    # If method is GET then collect content
    else:
        return render(request, 'encyclopedia/edit_page.html', {
            'name': name,
            'pages': util.list_pages(),
            'content_form':
                forms.ContentForm(initial={'content': content_orig})
        })


# Random page
def random_page(request):

    # Get pages list
    pages = util.list_pages()

    # Convert page content to html and render random page
    page_selected = choice(pages)
    content = markdowner.convert(util.get_page(page_selected))
    return render(request, 'encyclopedia/page.html', {
        'name': page_selected,
        'pages': util.list_pages(),
        'content': content,
    })
