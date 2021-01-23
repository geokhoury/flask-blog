from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from blog.models import Post, TextPost
from blog.forms import TextSearchForm

# define our blueprint
search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET', 'POST'])
def text_search():
    search_form = TextSearchForm()

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        results = TextPost.objects.search_text(keyword).order_by('$text_score')

        return render_template('search/results.html', posts=results, title="Search Results", icon="fas fa-search", keyword=keyword)

    return render_template('search/search.html', form=search_form, title="Search", icon="fas fa-search")
