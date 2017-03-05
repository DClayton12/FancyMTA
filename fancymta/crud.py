from fancymta import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)

@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    query_results, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        trains=query_results,
        next_page_token=next_page_token)

@crud.route('/filter_dates/', methods=['POST'])
def filter_dates():
    user_date = request.form['select_date']
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    query_results, next_page_token = get_model().filtered_date_list(filter=user_date, cursor=token)
    return render_template(
        "list.html",
        trains=query_results,
        next_page_token=next_page_token)

@crud.route('/filter_train/', methods=['POST'])
def filter_routes():
    user_train = request.form['select_train']
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    query_results, next_page_token = get_model().filtered_route_list(filter=user_train, cursor=token)
    return render_template(
        "list.html",
        trains=query_results,
        next_page_token=next_page_token)
