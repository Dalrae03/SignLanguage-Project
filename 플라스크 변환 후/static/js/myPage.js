const goToStudyingBut = document.querySelector(".moveToStudying");
const goToLectureBut = document.querySelector(".moveToLecture")
const goToCheckBut = document.querySelector(".moveToCheck")


function goToStudying() {
    window.location.href = '/studying';
}

function goToLecture() {
    window.location.href = '/lecture';
}

function goToCheck() {
    window.location.href = '/myCheckPage';
}


goToStudyingBut.addEventListener("click", goToStudying);
goToLectureBut.addEventListener("click", goToLecture);
goToCheckBut.addEventListener("click", goToCheck);


