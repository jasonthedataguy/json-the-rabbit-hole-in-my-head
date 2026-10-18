const nodes = document.querySelectorAll('[data-node]');
nodes.forEach(button => button.addEventListener('click', () => {
  nodes.forEach(node => node.setAttribute('aria-pressed', String(node === button)));
  const image = document.querySelector('#node-image');
  image.src = button.dataset.image;
  image.alt = button.dataset.title + ' — supplied illustrative scene';
  document.querySelector('#node-title').textContent = button.dataset.title;
  document.querySelector('#node-desc').textContent = button.dataset.detail;
  document.querySelector('#node-tag').textContent = button.dataset.tag;
}));
