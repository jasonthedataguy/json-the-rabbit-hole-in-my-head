# 4. Expected_utility

Tôi chẳng biết tại sao, cũng chẳng biết từ khi nào mà hình ảnh của cô ấy cứ mãi lảng vảng trong đầu mình.

Tôi cố tập trung. Pha một cốc cà phê, nhét AirPods vào tai, kéo volume lên gần hết cỡ rồi dán mắt vào những dòng code, cố tìm xem vấn đề nằm ở đâu. Kiểu debugging quen thuộc: đọc lại logic, check từng biến, chạy lại, nhìn error, tự hỏi mình đã mess up ở đoạn nào. Nhưng cứ được một lúc, giữa đống syntax và những dòng chữ trên màn hình, cô ấy lại xuất hiện. Chính xác hơn là đôi mắt ấy — đôi mắt buồn, long lanh dưới ánh đèn mờ.

Đôi khi bạn không nên làm theo trái tim của mình. Tôi nói thật đấy.

Người ta hay bảo rằng you miss 100% of the shots you don't take. Rằng nếu không thử, sau này kiểu gì bạn cũng sẽ hối hận. Rằng cứ follow your heart đi, ít nhất còn biết chuyện gì xảy ra. Nghe thì rất hợp lý, nhưng bạn có chắc việc làm theo trái tim lúc nào cũng là optimal choice không?

Tôi là một đứa khá thích game theory, behavioral economics và mấy bài toán decision making, nên thay vì xử lý chuyện tình cảm như một người bình thường, tôi lại ngồi thử nhét nó vào một model.

Tạm simplify thế này nhé. Mỗi quyết định đều đem lại cho bạn một thứ gì đó và bắt bạn trả một cái giá nào đó. Gọi đơn giản là Benefit và Cost, formalize một cách thô bạo thì tôi viết Utility = Benefit - Cost. Nếu Benefit lớn hơn Cost, Utility sẽ positive. Còn khi outcome chưa chắc chắn, trên giấy người ta sẽ xét Expected Utility: giá trị của từng outcome được cân theo xác suất xảy ra của nó. Vấn đề là tôi lại chẳng biết mấy cái xác suất ấy.

Ít nhất trên giấy là vậy.

Vấn đề là con người chúng ta không có một cái bảng Excel trong đầu để nhập Benefit vào ô B2, Cost vào C2 rồi kéo công thức `=B2-C2` xuống. Tạo hóa — hoặc evolution, hoặc whatever you want to call it — cho chúng ta những công cụ đo lường kỳ quặc hơn nhiều. Tôi tạm gọi hai thứ đó là trái tim và lý trí.

Trái tim, theo cách tôi nghĩ lúc ấy, giống một cái máy đo emotional surplus.

Ví dụ đơn giản nhé. Bạn đang rất đói. Bạn vừa mua một ổ bánh mì và chuẩn bị ăn thì có một người homeless tới xin. Bây giờ bạn đứng giữa hai lựa chọn. Một là ăn ổ bánh mì và giải quyết physical need của bản thân. Hai là đưa nó cho người kia: bạn vẫn đói, nhưng đổi lại có thể nhận được một cảm giác rất khó quy đổi ra tiền — kiểu cảm giác mình vừa làm được một việc tốt, hoặc ít nhất là biết có một người khác đỡ đói hơn vì mình.

Nếu chỉ nhìn vào calories thì lựa chọn thứ nhất khá obvious. Nhưng con người không chỉ sống bằng calories. Có những lợi ích tồn tại dưới dạng cảm xúc, và theo cái model của tôi khi đó, trái tim là thứ có khả năng estimate những lợi ích kiểu này.

Tình cảm cũng thế. Bạn thích một cô gái. Trái tim gần như ngay lập tức trả về một con số rất lớn ở cột Benefit cho viễn cảnh hai người bắt đầu một mối quan hệ. Được ở cạnh cô ấy, được nói chuyện với cô ấy, được nhìn đôi mắt kia ở khoảng cách gần hơn thay vì để nó cứ hiện lên giữa màn hình code lúc hai giờ sáng. Đại loại vậy.

Nhưng Benefit mới chỉ là một nửa bài toán. Phần còn lại là Cost, và tôi nghĩ đó là công việc của lý trí.

Nếu trái tim hỏi: *mình sẽ vui đến mức nào nếu chuyện này xảy ra?* thì lý trí hỏi: *okay, nhưng nếu mình làm thế thì chuyện gì có thể xảy ra tiếp theo?*

Lý trí, theo tôi lúc ấy, thực chất là một prediction engine cho outcome.

Nghe hơi complicated nên lại lấy ví dụ hồi nhỏ cho dễ. Giả sử bạn trốn học đi chơi net và bị bố mẹ bắt được. Trên quãng đường về nhà não bạn kiểu gì cũng tự động chạy một đống simulation. Bố sẽ đánh cho một trận lên bờ xuống ruộng? Bố mẹ sẽ mắng? Tịch thu máy tính? Hay tệ hơn, họ quá chán với một đứa con ngỗ nghịch đến mức chẳng thèm nói gì nữa và Cold War 2 chính thức bắt đầu?

Bạn không biết outcome nào sẽ xảy ra, bạn chỉ có thể tưởng tượng ra một đống scenario, tự gán cho chúng những mức độ có khả năng xảy ra khác nhau, rồi cố estimate cái giá của hành động vừa làm.

Quay lại ổ bánh mì: nếu cho người homeless thì outcome khá rõ — bạn vẫn đói, và có thể phải bỏ thêm tiền mua một ổ khác. Còn nếu bạn thích một cô gái và quyết định làm gì đó về chuyện ấy thì outcome tree phức tạp hơn nhiều. Có thể mọi thứ tốt đẹp, có thể bị friendzone, có thể bị từ chối, có thể từ đó hai người awkward với nhau, cũng có thể chẳng có chuyện gì nghiêm trọng cả và vài tuần sau bạn tự hỏi tại sao lúc đó mình lại nghĩ nhiều đến thế.

Vấn đề nằm ở chỗ trong câu chuyện của tôi, chẳng ai biết xác suất của từng outcome. Bạn có thể tưởng tượng rất giỏi, nhưng imagination không phải probability distribution. Và tôi nghĩ đó là chỗ con người bắt đầu làm hỏng mấy bài toán tưởng như rất rational. Nếu mọi thứ chỉ đơn giản là Benefit trừ Cost thì đáng lẽ chúng ta phải rất giỏi decision making. Nhưng rõ ràng là không.

Bởi vì chúng ta không phải lúc nào cũng act rationally. Hoặc ít nhất, không rational theo cái nghĩa gọn gàng mà textbook thích giả định. Chúng ta bị chi phối bởi cảm xúc, thói quen, ego, fear, những thứ vừa xảy ra năm phút trước, đôi khi cả chất kích thích. Chúng ta overestimate một vài outcome, underestimate những outcome khác, hoặc đơn giản là chẳng có đủ dữ liệu để estimate cái quái gì cả.

Và quan trọng hơn, chúng ta không phải Dr. Strange. Không ai đứng trước một quyết định rồi trong một tích tắc nhìn xuyên qua hàng triệu future scenarios, chạy simulation cho từng cái, assign probability, calculate expected utility rồi bình tĩnh chọn phương án tối ưu.

Phần lớn thời gian, chúng ta chỉ đoán. Thậm chí có những lúc chúng ta còn chẳng buồn đoán.

*We don't give a fuck about the outcomes. Just do it anyway and let's see how it goes.*

Tôi thuộc loại đó, ít nhất là khá thường xuyên.

Buồn cười ở chỗ tôi có thể ngồi đọc behavioral economics, game theory, decision making process, probability, risk, đủ thứ trên đời; có thể nói thao thao bất tuyệt về rational choice hay optimization; nhưng tới lúc phải áp dụng mấy thứ đó vào chính cuộc đời mình thì performance tụt thảm hại. Kiến thức thì có thể đem lên đây bốc phét với các bạn được. Còn quyết định cá nhân thì vẫn rất nhiều lần hoạt động theo architecture cũ: nghĩ một đằng, cảm nhận một nẻo, rồi làm một thứ khác. Hoặc tệ hơn, biết mình muốn làm, nhưng lại sợ một outcome chưa chắc sẽ xảy ra đến mức không làm nữa.

Và như mọi hệ thống được build bởi một thằng developer hơi ẩu, bugs bắt đầu xuất hiện.

Có những quyết định tôi từng nghĩ là đúng rồi sau này chỉ muốn quay ngược thời gian để sửa lại. Có những việc lúc làm tôi biết luôn là không optimal nhưng vẫn làm. Có những thứ tôi hiểu cost của nó khá rõ nhưng Benefit lúc ấy lớn đến mức tôi chẳng buồn quan tâm. Và cũng có những trường hợp ngược lại: tôi sợ một outcome chưa chắc đã xảy ra đến mức bỏ qua một thứ mình thực sự muốn.

Có lẽ đó mới là vấn đề khó chịu nhất của decision making. Bạn không bao giờ được nhìn bảng kết quả của những lựa chọn mình không chọn. Không có một alternate timeline gửi email về mỗi sáng để bảo: “Này Jason, FYI, nếu hôm đó mày chọn option B thì mọi chuyện đã như thế này.” Bạn chỉ sống được với một branch duy nhất, rồi lấy dữ liệu của branch đó mà tưởng tượng về tất cả những branch còn lại.

Thế nên câu “giá như” vừa vô dụng vừa addictive.

Giá như hôm ấy mình im lặng. Giá như mình nói ra. Giá như mình ở lại. Giá như mình bỏ đi sớm hơn. Giá như mình đừng nghe trái tim. Giá như mình đừng nghĩ nhiều đến thế.

Nhưng lúc viết những dòng này, tôi vẫn chưa biết cái nào trong số đó đúng.

Tôi chỉ biết rằng tôi đã thử pha cà phê, mở nhạc thật to, nhìn chằm chằm vào màn hình và bắt mình tập trung vào một bài toán mà ít nhất error còn có stack trace.

Không hiệu quả lắm.

Vì sau tất cả những dòng về utility, Benefit, Cost, rational people và optimal choice, thứ vẫn hiện lên rõ nhất trong đầu tôi chẳng phải một phương trình nào cả.

Vẫn là đôi mắt buồn long lanh dưới ánh đèn mờ.
