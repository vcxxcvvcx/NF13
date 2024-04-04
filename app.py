#app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from sqlalchemy import text

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

# 모델 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #게시글 아이디 ->아이디는 자동생성
    title = db.Column(db.String(100), nullable=False) #게시글제목
    content = db.Column(db.Text, nullable=False) #게시글내용
    author = db.Column(db.String(100), nullable=True) #게시글작성자
    category = db.Column(db.String(100), nullable=True)  # 게시글 카테고리
    likes = db.Column(db.Integer, server_default=text('0'))##좋아요 추가하엿음


@app.route('/')
def index(): #메인페이지를 위한뷰함수( 홈페이지나 시작 페이지에 접근했을 때 실행되는 함수임ㅇㅇ)
    posts = Post.query.all()  # 모든 Post 객체를 데이터베이스에서 조회
    # 'index.html' 페이지를 렌더링하고 posts 데이터를 전달
    return render_template('index.html', posts=posts)

# @app.route('/write', methods=['GET'])
# def write():
#     # 'write.html' 페이지를 렌더링
#     return render_template('write.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':#이제부터 폼데이터에서 게시글의 해당정보를 받아서 객체 생성하고 저장하겠음
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author')
        category = request.form.get('category')  # 카테고리 정보를 가져옴
        new_post = Post(title=title, content=content, author=author, category=category)  # 카테고리 정보 포함하여 인스턴스 생성
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


##게시글 생성 - 디비에서 포스트 요청 처리 
@app.route('/posts', methods=['POST'])
def create_post(): 
    data = request.json # 클라이언트로부터 받은 JSON 데이터를 파싱(일련의 문자열을 의미있는 토큰(token)으로 분해하고, 그 토큰들의 구조를 분석하여 의미를 이해하거나 처리하는 과정:HTML 코드를 파싱하여, 그 구조를 이해하고, 특정 요소의 내용을 추출하거나 조작할 수 있음)
    new_post = Post(title=data['title'], content=data['content'],author=data['author'], category=data['category']) # 새 게시글 객체 생성
    db.session.add(new_post)# 데이터베이스 세션에 추가
    db.session.commit() # 변경사항 커밋
    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'author': new_post.author, 'category': new_post.category}), 201
##작성자와 카테고리 추가하였음

#게시글 조회
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

##게시글 조회 - 데이터베이스에서 게시글 정보를 조회하는 방식으로 변경
@app.route('/posts', methods=['GET'])
def get_posts():# 모든 게시글을 JSON 형식으로 반환하는 API
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author, 'category': post.category} for post in posts])

@app.route('/posts/<int:post_id>', methods=['GET'])
def post_detail(post_id):  # 특정 게시글의 상세 정보를 보여주는 뷰
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


#게시글에 아이디추가
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

##게시글 고유 아이디 자동생성(/add_post 엔드포인트는 웹 애플리케이션에서 JSON 형식의 데이터를 받아 게시글을 데이터베이스에 추가하는 API 역할을 수행해야함)
#json 형태로 데이터를 받아 게시글을 생성하ㄹ것임
@app.route('/add_post', methods=['POST'])
def add_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')  
    category = data.get('category')
    # 새 Post 인스턴스 생성
    new_post = Post(title=title, content=content, author=author, category=category)
    # 데이터베이스 세션에 추가
    db.session.add(new_post)
    # 변경사항 커밋
    db.session.commit()
    # 새로운 포스트의 ID와 함께 응답
    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'author': new_post.author, 'category': new_post.category}), 201


#게시글 삭제
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

#게시글 수정
@app.route('/posts/<int:post_id>/update', methods=['POST'])
def update_post(post_id):
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

if __name__ == '__main__':
    app.run(debug=True)
