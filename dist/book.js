/* Reader-facing front matter and narrative order from the publisher review.
   Introduction and chapter premises are editorial source text, not an authored
   preface or substitutes for the original chapter manuscripts. */

export const introduction = {
  title: 'Dẫn nhập',
  epigraph: 'I like maths because there is always a definite answer. I like literature because there isn’t a wrong one.',
  paragraphs: [
    'Jason thích toán vì ở đó có đáp án; anh thích văn chương vì có những câu hỏi không nhất thiết phải có đáp án đúng. Anh lớn lên với những ký ức vừa dịu dàng vừa đáng sợ, rồi bước vào tuổi trưởng thành bằng niềm tin rằng mọi vấn đề đều có thể hiểu được nếu quan sát đủ kỹ, đặt đúng biến số và tìm đúng mô hình.',
    'Từ chuyện mặc quần áo, mua giày, quản lý tiền, yêu đương tới đi làm, anh liên tục tìm cách giải thích hành vi con người bằng kinh tế học, game theory, xác suất, tư duy định lượng. Anh gọi mình là một quant từ trong bản chất: người biết kiểm soát rủi ro giữa một thế giới không thể dự đoán.',
    'Độc giả không cần biết data science để đọc cuốn sách này. Mọi thuật ngữ có vai trò kể chuyện sẽ được đặt trong những trải nghiệm cụ thể.',
  ],
  source: {
    document: 'Publisher narrative review',
    section: 'I. Hồ sơ tác phẩm',
    subsections: ['Giới thiệu nội dung', 'Lời hứa dành cho độc giả'],
    kind: 'editorial introduction',
    note: 'Trích phần dẫn nhập không tiết lộ diễn biến từ hồ sơ tác phẩm; bản nguồn không có lời tựa riêng của tác giả.',
    epigraphSection: 'Trang tên sách',
    epigraphRevision: 'Opening updated to I like maths at the author’s request; the remainder follows the supplied epigraph.',
  },
};

export const parts = [
  {
    id: 1,
    key: 'model_specification',
    title: 'Những mô hình đầu tiên',
    subtitle: 'Người kể tin rằng thế giới có thể đọc được nếu ta nhận ra cấu trúc của nó.',
  },
  {
    id: 2,
    key: 'data_collection',
    title: 'Những thứ không thể đo',
    subtitle: 'Sau hệ thống lý thuyết, độc giả gặp những con người và khung cảnh thực đã nuôi dưỡng tác giả.',
  },
  {
    id: 3,
    key: 'relationship_modeling',
    title: 'Mô hình của tình yêu',
    subtitle: 'Jason xây các lý thuyết về tiếp cận và bảo vệ bản thân, trong khi các mối quan hệ riêng lẻ làm lộ những điều không lọt vào mô hình ấy.',
  },
  {
    id: 4,
    key: 'model_failure',
    title: 'Một mô hình tự chứng minh mình đúng',
    subtitle: 'Những cuộc hội thoại, tin nhắn và ghi chép công sở.',
  },
  {
    id: 5,
    key: 'under_revision',
    title: 'Những thứ bị bỏ sót',
    subtitle: 'Khi việc thắng không còn là mục tiêu, điều gì bắt đầu hiện ra?',
  },
];

export const chapterNotes = {
  '00': {
    title: 'Cơm nguội',
    summary: 'Một người trẻ vẫn ăn cơm nguội dù luôn có cơm mới nấu. Lý do dẫn về ký ức đứa trẻ giành phần cơm nguội từ bố.',
  },
  '01': {
    title: 'I Was Born a Quant',
    summary: 'Jason phân biệt tư duy dự báo kết quả với tư duy quản lý rủi ro khi kết quả không thể bảo đảm. Anh kể chuyện trưởng thành trong môi trường thiếu tính nhất quán như một lý giải cá nhân cho sự đề phòng.',
  },
  '02': {
    title: 'Expected Utility',
    summary: 'Một chàng trai tìm bug trong code nhưng không ngừng nhìn thấy đôi mắt một cô gái. Từ một mất tập trung rất người, anh chuyển sang lợi ích, chi phí, hối tiếc và lựa chọn tối ưu.',
  },
  '03': {
    title: 'Chơi để không thua',
    summary: 'Từ cảnh mạt chược của Crazy Rich Asians, Jason đọc một mối quan hệ như một game có những payoff xung đột. Anh tin kiến thức giúp tìm điểm cân bằng trong đời sống.',
  },
  '04': {
    title: 'Fashion — Be Your Own Label',
    summary: 'Một thời chạy theo NMD, Yeezy và các thần tượng hip-hop, rồi chuyển từ sưu tập món đồ đắt tiền sang trân trọng thứ mặc được lâu và có lịch sử riêng.',
  },
  '05': {
    title: 'FLOW',
    summary: 'Jason trò chuyện với flatmate về tiền, căn hộ, đi vay và sự khác nhau giữa tài sản nằm yên với dòng tiền lưu chuyển.',
  },
  '06': {
    title: 'Nút đỏ',
    summary: 'Trong một cuộc điện thoại với mẹ, Jason bấm ngắt cuộc gọi. Sau nút đỏ là nỗi sợ gắn với những giờ học, bài toán và các lời nói thời thơ ấu.',
  },
  '07': {
    title: 'Một người bạn cũ',
    summary: 'Một món đồ chơi nhỏ từ lớp mẫu giáo mở ra một tình bạn kéo dài rồi thay đổi.',
  },
  '08': {
    title: 'For Mother Russia',
    summary: 'Một người chưa từng đặt chân tới nước Nga lại mơ lặp đi lặp lại về lối mòn tuyết và ngôi nhà gỗ sáng đèn. Ký ức về ông, quy hoạch Liên Xô, game chiến tranh và những chuyến đi qua màn hình tạo nên một miền ký ức vay mượn, vừa thật vừa tưởng tượng.',
  },
  '09': {
    title: 'Metro số 5',
    summary: 'Hai đứa trẻ ngồi đối diện trên chuyến tàu tới Bastille. Từ một đoạn hội thoại nghe được, Jason tưởng tượng ra bữa tối trong gia đình chúng và thứ ánh sáng vàng của những phim cũ.',
  },
  '10': {
    title: 'Những thứ không được lưu lại',
    summary: 'Nhật ký những giấc mơ, ký ức về các nơi chưa hề đặt chân tới và nỗi băn khoăn liệu việc ghi lại có làm chúng trở nên thật.',
  },
  '11': {
    title: 'Những sự trùng hợp',
    summary: 'Những dãy giờ lặp trên iPhone, cuộc tái ngộ flatmate, một cuộc trò chuyện Việt Nam ở hiệu sách Saratoga và sách của Thích Nhất Hạnh tạo cảm giác thế giới đang gửi tín hiệu.',
  },
  '12': {
    title: 'Vỡ mộng',
    summary: 'Từ ông già Noel tới những phát hiện không dễ chịu khác, Jason kể quá trình mất dần sự đơn giản của thế giới thời bé.',
  },
  '13': {
    title: 'Những người anh em',
    summary: 'Cuộc gặp lại ông Tư, ký ức road trip xuyên Việt và nỗi nhớ một tập thể cũ có khả năng nói chuyện đến tận khuya về bất cứ thứ gì.',
  },
  '14': {
    title: 'Viết cho Sài Gòn của t',
    summary: 'Jason đến thành phố vào sinh nhật 26 tuổi, với ít tiền, khoản nợ và chưa có công việc. Grab, Masan, cầu Ba Son, những người bạn, sự thăng tiến và các cuộc chia tay tạo ra chương địa lý quan trọng nhất của cuốn sách.',
  },
  '15': {
    title: 'I Am 28 Today',
    summary: 'Một người từng nghĩ tuổi 27 là giới hạn nhìn lại lý do mình lưu ảnh, video và kỷ niệm với cả những người không còn thân.',
  },
  '16': {
    title: 'Tiểu hành tinh',
    summary: 'Một bức thư gửi cô gái được ví như ngôi sao nhỏ: non nớt, sáng rực và có con đường riêng.',
  },
  '17': {
    title: 'Three Meeting Theory',
    summary: 'Niềm tin của những đứa trẻ hopeless romantic: hai người có thể cắt nhau ba lần trước khi nhận ra nhau.',
  },
  '18': {
    title: 'Dating Algorithm',
    summary: 'Jason lên sân khấu tưởng tượng của một buổi TED Talk, định lượng sự hấp dẫn, incentive và luật chơi của dating.',
  },
  '19': {
    title: 'To Mary Jane',
    summary: 'Một lá thư chia tay: anh biết mình đang rời đi, cố giữ sự dịu dàng và đồng thời đặt một cánh cửa đóng lại.',
  },
  '20': {
    title: 'Runaway',
    summary: 'Một lần chăm người mình thương lúc ốm, những nét vẽ trên iPad, bài Runaway của Kanye và cảm giác bị người khác nhìn xuyên qua vẻ hào nhoáng. Jason nhận ra anh vừa phán xét những người chạy theo hình ảnh bề ngoài vừa đang tự đuổi theo tiền bạc, status và sự công nhận.',
  },
  '21': {
    title: 'Những hình chiếu xấu xí',
    summary: 'Jason nhận ra mình đã đem một ký ức đau đớn về mẹ áp lên phụ nữ và tình yêu như thế nào.',
  },
  '22': {
    title: 'The 23-Word Nuclear Warhead',
    summary: 'Khởi đầu từ tin nhắn, một lời đùa về video Professor Jiang, 4chan meme trong #ai-learning và một ticket từng có tiêu đề thiếu tôn trọng. Jason trả đũa bằng cách nhờ Claude nói hộ và dựng ra năm tầng “sát thương” của một câu nhắn.',
  },
  '23': {
    title: 'Better and Brighter Than Ever',
    summary: 'Từ món quà áo bóng đá từng tượng trưng cho tình bạn tới sự cay nghiệt sau khi mất lòng tin.',
  },
  '24': {
    title: 'Masterclass in Record Keeping',
    summary: 'Người từng bị phê bình về cách ghi chép trên Linear dựng một kho bằng chứng về chính ticket đó: title history, timestamps, activity log, nhiều yêu cầu tìm dữ liệu và các câu trả lời từ AI.',
  },
  '25': {
    title: 'Good Boy',
    summary: 'Jamin gửi một lời xin lỗi riêng tư, thừa nhận một số hành vi không phù hợp. Jason yêu cầu được để yên; người kia chấp nhận; Jason vẫn gửi thêm “good boy”.',
  },
  '26': {
    title: 'Negative-Sum Game',
    summary: 'Jason thử biến sự trả đũa thành một “moral mathematical model”, được AI nhắc về giới hạn dữ liệu, phạm vi phân tích và phép lịch sự tối thiểu. David nhiều lần đề nghị dừng đăng công khai; Jason tiếp tục bảo mình “chỉ làm toán”.',
  },
  '27': {
    title: 'Sharingan',
    summary: 'Đi bộ dưới những cây cổ thụ, Jason nhớ lần rời Masan hai năm trước và nhận ra lịch sử có vẻ đang lặp lại. Người tự hào sở hữu đôi mắt Sharingan nhìn được pattern ở mọi nơi lại không thấy những pattern độc hại của chính mình.',
  },
  '28': {
    title: 'Command Respect',
    summary: 'Jason kết nối nhu cầu khiến Jamin sợ với ký ức mình từng sợ người cha bộ đội và những trận đòn thời bé. David không nói bằng lý thuyết, mà bằng sự quan tâm của một người anh và lời khuyên phải tìm cách giải quyết xung đột lành mạnh hơn.',
  },
  '29': {
    title: 'Lone Wolf',
    summary: 'Jason mô tả mình lần lượt là golden retriever, con mèo khó gần rồi sói đơn độc. Nhưng các bài hát của NF khiến anh phải thú nhận rằng sự độc lập cực đoan không xóa đi nhu cầu được nắm tay ai đó.',
  },
  '30': {
    title: 'Có những thứ chỉ khi mình rời đi rồi mới nhìn thấy',
    summary: 'Ba tuần sau khi rời team, Jason nhìn thấy bức vẽ trên whiteboard vẫn còn đó. Bao thuốc, chai rượu, người đi mưa tới farewell, email từ Geoffrey và câu hỏi thăm của David trở thành những chi tiết về sự quan tâm mà anh từng bỏ sót.',
  },
  '31': {
    title: 'Lời xin lỗi',
    summary: 'Một thông điệp gửi người từng bị Jason đối xử lạnh lùng hai năm trước.',
  },
};

export const narrativeSource = {
  document: 'Publisher narrative review',
  section: 'II. Kiến trúc truyện kể',
  kind: 'editorial chapter premises',
  order: 'Prologue 00; five parts; chapters 01–31; chapter 31 as epilogue',
};
