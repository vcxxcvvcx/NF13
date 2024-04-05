# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from sqlalchemy import text

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 모델 정의


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)  # 게시글 아이디 ->아이디는 자동생성
    title = db.Column(db.String(100), nullable=False)  # 게시글제목
    content = db.Column(db.Text, nullable=False)  # 게시글내용
    author = db.Column(db.String(100), nullable=True)  # 게시글작성자
    category = db.Column(db.String(100), nullable=True)  # 게시글 카테고리
    likes = db.Column(db.Integer, server_default=text('0'))  # 좋아요 추가하엿음

    comment = db.relationship(
        'Comment', backref=db.backref('post_comments'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    contents = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id'), nullable=False)

    # 데이터 표시

    def __repr__(self):
        return f'{self.username}: {self.contents}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # 전체 게시글 가져오기
    posts = Post.query.order_by(Post.id.desc()).paginate(
        page=request.args.get('page', 1, type=int), per_page=4)
    return render_template('index.html', posts=posts)


@app.route('/category/<category>')
def category(category):
    # 선택한 카테고리에 해당하는 게시글 가져오기
    posts = Post.query.filter_by(category=category).order_by(
        Post.id.desc()).paginate(page=request.args.get('page', 1, type=int), per_page=4)
    return render_template('index.html', posts=posts)


# @app.route('/write', methods=['GET'])
# def write():
#     # 'write.html' 페이지를 렌더링
#     return render_template('write.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':  # 이제부터 폼데이터에서 게시글의 해당정보를 받아서 객체 생성하고 저장하겠음
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author')
        category = request.form.get('category')  # 카테고리 정보를 가져옴
        new_post = Post(title=title, content=content, author=author,
                        category=category)  # 카테고리 정보 포함하여 인스턴스 생성
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('write.html')


# @app.route('/posts', methods=['POST'])
# def create_post():
#     data = request.json
#     posts.append(data)
#     # 새로운 포스트가 추가된 후 index 페이지로 리다이렉트
#     return jsonify(data), 201


# 게시글 생성 - 디비에서 포스트 요청 처리
@app.route('/posts', methods=['POST'])
def create_post():
    # 클라이언트로부터 받은 JSON 데이터를 파싱(일련의 문자열을 의미있는 토큰(token)으로 분해하고, 그 토큰들의 구조를 분석하여 의미를 이해하거나 처리하는 과정:HTML 코드를 파싱하여, 그 구조를 이해하고, 특정 요소의 내용을 추출하거나 조작할 수 있음)
    data = request.json
    new_post = Post(title=data['title'], content=data['content'],
                    # 새 게시글 객체 생성
                    author=data['author'], category=data['category'])
    db.session.add(new_post)  # 데이터베이스 세션에 추가
    db.session.commit()  # 변경사항 커밋
    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'author': new_post.author, 'category': new_post.category}), 201
# 작성자와 카테고리 추가하였음

# 게시글 조회
# @app.route('/posts', methods=['GET'])
# def get_posts():
#     return jsonify(posts)

# @app.route('/posts/<int:post_id>')
# def post_detail(post_id):
#     # post_id를 사용하여 해당 게시글 데이터 찾기
#     post = next((post for post in posts if post['id'] == post_id), None)
#     if post is None:
#         # 게시글을 찾을 수 없는 경우, 404 에러 페이지로 이동
#         return render_template('404.html'), 404
#     # 게시글이 있는 경우, 게시글 상세 페이지로 이동
#     return render_template('post_detail.html', post=post)

# 게시글 조회 - 데이터베이스에서 게시글 정보를 조회하는 방식으로 변경


@app.route('/posts', methods=['GET'])
def get_posts():  # 모든 게시글을 JSON 형식으로 반환하는 API
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author, 'category': post.category} for post in posts])


@app.route('/posts/<int:post_id>', methods=['GET'])
def post_detail(post_id):  # 특정 게시글의 상세 정보를 보여주는 뷰
    post = Post.query.get_or_404(post_id)
    comment_list = Comment.query.filter_by(post_id=post_id)
    return render_template('post_detail.html', post=post, comment_list=comment_list)


# 게시글에 아이디추가
# @app.route('/add_post', methods=['POST'])  # URL 엔드포인트도 '/add_post'로 변경
# def add_post():
#     data = request.json
#     # 게시글 ID 생성: 현재 게시글의 최대 ID에 1을 더함
#     if posts:
#         new_id = max(post['id'] for post in posts) + 1
#     else:
#         new_id = 1
#     data['id'] = new_id
#     posts.append(data)
#     # 새로운 포스트가 추가된 후 index 페이지로 리다이렉트
#     return jsonify(data), 201

# 게시글 고유 아이디 자동생성(/add_post 엔드포인트는 웹 애플리케이션에서 JSON 형식의 데이터를 받아 게시글을 데이터베이스에 추가하는 API 역할을 수행해야함)
# json 형태로 데이터를 받아 게시글을 생성하ㄹ것임
@app.route('/add_post', methods=['POST'])
def add_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')
    category = data.get('category')
    # 새 Post 인스턴스 생성
    new_post = Post(title=title, content=content,
                    author=author, category=category)
    # 데이터베이스 세션에 추가
    db.session.add(new_post)
    # 변경사항 커밋
    db.session.commit()
    # 새로운 포스트의 ID와 함께 응답
    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'author': new_post.author, 'category': new_post.category}), 201


# 게시글 삭제
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

# 게시글 수정


@app.route('/posts/<int:post_id>/update', methods=['POST'])
def update_post(post_id):
    print(post_id)
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    post.author = request.form['author']
    post.category = request.form['category']
    db.session.commit()
    return redirect(url_for('post_detail', post_id=post_id))


@app.route('/like', methods=['POST'])
def like_post():
    data = request.json
    post_id = data.get('postId')
    post = Post.query.get(post_id)
    if post:
        post.likes += 1  # 좋아요 수 증가
        db.session.commit()
        return jsonify({'message': 'Likes updated successfully'}), 200
    else:
        return jsonify({'error': 'Post not found'}), 404


# 댓글 CRUD
@app.route("/posts/<int:post_id>")
def home(post_id):
    print(post_id)
    comment_list = Comment.query.filter_by(post_id=post_id)
    print(comment_list)
    username = None
    if comment_list:
        username = comment_list[0].username
    else:
        username = None
    return render_template("post_detail.html", data=comment_list, username=username, post_id=post_id)

# 댓글 작성


@app.route("/create", methods=['POST'])
def write_comment():
    # 데이터 받아오기
    username_comment = request.form.get("username")
    contents_comment = request.form.get("contents")
    post_id = request.form.get("post_id")
    # print(post_id)

    if username_comment and contents_comment and post_id:
        new_comment = Comment(username=username_comment,
                              contents=contents_comment, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('home', post_id=post_id))
    else:
        return "Error: 작성자 이름 또는 내용이 유효하지 않습니다."


@app.route("/<int:comment_id>/edit-modal")
def edit_comment_modal(comment_id):
    print(comment_id)
    comment = Comment.query.get(comment_id)
    print(comment)
    if comment:
        return render_template("edit_comment.html", comment=comment)
    else:
        return "Comment not found", 404


@app.route("/<int:comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    print(comment_id)
    comment = Comment.query.get_or_404(comment_id)
    new_username = request.form.get("new_username")
    new_contents = request.form.get("new_contents")
    print(comment)
    if comment:
        comment.username = new_username
        comment.contents = new_contents
        db.session.commit()
        return redirect(url_for('home', post_id=comment.post_id))

    # if request.method == 'POST':
    #     data = request.json
    #     print(data)
    #     updated_username = data.get("newUsername")
    #     updated_contents = data.get("newContents")
    #     post_id = data.get("post_id")
    #     # print(updated_contents, updated_username)

    #     comment = Comment.query.get(comment_id)
    #     # print(comment)
    #     if comment:
    #         comment.username = updated_username
    #         comment.contents = updated_contents
    #         db.session.commit()

    #     return redirect(url_for('home', post_id=post_id))

    # return redirect(url_for('home', post_id=post_id))


@app.route("/<int:comment_id>/delete", methods=['POST'])
def delete_comment(comment_id):
    # print("test")
    # print(comment_id)
    comment = Comment.query.filter_by(id=1).first()
    # print(comment.post_id)
    post_id = comment.post_id

    if comment:
        # print(comment.id)
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('home', post_id=post_id))


if __name__ == '__main__':
    app.run(debug=True)
