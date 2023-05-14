function closeMenu() {
    const menu = document.querySelector(".header__menu");
    const hamburger = document.querySelector(".hamburger");
    menu.classList.remove('header__menu--open');
    hamburger.classList.remove('hamburger--menu-open');
    document.body.classList.remove('body--menu-open');
  }
  