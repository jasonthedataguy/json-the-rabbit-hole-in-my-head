const choices = document.querySelectorAll('[data-memory]');
choices.forEach(button => button.addEventListener('click', () => {
  choices.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  const image = document.querySelector('#memory-img');
  image.src = button.dataset.image;
  image.alt = 'Poster-art detail: ' + button.dataset.title;
  document.querySelector('#memory-title').textContent = button.dataset.title;
  document.querySelector('#memory-desc').textContent = button.dataset.description;
}));
