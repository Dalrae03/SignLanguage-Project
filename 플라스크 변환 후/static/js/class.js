const MoveClassBut = document.querySelector(".moveClass")

const openSlideMenuButton = document.getElementById('open-menu');
const closeSlideMenuButton = document.getElementById('close-menu');
const slideMenu = document.getElementById('explain-box');

openSlideMenuButton.addEventListener('click', () => {
  slideMenu.classList.add('on');
  openSlideMenuButton.classList.add('hidden');
});

closeSlideMenuButton.addEventListener('click', () => {
  slideMenu.classList.remove('on');
  openSlideMenuButton.classList.remove('hidden');
});



function goToClass() {
    window.location.href = '/class';
}


MoveClassBut.addEventListener("click",goToClass);