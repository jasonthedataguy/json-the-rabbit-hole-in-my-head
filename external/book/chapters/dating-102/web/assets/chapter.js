(() => {
  const root = document.getElementById('currency-exchange');
  if (!root) return;
  const items = {
    sketch: {title:'Những nét vẽ trên iPad', image:'02-curiosity.jpg', alt:'Hai người cùng xem những nét vẽ trên máy tính bảng.', status:'Chiếc máy đó bao nhiêu tiền?', curiosity:'Điều gì ở những nét vẽ này khiến bạn muốn vẽ tiếp?', note:'Ở lại với câu trả lời. Điều đáng biết có thể là một cách nhìn, một ký ức, hoặc niềm vui rất nhỏ.'},
    light: {title:'Ánh sáng trong căn phòng', image:'03-sketchbook.jpg', alt:'Chi tiết máy tính bảng với những nét phác họa trong ánh sáng ấm.', status:'Căn phòng này trông có sang không?', curiosity:'Bạn muốn căn phòng đem lại cảm giác gì khi trở về?', note:'Hình chỉ minh họa không khí ấm từ tranh được cung cấp. Câu hỏi xuất phát từ chi tiết decor và ánh sáng trong bài.'},
    football: {title:'Trận bóng tối thứ Năm', image:'04-football.jpg', alt:'Giày và quả bóng trên bãi cỏ trong minh họa ý niệm.', status:'Chơi với ai thì có thêm quan hệ?', curiosity:'Pha bóng nào khiến bạn vẫn muốn kể lại, dù bắp chân còn đau?', note:'Chú ý đến điều khiến người kia hào hứng và cả điều khiến họ đau. Chi tiết thứ Năm theo chữ “t5” trong bản gốc.'},
    picnic: {title:'Một chiều Chủ nhật', image:'05-picnic.jpg', alt:'Hai người ngồi trên bãi cỏ nhìn thành phố lúc hoàng hôn.', status:'Buổi hẹn này có đủ đẹp để khoe không?', curiosity:'Điều gì khiến một buổi chiều giản dị trở nên đáng nhớ với bạn?', note:'Gợi ý từ buổi picnic và thức uống bình dân trong bài. Một lời mời cùng hiểu nhau, không phải đáp án đúng cho mọi buổi hẹn.'}
  };
  let mode='curiosity', selected='sketch';
  const image=document.getElementById('object-image');
  const imageBase=image.getAttribute('src').slice(0,image.getAttribute('src').lastIndexOf('/')+1);
  function render() {
    const item=items[selected];
    root.dataset.mode=mode;
    root.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
    root.querySelectorAll('[data-object]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.object===selected)));
    image.src=imageBase+item.image;image.alt=item.alt;
    document.getElementById('object-title').textContent=item.title;
    document.getElementById('mode-label').textContent=mode==='curiosity'?'CURIOSITY / TÒ MÒ':'STATUS / ĐỊA VỊ';
    document.getElementById('object-question').textContent=item[mode];
    document.getElementById('object-note').textContent=mode==='curiosity'?item.note:'Cách nhìn này tập trung vào dấu hiệu bên ngoài. Nó chưa cho biết người kia nghĩ gì, thích gì hay cảm thấy thế nào.';
    document.getElementById('currency-token').textContent=mode==='curiosity'?'Sự chú ý':'Sự công nhận';
  }
  root.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;render();}));
  root.querySelectorAll('[data-object]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.object;render();}));
  document.getElementById('exchange-reset').addEventListener('click',()=>{mode='curiosity';selected='sketch';render();});
})();
