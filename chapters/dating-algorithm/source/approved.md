# Dating Algorithm

*18_feature_importance — VERSION B / TINDER EDITION*

let a data scientist teach you how to optimize your dating game. Its all based on a metric name SMV (sexual market value) and this value is perceived differently between genders. Suppose we have some factors: appearance, intelligence, status, money… for men the more significant factors are money/status (account for 70% of weight) while for women its mostly about appearance (90%). From that you can easily estimate your value and the girl value and the game is like you want to date up right because there is no point to date a girl lesser than you which deteriorate your value, the optimal should be a compatible between both players’ value thats the nash equilibrium n the best case since if you date a higher value girl than you its just because she settle down to you cuz she cant find any better mates eventually she gonna undermine and have no respect to you (thats the natural selection of female), and if you date a girl lesser than you you will find yourself losing (think of financial asset you should invest in high return value asset).

Welcome to my TED Talk on dating.

T vừa giải thích tình yêu bằng một scoring function, vài weights và Nash equilibrium. Một vấn đề mà nhân loại vật lộn hàng nghìn năm, t xử lý trong đúng một paragraph.

You're welcome.

Và trước khi các bạn bắt đầu hỏi dataset đâu, sample size bao nhiêu, p-value có significant không — please, hold your questions until the end.

First, a little evolutionary biology.

Có một lý do khiến tôi thích đặt những giả thuyết khó chịu về mating strategies. Robert Trivers có Parental Investment Theory: ở nhiều loài, giới đầu tư nhiều hơn vào việc tạo và nuôi con có thể chịu những áp lực lựa chọn bạn tình khác biệt. Con người không giống một mô hình sinh học tối giản, nhưng nó gợi ra một câu hỏi về incentives: khi cost và risk khác nhau, hai players có nhất thiết dùng cùng strategy không?

Các nghiên cứu cross-cultural về mate preferences của David Buss từng tìm thấy những khác biệt trung bình giữa nam và nữ trong mức độ coi trọng ngoại hình và khả năng kiếm nguồn lực. Lịch sử cũng có những xã hội cho phép đa thê, thậm chí hậu cung của hoàng đế, nơi quyền lực và cơ hội sinh sản gắn với nhau. Nhưng trung bình của một mẫu không phải tính cách của một cá nhân. Và hậu cung không phải Tinder: quyền lực chính trị, ép buộc và trật tự xã hội đều có mặt trong câu chuyện.

Harari trong Sapiens khiến tôi hứng thú với chính khoảng giao nhau giữa sinh học và trật tự do con người tạo ra. Những gì ta gọi là 'natural' đôi khi đã qua vô số lớp văn hóa và thể chế. Thú vị là tôi có thể đọc những điều ấy rồi vẫn tự tin nhét toàn bộ con người vào bốn features và hai bộ weight bịa ra trong một buổi chiều.

70% và 90% không phải evidence. They're hyperparameters. Assigned by Jason, peer-reviewed by Jason, approved by Jason.

Còn Nash equilibrium? Tôi dùng từ ấy rất hào hứng. Nhưng hai người có cùng SMV không tự động tạo ra Nash equilibrium. Đúng nghĩa game theory, equilibrium liên quan tới những chiến lược mà không ai muốn đơn phương đổi khi người kia giữ nguyên. Cái tôi đang mô tả có lẽ gần một matching problem hơn. Có lẽ ngay từ đầu tôi đã trộn game theory với một trò xếp hạng người yêu.

Okay, có một chuyện khá buồn cười ở đây. Trong lúc tôi tự nhận mình vừa giải xong dating market, một người khác đã đem gần như cùng một mô hình lên bảng. Professor Jiang Xueqin, trong bài giảng Game Theory #1: The Dating Game, lấy năm người đàn ông và năm người phụ nữ, rồi xếp mỗi bên từ 1 đến 5 dựa trên genes, wealth và status.

Nếu tất cả đều muốn người top-ranked, người đàn ông số 5 có thể muốn theo đuổi cả năm người. Nhưng lúc ấy, những players còn lại đâu có đứng yên chờ được chọn. Họ đổi strategy. Người ta có thể chọn một partner ít nổi bật hơn nhưng đáng tin cậy hơn, và cuối cùng gã số 5, vì muốn maximize mọi cơ hội, lại có nguy cơ chẳng giữ được điều mình muốn nhất.

Trong minh họa của Jiang, các cặp 5–5, 4–4, 3–3, 2–2, 1–1 tạo ra một phương án hợp tác. Ông gọi nó là Nash equilibrium. Strictly speaking, xếp hạng bằng nhau chưa đủ để chứng minh equilibrium nếu ta chưa định nghĩa đầy đủ payoffs và deviations. Nhưng cái point của ông thì hay: your best move depends on what everybody else is going to do.

Ông còn kể một bài tập trên lớp: hỏi sinh viên rằng nếu đã ba mươi tuổi và rất muốn kết hôn, họ cần điều kiện tối thiểu gì ở partner. Câu trả lời của các bạn nam và nữ trong lớp được ông dùng để bàn về incentives. Fun story, nhưng đấy là một classroom anecdote, không phải randomized controlled trial.

Có điều Professor Jiang có một cái bảng trắng. Tôi thì có Tinder.

T từng đem chính cái model ấy ra đối chiếu với một bộ data nhỏ: 10 Tinder profiles, gồm năm thằng bạn và năm cô bạn gái của t.

Five guys. Five girls. A very questionable research grant of exactly zero dollars.

T bắt đầu bằng cách chấm mỗi profile trên thang 1 đến 10. T gọi chỉ số ấy là *perceived visual SMV* — không phải giá trị của một con người, cũng chẳng phải SMV thật trong đời sống, mà là điểm hấp dẫn chủ quan mà một người xem có thể gán cho cách profile được trình bày trên app: ảnh đại diện, outfit, expression, cách chọn góc chụp, overall vibe và first impression.

Một người ngoài đời rất cuốn hút có thể lên ảnh cực kỳ nhạt nhẽo. Một người chụp ảnh đẹp chưa chắc nói chuyện thú vị. Cho nên 8/10 ở đây có nghĩa là “Jason nhìn profile này và chấm 8”, chứ không phải “người này có giá trị bằng 8”.

Scientific rigor, ladies and gentlemen.

T gắn nhãn M1 đến M5 và F1 đến F5, rồi muốn nhìn vào từng bước của funnel: bao nhiêu lượt swipe right, bao nhiêu match, tỷ lệ match trên số likes đã gửi, ai chủ động nhắn trước, bao nhiêu cuộc trò chuyện thực sự tiếp tục sau lời chào đầu tiên.

Vì sao phải tách chúng ra? Bởi vì *getting liked*, *getting matched*, và *being worth meeting again* là ba outcome khác nhau. Bạn có thể có rất nhiều matches mà chẳng có nổi một cuộc nói chuyện ra hồn. Cũng có thể có rất ít matches, nhưng mỗi cuộc trò chuyện lại đáng để tiếp tục.

Đương nhiên, N = 10 thì không ai nên dùng dataset này để công bố quy luật về toàn bộ đàn ông và phụ nữ. App còn quyết định ai được nhìn thấy profile nào, thời điểm nào; tuổi, thành phố, ảnh và cách mỗi người swipe đều là confounders. Tự tay t chấm điểm visual SMV cũng tạo thêm một layer bias khổng lồ.

Nhưng nếu coi nó như một observational case study về những người t biết, thì đây là một experiment đủ thú vị để đặt ra câu hỏi. Nó cho tôi cơ hội kiểm tra xem cái lý thuyết về attraction mà tôi vừa hùng hồn giảng có chịu nổi một chút real-world data hay không.

[EDITORIAL DATA SLOT — điền từ 10 profile thật trước khi xuất bản: Số swipe-right và matches của M1–M5, F1–F5; điểm visual SMV mỗi profile; số conversations và replies nếu có; thời gian quan sát; bối cảnh và sự đồng ý của chủ tài khoản. Chưa có kết quả được cung cấp nên không thể viết kết luận trung thực.]

T cũng đọc một nghiên cứu field experiment trên Tinder với 3.600 profile evaluations: trong mẫu nghiên cứu ấy, phụ nữ có xu hướng chọn lọc hơn và quan tâm đến trình độ học vấn của nam giới; nghiên cứu không tìm thấy bằng chứng đàn ông né tránh những phụ nữ có học vấn cao. Nói cách khác, đời thực có một vài pattern đáng nghiên cứu, nhưng nó chẳng ngoan ngoãn biến thành hai con số 70% và 90% của tôi.

That's the difference between a model you like and a model the data actually supports.

Dù kết quả của mười profile kia như thế nào, có một thứ đã rõ ngay từ lúc thiết kế nghiên cứu: tôi đang đo *profile performance*, không phải giá trị của con người, và càng không phải chất lượng của một relationship.

Nhưng thôi, giả sử bạn tạm chấp nhận premise của tôi. Dating market có players, preferences, perceived values và trade-offs. Vậy tối ưu thứ đầu tiên mà bạn đo được: ngân sách cho một buổi hẹn.

Đơn giản mà đúng k, vậy nên để optimize cho cái ví tiền của b, look at the girl và định giá cái nhan sắc đó đáng giá để b chi bao nhiêu tiền cho bữa tối (1tr, 3tr, 10tr…) nhan sắc càng cao thì khi chi tiền b càng cảm thấy xứng đáng believe me.

Tôi từng nói với một người bạn rằng mình hoàn toàn có thể rủ một cô gái đi chơi. Nó hỏi, bằng cái giọng của người không biết tôi tự tin đến mức nào:

“Are you sure?”

“Absolutely.”

“Sao mày nghĩ cô ấy sẽ đồng ý?”

“Why not?”

“Không, tao đang hỏi tại sao cô ấy muốn đi chơi với mày?”

“Yeah. Why not? That’s my answer.”

Tôi giải thích cho nó. Cô ấy có một bữa tối được trả tiền, có người nghe cô ấy yapping cả buổi, rồi còn được hang out với một người như tôi. I'm funny, you know.

“À, còn được đi với một thằng đẹp trai nữa nhỉ?”

“Exactly! You got it now.”

Tôi nói bằng vẻ mặt như vừa đặt dấu chấm cuối cùng cho một proof. I know it sounds fuckboy. But that's Jason.

Nhiều lúc câu hỏi thú vị hơn câu trả lời. Nó hỏi *why would she say yes?* — tìm demand, tìm bằng chứng cho việc cô ấy có hứng thú với tôi. Tôi hỏi *why would she say no?* — tìm friction, tìm những thứ làm một lời mời trở nên bất tiện, rủi ro hoặc khó xử.

Nếu xa quá, chọn địa điểm khác. Nếu ngại mất tiền, dinner is on me. Nếu sợ một buổi tối nhạt nhẽo, tôi có thể chủ động trò chuyện và hỏi cô ấy muốn kể gì. Tư duy của tôi là remove blockers trước khi nghĩ đến adding features.

Nhưng một lời mời không có obstacles vẫn có thể bị từ chối. Vì friend tôi hỏi một câu mà tôi không trả lời: cô ấy có muốn dành buổi tối ấy với tôi không? Nó đang giải bài toán demand validation, còn tôi đang giải bài toán conversion optimization. Hai lời giải không triệt tiêu nhau. Chúng chỉ bắt đầu bằng hai unknowns khác nhau.

Dù vậy, tôi vẫn bắt đầu bài giảng thứ hai: treat dating like a data pipeline.

Job 01 là first date. Input gồm hai người chưa hiểu nhau đủ, một bữa tối, và nhiều uncertainty. Success không phải 'tôi đã làm cô ấy đồng ý'. Success là cả hai có một buổi tối tử tế và đều muốn gặp lại.

Job 01 successful? Trigger Job 02: cà phê, phim, hoặc đi dạo. Job 02 successful? Trigger Job 03. Cứ thế. Don't overengineer your wedding before finishing the first dinner. Và nếu một người không muốn tiếp tục, đó không phải transient error để mình retry đến sáng. Pipeline ends.

Tôi thích mô hình này vì nó cho phép cập nhật dựa trên observation thay vì dự đoán một cái future rất xa từ vài bức hình. Người ta có thể nói mình thích người giàu, người đẹp, người thông minh. Nhưng lúc hai người thực sự gặp nhau, chemistry không ngoan ngoãn đi theo những features ấy. Nghiên cứu speed-dating của Eastwick và Finkel cũng cho thấy sự khác biệt giữa những gì người ta tuyên bố mình muốn và điều dự đoán sự hấp dẫn khi gặp thật.

Nói cách khác, cái model mở đầu chương này có thể là một bộ prior khá ngạo mạn. Bữa tối đầu tiên mới cho tôi dữ liệu. Và có khi dữ liệu ấy không chỉ giúp tôi hiểu cô gái hơn, mà còn khiến tôi phát hiện mình chẳng hiểu rõ preferences của chính mình.

Tôi từng tưởng mình tối ưu để date up. Nhưng càng nghĩ, tôi càng nghi ngờ cái khái niệm up ấy. Một người có thể rất đẹp, rất có status, rất high-value trong mắt đám đông, mà khi ngồi cạnh nhau tôi vẫn thấy chẳng có gì để kể. Một người khác có thể khiến tôi muốn kéo dài cuộc nói chuyện cho đến lúc quán đóng cửa.

Vì vậy, sau cả đống biology, history, game theory và product analytics, đây mới là phần t tự nhận thấy mình quan tâm khi thực sự đi tìm một mối quan hệ:

Nhưng đó là game, còn relationship thì khác trọng số kia tuỳ thuộc vào preference của b. Với t thì t cx chả cần cái nhan sắc trên trời (nhưng đương nhiên vẫn phải xinh r lol), t quan trọng hơn là cái trí tuệ của cô gái kia, liệu cô ta có thể ngồi tiếp chuyện t về philosophy, science, conspiracy theory… hay không cái đó mới quan trọng
