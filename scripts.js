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
