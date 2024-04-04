// scripts.js

document.addEventListener("DOMContentLoaded", function () {
  // 로그인 버튼 이벤트 리스너
  document.querySelector("#loginButton").addEventListener("click", function () {
    // 모달 창 표시
    $("#loginModal").modal("show");
  });
});

// 글쓰기 버튼 이벤트 리스너
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#writeButton").addEventListener("click", function () {
    // 글쓰기 페이지로 이동
    window.location.href = "write.html"; // 글쓰기 페이지의 URL을 여기에 입력
  });
});

function submitPost(event) {
  event.preventDefault(); // 폼 기본 제출 이벤트 방지

  const title = document.getElementById("titleInput").value;
  const author = document.getElementById("authorInput").value;
  const category = document.getElementById("categorySelect").value;
  const content = document.getElementById("contentTextarea").value;

  // FormData 객체를 사용해 파일 업로드 처리
  const formData = new FormData();
  formData.append("title", title);
  formData.append("author", author);
  formData.append("category", category);
  formData.append("content", content);
  // 여기에 파일 관련 데이터도 추가할 수 있음

  fetch("/posts", {
    method: "POST",
    body: JSON.stringify({ title, author, category, content }),
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      // 성공적으로 데이터를 보낸 후에 할 행동 (예: write.html에서 index.html로 리디렉션)
      window.location.href = "/#";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  fetch("/posts")
    .then((response) => response.json())
    .then((data) => {
      // 여기서 data를 사용해 동적으로 카드 생성 로직 구현
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

// // 자세히창 모달
// $("#editModal").on("show.bs.modal", function (event) {
//   var button = $(event.relatedTarget); // 모달을 트리거한 버튼
//   var id = button.data("id"); // data-id 속성의 값
//   var title = button.data("title"); // data-title 속성의 값
//   var content = button.data("content"); // data-content 속성의 값

//   var modal = $(this);
//   modal.find(".modal-title").text("게시글 수정: " + title);
//   modal.find(".modal-body #editTitle").val(title);
//   modal.find(".modal-body #editContent").val(content);
// });

///////////////
function submitPost(event) {
  event.preventDefault(); // 기본 폼 제출 이벤트 방지

  const title = document.getElementById("titleInput").value;
  const author = document.getElementById("authorInput").value;
  const category = document.getElementById("categorySelect").value;
  const content = document.getElementById("contentTextarea").value;

  // JSON 형식으로 데이터를 준비
  const postData = JSON.stringify({ title, author, category, content });

  fetch("/add_post", {
    // '/add_post' 엔드포인트 사용
    method: "POST",
    body: postData,
    headers: {
      "Content-Type": "application/json" // JSON 형식의 데이터임
    }
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Success:", data);
      alert("글이 성공적으로 제출되었습니다!"); // 성공 알림
      window.location.href = "/"; // 성공 후 메인 페이지로 리다이렉트
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("오류가 발생했습니다. 다시 시도해주세요."); // 실패 알림
    });
} //게시글 등록 알림을 추가하였음

function deletePost(postId) {
  if (confirm("이 게시글을 정말 삭제하시겠습니까?")) {
    fetch(`/posts/${postId}/delete`, {
      method: "POST"
      
    })
      .then((response) => {
        window.location.href = "/";
      })
      .catch((error) => console.error("Error:", error));
  }
}

//게시글 수정
function updatePost(postId) {
  const title = document.getElementById("titleInput").value;
  const author = document.getElementById("authorInput").value;
  const category = document.getElementById("categorySelect").value;
  const content = document.getElementById("contentTextarea").value;

  fetch(`/posts/${postId}/update`, {
    method: "POST",
    body: JSON.stringify({ title, author, category, content }),
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = `/posts/${postId}`; 
      }
    })
    .catch((error) => console.error("Error:", error));
}

// JavaScript 코드 for 좋아요
let likeCount = parseInt(document.getElementById('likeCount').innerText);

function increaseLikes() {
    likeCount++;
    document.getElementById('likeCount').innerText = likeCount;
    // 여기에 좋아요를 서버로 보내는 코드를 추가할 수 있습니다.
}
function increaseLikes(postId) {
  let likeCountElement = document.getElementById('likeCount' + postId);
  let likeCount = parseInt(likeCountElement.innerText);
  
  // 좋아요 수 증가
  likeCount++;
  likeCountElement.innerText = likeCount;

  // 서버로 좋아요 정보 전송
  fetch('/like', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ postId: postId }),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      // 서버 응답에 따른 추가 작업 수행
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

// 댓글 자바스크립트
function openEditModal(username, contents, commentId) {
  document.getElementById('comment_username').value = username;
  document.getElementById('comment_contents').value = contents;
  document.getElementById('comment_id').value = commentId;
  document.querySelector('#edit-comment-form').action = `/comments/${commentId}/edit`;
}

function deleteComment(formId) {
  const form = document.getElementById(formId);
  form.submit();
}

function submitEditForm() {
  const form = document.getElementById('edit-comment-form');
  const commentId = form.querySelector('input[name="comment_id"]').value;
  const newUsername = form.querySelector('input[name="new_username"]').value;
  const newContents = form.querySelector('input[name="new_contents"]').value;

  // Send a POST request to the server with the updated data
  fetch(`/comments/${commentId}/edit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ newUsername: newUsername, newContents: newContents }),
  })
    .then(response => {
      // Handle the response as needed
      if (response.ok) {
        // Reload the page to reflect the changes
        window.location.reload();
      } else {
        // Handle errors
        console.error('Failed to update comment');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

document.querySelectorAll('.edit-btn').forEach(button => {
  button.addEventListener('click', function () {
    const username = this.getAttribute('data-username');
    const contents = this.getAttribute('data-contents');
    const commentId = this.getAttribute('data-comment-id');
    openEditModal(username, contents, commentId);
  });
});