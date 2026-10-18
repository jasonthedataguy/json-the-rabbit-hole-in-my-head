(() => {
  const modes={
    observed:{image:'dream-world-observed-v2.webp',alt:'Minh họa hai đứa trẻ cùng ván trượt trên tàu điện Paris.',title:'The real moment',label:'OBSERVED / Métro Line 5',body:'Hai đứa trẻ, giày đã sờn, một tấm ván trượt và cuộc điện thoại mà Jason chỉ hiểu lõm bõm.',note:'Màu tóc và diện mạo trong tranh là lựa chọn minh họa, không phải chi tiết được ghi trong bản thảo.'},
    imagined:{image:'dream-world-imagined-v2.webp',alt:'Minh họa một bữa tối gia đình trong căn bếp vàng ấm mà người kể tưởng tượng.',title:'Somewhere, a family dinner',label:'IMAGINED / an unseen kitchen',body:'Chuyện ở trường, cá hồi, măng tây, một bạn nữ mới chuyển đến và ánh đèn xe ngoài cửa sổ. Jason tưởng tượng những chi tiết đó; anh không biết chúng có thật hay không.',note:'Cảnh này diễn giải trí tưởng tượng của người kể, không phải bằng chứng về cuộc sống của hai đứa trẻ.'},
    afterimage:{image:'dream-world-afterimage-v2.webp',alt:'Các bức ảnh và dải phim quấn quanh khung cửa gia đình trong sắc vàng ấm.',title:'A recurring shade of yellow',label:'AFTERIMAGE / a familiar colour',body:'Tương phản thấp, chút nhiễu và ánh vàng xuất hiện trong những cảnh anh hình dung, rồi cả những bức ảnh anh chỉnh sửa về sau.',note:'Các bức ảnh và dải phim diễn giải cảm giác của người kể; chúng không phải ảnh tư liệu.'}
  };
  const image=document.getElementById('frame-img'), slider=document.getElementById('grade');
  if(!image||!slider)return;
  const base=image.getAttribute('src').slice(0,image.getAttribute('src').lastIndexOf('/')+1);
  function gradeImage(){
    const v=Number(slider.value);
    document.getElementById('grade-val').textContent=v+'%';
    slider.setAttribute('aria-valuetext',v+' phần trăm');
    image.style.filter='sepia('+(v*.009).toFixed(2)+') saturate('+(1+v*.005).toFixed(2)+') contrast('+(1.13-v*.0025).toFixed(2)+') brightness('+(1.02-v*.0005).toFixed(2)+')';
  }
  function drawMode(mode){
    const x=modes[mode];
    document.querySelectorAll('button[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.layer===mode)));
    image.src=base+x.image;image.alt=x.alt;
    for(const [id,key] of [['frame-label','label'],['layer-title','title'],['layer-body','body'],['layer-note','note']])document.getElementById(id).textContent=x[key];
    gradeImage();
  }
  document.querySelectorAll('button[data-layer]').forEach(b=>b.addEventListener('click',()=>drawMode(b.dataset.layer)));
  slider.addEventListener('input',gradeImage);
  document.getElementById('reel-reset').addEventListener('click',()=>{slider.value='55';drawMode('observed');});
  gradeImage();
})();
