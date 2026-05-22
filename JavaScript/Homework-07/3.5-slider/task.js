const slider = document.querySelector('.slider');
const items = Array.from(slider.querySelectorAll('.slider__item'));
let activeIndex = 0;

function showSlide(index) {
  items[activeIndex].classList.remove('slider__item_active');
  activeIndex = (index + items.length) % items.length;
  items[activeIndex].classList.add('slider__item_active');
}

slider.querySelector('.slider__arrow_prev').onclick = function() {
  showSlide(activeIndex - 1);
};

slider.querySelector('.slider__arrow_next').onclick = function() {
  showSlide(activeIndex + 1);
};
