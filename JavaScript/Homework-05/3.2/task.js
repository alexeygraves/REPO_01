const links = document.querySelectorAll('.menu__link');

links.forEach(function(link) {
  link.onclick = function() {
    const subMenu = this.closest('.menu__item').querySelector('.menu_sub');
    if (subMenu) {
      document.querySelectorAll('.menu_active').forEach(function(active) {
        if (active !== subMenu) {
          active.classList.remove('menu_active');
        }
      });
      subMenu.classList.toggle('menu_active');
      return false;
    }
  };
});
