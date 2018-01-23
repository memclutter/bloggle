from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError, OperationalError

from blueprints.blog.models import Blog
from common import db

blog_blueprint = Blueprint('blog', __name__, url_prefix='/blogs')


@blog_blueprint.route('', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify('Invalid payload'), 400
    
    user_guid = data.get('user_guid')
    title = data.get('title')
    about = data.get('about')
    
    try:
        blog = Blog(user_guid=user_guid,
                    title=title,
                    about=about)
        
        db.session.add(blog)
        db.session.commit()

        return jsonify(dict(blog)), 201
    
    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify(message), 500


@blog_blueprint.route('', methods=['GET'])
def index():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if (page_size <= 0) or (page <= 0):
            raise ValueError
    except ValueError:
        return jsonify('Invalid payload'), 400

    try:
        query = db.session.query(Blog)

        conditions = []

        if 'user_guid' in request.args:
            conditions.append(Blog.user_guid == request.args.get('user_guid'))

        if 'search' in request.args:
            search = request.args.get('search')
            conditions.append(or_(
                Blog.title.ilike('%' + search + '%'),
                Blog.about.ilike('%' + search + '%')
            ))

        query = query.filter(and_(*conditions))

        total_count = query.count()
        page_count = (total_count // page_size) + (1 if (total_count % page_size) != 0 else 0)
        offset = (page-1) * page_size
        limit = page_size

        query = query.offset(offset).limit(limit)

        blogs = [dict(u) for u in query.all()]
        data = dict(items=blogs,
                    page=page,
                    page_count=page_count,
                    page_size=page_size,
                    total_count=total_count)
        return jsonify(data), 200
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify(message), 500


@blog_blueprint.route('/<blog_guid>', methods=['PATCH'])
def update(blog_guid):
    data = request.get_json()
    if not data:
        return jsonify('Invalid payload'), 400

    try:
        try:
            blog = Blog.query.filter_by(guid=blog_guid).first()
            if not blog:
                raise ValueError

        except ValueError:
            return jsonify('Blog (guid=%s) does not exist' % blog_guid), 404

        blog.user_guid = data.get('user_guid', blog.user_guid)
        blog.title = data.get('title', blog.title)
        blog.about = data.get('about', blog.about)
        
        db.session.add(blog)
        db.session.commit()

        return jsonify(dict(blog)), 200

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify(message), 500


@blog_blueprint.route('/<blog_guid>', methods=['GET'])
def view(blog_guid):
    try:
        blog = Blog.query.filter_by(guid=blog_guid).first()
        if not blog:
            raise ValueError

        return jsonify(dict(blog)), 200
    except ValueError:
        return jsonify('Blog (guid=%s) does not exist' % blog_guid), 404

    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify(message), 500


@blog_blueprint.route('/<blog_guid>', methods=['DELETE'])
def delete(blog_guid):
    try:
        blog = Blog.query.filter_by(guid=blog_guid).first()
        if not blog:
            raise ValueError

        db.session.delete(blog)
        db.session.commit()

        return jsonify(), 204
    except ValueError:
        return jsonify('Blog (guid=%s) does not exist' % blog_guid), 404

    except OperationalError as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify(message), 500
