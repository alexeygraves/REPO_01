const tooltipElements = document.querySelectorAll('.has-tooltip');
let currentTooltip = null;

tooltipElements.forEach(function(element) {
  element.onclick = function(event) {
    event.preventDefault();

    if (currentTooltip) {
      document.body.removeChild(currentTooltip);
      currentTooltip = null;
    }

    const rect = this.getBoundingClientRect();
    const tooltip = document.createElement('div');
    tooltip.classList.add('tooltip', 'tooltip_active');
    tooltip.textContent = this.title;
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = rect.bottom + 'px';

    document.body.appendChild(tooltip);
    currentTooltip = tooltip;
  };
});

document.addEventListener('click', function(event) {
  if (currentTooltip && !event.target.classList.contains('has-tooltip')) {
    document.body.removeChild(currentTooltip);
    currentTooltip = null;
  }
});
