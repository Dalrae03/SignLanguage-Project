document.addEventListener("DOMContentLoaded", function() {
    if (window.location.search.includes("signup=success")) {
        var userResponse = confirm("회원가입이 완료되었습니다! 메인 페이지로 이동하시겠습니까?");
        if (userResponse) {
            window.location.href = "/";  // 사용자가 '확인'을 클릭한 경우, 메인 페이지로 이동
        } else {
            window.location.href = "/signup";
        }
    } else if(window.location.search.includes("signup=useing")){ //같은 이메일이 있는경우 처리
        alert("이미 존재하는 이메일입니다.");
        window.location.href = "/signup";
    } else if (window.location.search.includes("login=noinput")){
        alert("이메일과 비밀번호를 입력하세요!");
        window.location.href = "/login";
    } else if (window.location.search.includes("login=error")){
        alert("로그인 정보가 일치하지 않습니다.");
        window.location.href = "/login";
    } else if (window.location.search.includes("login=success")){
        alert("로그인 되었습니다.");
        window.location.href = "/";
    } else if (window.location.search.includes("nologin")){
        alert("로그인하셔야 이용하실 수 있습니다.");
        window.location.href = "/login";
    }
});

const FlashButton = document.querySelector(".moveToStudying");
const FlashButton2 = document.querySelector(".moveToStudying2");

function goToStudying() {
    window.location.href = '/studying';
}

function checkLogin() {
    // 세션에서 로그인 상태를 확인
     if (!req.session.is_logined) {
    alert('로그인 후 이용할 수 있습니다.');
    window.location.href = '/login'; // 로그인 페이지로 이동
    }}


FlashButton.addEventListener("click", goToStudying);
FlashButton2.addEventListener("click", goToStudying);


