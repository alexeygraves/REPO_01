const rotators = document.querySelectorAll('.rotator');

rotators.forEach(function(rotator) {
  const cases = Array.from(rotator.querySelectorAll('.rotator__case'));
  let activeIndex = cases.findIndex(function(c) {
    return c.classList.contains('rotator__case_active');
  });
  if (activeIndex === -1) activeIndex = 0;

  function applyActive(index) {
    cases.forEach(function(c) {
      c.classList.remove('rotator__case_active');
    });
    const current = cases[index];
    current.classList.add('rotator__case_active');
    if (current.dataset.color) {
      current.style.color = current.dataset.color;
    }
    const speed = parseInt(current.dataset.speed) || 1000;
    setTimeout(function() {
      applyActive((index + 1) % cases.length);
    }, speed);
  }

  applyActive(activeIndex);
});
