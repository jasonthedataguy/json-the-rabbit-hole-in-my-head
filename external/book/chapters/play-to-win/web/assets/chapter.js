const sourceExcerpts={"15": "Ban đầu, trong cách Eleanor nhìn nhận trò chơi, việc ngăn cản Rachel dường như mang lại payoff cao hơn. Bà tin rằng nếu Rachel rời đi, Nick sẽ quay trở về với gia đình, mọi thứ lại trở về đúng vị trí của nó. Ngược lại, chấp nhận Rachel đồng nghĩa với việc bà phải nhượng bộ và từ bỏ những kỳ vọng dành cho con trai.", "22": "Nói chính xác hơn một chút, không phải vì Rachel nhả ra một quân mạt chược mà payoff thực tế của tất cả các kết quả bỗng nhiên thay đổi. Điều thay đổi là beliefs của Eleanor về Rachel, về Nick và về hậu quả của từng lựa chọn. Khi có thêm thông tin, cách bà đánh giá expected payoff của các chiến lược cũng khác đi."};

const models = {
 before: {
  stay_accept: ['Nhượng bộ?', 'Điều Eleanor tin mình mất', 'Trước cuộc đối thoại: Eleanor xem việc chấp nhận Rachel như từ bỏ những kỳ vọng dành cho con trai. Đây là cách bà nhìn nhận, không phải một điểm số khách quan.'],
  stay_block: ['Buộc phải chọn', 'Tình yêu hay gia đình?', 'Hai mục tiêu xung đột: nếu Rachel tiếp tục ở bên Nick trong khi Eleanor ngăn cản, Nick có thể bị đặt trước lựa chọn giữa hai phía.'],
  leave_accept: ['Một lựa chọn mở', 'Rachel thực sự muốn gì?', 'Tổ hợp này là một câu hỏi của mô hình: chấp nhận về phía Eleanor chưa tự nó quyết định Rachel sẽ lựa chọn thế nào.'],
  leave_block: ['Giữ được con?', 'Kỳ vọng ban đầu', 'Trước cuộc đối thoại: Eleanor tin rằng Rachel rời đi thì Nick sẽ trở về với gia đình. Chọn một ô để xem giả định.']
 },
 after: {
  stay_accept: ['Cùng giữ điều quý', 'Một khả năng hợp tác', 'Sau cuộc đối thoại: chấp nhận Rachel có thể giúp Nick vừa có người yêu vừa có gia đình. Bài viết gợi một khả năng cùng có lợi, không chứng minh một cân bằng toán học.'],
  stay_block: ['Cái giá của ngăn cản', 'Quan hệ mẹ con cũng bị tác động', 'Ngăn cản không chỉ tác động tới Rachel. Eleanor có thêm lý do để cân nhắc cái giá đối với Nick và mối quan hệ mẹ con.'],
  leave_accept: ['Tôn trọng lựa chọn', 'Chấp nhận không phải ép ở lại', 'Mô hình vẫn để ngỏ lựa chọn của Rachel. Thông tin mới giúp đọc động cơ của cô khác đi; nó không bảo đảm một kết quả.'],
  leave_block: ['Ở gần ≠ gần nhau', 'Nguy cơ xa cách và oán trách', 'Rachel rời đi chưa chắc giúp Eleanor giữ được Nick theo cách bà mong muốn. Một khoảng cách về tình cảm có thể tồn tại ngay cả khi anh ở lại.']
 }
};
let phase='before', selected='leave_block';
const phaseButtons=[...document.querySelectorAll('[data-phase]')];
const cells=[...document.querySelectorAll('[data-cell]')];
function render(){
 phaseButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.phase===phase)));
 cells.forEach(button=>{
  const content=models[phase][button.dataset.cell];
  button.querySelector('.cell-title').textContent=content[0];
  button.querySelector('small').textContent=content[1];
  button.setAttribute('aria-pressed',String(button.dataset.cell===selected));
  button.classList.toggle('changed',phase==='after');
 });
 document.querySelector('#insight').textContent=models[phase][selected][2];
 const index=phase==='before'?15:22;
 document.querySelector('#source-excerpt').textContent=sourceExcerpts[index];
 document.querySelector('#source-location').textContent='Đoạn '+(index+1)+' trong bản gốc.';
}
phaseButtons.forEach(button=>button.addEventListener('click',()=>{phase=button.dataset.phase;render()}));
cells.forEach(button=>button.addEventListener('click',()=>{selected=button.dataset.cell;render()}));

document.querySelector('#matrix-reset').addEventListener('click',()=>{phase='before';selected='leave_block';render()});
