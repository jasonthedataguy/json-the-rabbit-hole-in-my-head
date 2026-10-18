document.querySelectorAll('[data-memory]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-memory]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const image = document.querySelector('#memory-image');
    image.src = button.dataset.image;
    image.alt = button.dataset.alt;
    document.querySelector('#memory-caption').textContent = button.dataset.quote;
  });
});
const result = document.querySelector('#decision-result');
const messages = {
  speak: 'Bạn chọn nói ra. Câu chuyện có thể thay đổi. Phản ứng của người ấy và con đường còn lại vẫn chưa được quan sát.',
  silent: 'Bạn chọn im lặng. Cảm xúc có thể qua đi, hoặc ở lại. Kết quả của việc nói ra vẫn nằm ngoài câu chuyện bạn đã sống.',
  reset: 'Chưa chọn một nhánh. Cả hai con đường vẫn mở; chưa có kết quả nào được quan sát.'
};
document.querySelectorAll('[data-choice]').forEach(button => {
  button.addEventListener('click', () => {
    const choice = button.dataset.choice;
    document.querySelectorAll('[data-choice]:not([data-choice="reset"])').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelectorAll('[data-node]').forEach(node => node.classList.toggle('selected', node.dataset.node === choice));
    result.textContent = messages[choice];
  });
});
