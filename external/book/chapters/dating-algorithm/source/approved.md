Let a data scientist teach you how to optimize your dating game.

It's all based on a metric called SMV (Sexual Market Value), and this value is perceived differently between genders.

Suppose we have a few factors: appearance, intelligence, status, money… For men, I'd argue that money and status account for 70% of the total weight, while for women, appearance alone accounts for 90%.

From there, you can easily estimate your value and the girl's value. And the game is simple: you want to date up, right?

I mean, why would you date a girl with a lower SMV than yours? You're basically downgrading your own position in the dating market. Think of it like investing in a financial asset. Why would you allocate your resources to a lower-return investment when you could get a better one?

But here's the catch.

If you date a girl whose perceived value is significantly higher than yours, there's a possibility she's only settling for you because she couldn't find a better option. And if that's the case, she might eventually start to undermine you, lose respect for you, or constantly compare you with the alternatives she thinks she deserves.

That's my rather brutal interpretation of female mate selection.

So what's the optimal strategy?

Find someone whose perceived value is roughly equivalent to yours. Neither player has a strong incentive to seek a better alternative, and both are getting a fair deal.

That's what I called Nash equilibrium.

Simple as that.

Welcome to my TED Talk on dating.

T vừa giải thích tình yêu bằng một scoring function, vài weights và Nash equilibrium. Một vấn đề mà nhân loại vật lộn hàng nghìn năm, t xử lý trong đúng một paragraph.

You're welcome.

Và trước khi các bạn bắt đầu hỏi 70% và 90% kia đến từ đâu, nguồn dataset nào, sample size bao nhiêu, p-value có significant không — please, hold your questions until the end.

First, a little evolutionary biology.

Có một lý do khiến tôi thích đặt những giả thuyết khó chịu về mating strategies. Robert Trivers có Parental Investment Theory: ở nhiều loài, giới đầu tư nhiều hơn vào việc tạo và nuôi con có thể chịu những áp lực lựa chọn bạn tình khác biệt. Con người không giống một mô hình sinh học tối giản, nhưng nó gợi ra một câu hỏi về incentives: khi cost và risk khác nhau, hai players có nhất thiết dùng cùng strategy không?

Các nghiên cứu cross-cultural về mate preferences của David Buss từng tìm thấy những khác biệt trung bình giữa nam và nữ trong mức độ coi trọng ngoại hình và khả năng kiếm nguồn lực. Lịch sử cũng có những xã hội cho phép đa thê, thậm chí hậu cung của hoàng đế, nơi quyền lực và cơ hội sinh sản gắn với nhau. Nhưng trung bình của một mẫu không phải tính cách của một cá nhân. Và hậu cung không phải Tinder: quyền lực chính trị, ép buộc và trật tự xã hội đều có mặt trong câu chuyện.

Harari trong Sapiens khiến tôi hứng thú với chính khoảng giao nhau giữa sinh học và trật tự do con người tạo ra. Những gì ta gọi là 'natural' đôi khi đã qua vô số lớp văn hóa và thể chế. Thú vị là tôi có thể đọc những điều ấy rồi vẫn tự tin nhét toàn bộ con người vào bốn features và hai bộ weight bịa ra trong một buổi chiều.

70% và 90% không phải evidence. They're hyperparameters. Assigned by Jason, peer-reviewed by Jason, approved by Jason.

Còn Nash equilibrium? Tôi dùng từ ấy rất hào hứng. Nhưng hai người có cùng SMV không tự động tạo ra Nash equilibrium. Đúng nghĩa game theory, equilibrium liên quan tới những chiến lược mà không ai muốn đơn phương đổi khi người kia giữ nguyên. Cái tôi đang mô tả có lẽ gần một matching problem hơn. Có lẽ ngay từ đầu tôi đã trộn game theory với một trò xếp hạng người yêu.

## The Dating Game

Okay, có một chuyện khá buồn cười ở đây. Trong lúc tôi tự nhận mình vừa giải xong dating market, một người khác đã đem gần như cùng một mô hình lên bảng. Professor Jiang Xueqin, trong bài giảng Game Theory #1: The Dating Game, lấy năm người đàn ông và năm người phụ nữ, rồi xếp mỗi bên từ 1 đến 5 dựa trên genes, wealth và status.

Nếu tất cả đều muốn người top-ranked, người đàn ông số 5 có thể muốn theo đuổi cả năm người. Nhưng lúc ấy, những players còn lại đâu có đứng yên chờ được chọn. Họ đổi strategy. Người ta có thể chọn một partner ít nổi bật hơn nhưng đáng tin cậy hơn, và cuối cùng gã số 5, vì muốn maximize mọi cơ hội, lại có nguy cơ chẳng giữ được điều mình muốn nhất.

Trong minh họa của Jiang, các cặp 5–5, 4–4, 3–3, 2–2, 1–1 tạo ra một phương án hợp tác. Ông gọi nó là Nash equilibrium. Strictly speaking, xếp hạng bằng nhau chưa đủ để chứng minh equilibrium nếu ta chưa định nghĩa đầy đủ payoffs và deviations. Nhưng cái point của ông thì hay: your best move depends on what everybody else is going to do.

Ông còn kể một bài tập trên lớp: hỏi sinh viên rằng nếu đã ba mươi tuổi và rất muốn kết hôn, họ cần điều kiện tối thiểu gì ở partner. Câu trả lời của các bạn nam và nữ trong lớp được ông dùng để bàn về incentives. Fun story, nhưng đấy là một classroom anecdote, không phải randomized controlled trial.

Có điều Professor Jiang có một cái bảng trắng. Jason thì có Tinder.

## The Tinder Experiment

T từng đem chính cái model ấy ra đối chiếu với một bộ data nhỏ: 10 Tinder profiles, gồm năm thằng bạn và năm cô bạn gái của t.

Five guys. Five girls. A very questionable research grant of exactly zero dollars.

T bắt đầu bằng cách chấm mỗi profile trên thang 1 đến 10. T gọi chỉ số ấy là perceived visual SMV — không phải giá trị của một con người, cũng chẳng phải SMV thật trong đời sống, mà là điểm hấp dẫn chủ quan mà một người xem có thể gán cho cách profile được trình bày trên app: ảnh đại diện, outfit, expression, cách chọn góc chụp, overall vibe và first impression.

Một người ngoài đời rất cuốn hút có thể lên ảnh cực kỳ nhạt nhẽo. Một người chụp ảnh đẹp chưa chắc nói chuyện thú vị. Cho nên 8/10 ở đây có nghĩa là “Jason nhìn profile này và chấm 8”, chứ không phải “người này có giá trị bằng 8”.

Scientific rigor, ladies and gentlemen.

T gắn nhãn M1 đến M5 và F1 đến F5, rồi muốn nhìn vào từng bước của funnel: bao nhiêu lượt swipe right, bao nhiêu match, tỷ lệ match trên số likes đã gửi, ai chủ động nhắn trước, bao nhiêu cuộc trò chuyện thực sự tiếp tục sau lời chào đầu tiên.

Vì sao phải tách chúng ra? Bởi vì getting liked, getting matched, và being worth meeting again là ba outcome khác nhau. Bạn có thể có rất nhiều matches mà chẳng có nổi một cuộc nói chuyện ra hồn. Cũng có thể có rất ít matches, nhưng mỗi cuộc trò chuyện lại đáng để tiếp tục.

Đương nhiên, N = 10 là một sample size đáng xấu hổ nếu muốn generalize cho toàn bộ dating market, và không ai có thể dùng dataset này để công bố quy luật về toàn bộ đàn ông và phụ nữ. Chưa kể Tinder algorithm còn quyết định profile nào được hiển thị cho ai, vào thời điểm nào. Tuổi, địa điểm, hình ảnh và cách mỗi người swipe đều có thể là confounding variables. Cái perceived SMV score lại còn do chính t chấm. Biased as hell.

Nhưng nếu coi nó như một observational case study về những người t biết, thì đây là một experiment đủ thú vị để đặt ra câu hỏi. Nó cho tôi cơ hội kiểm tra xem cái lý thuyết về attraction mà tôi vừa hùng hồn giảng có chịu nổi một chút real-world data hay không.

T cũng đọc một nghiên cứu field experiment trên Tinder với 3.600 profile evaluations: trong mẫu nghiên cứu ấy, phụ nữ có xu hướng chọn lọc hơn và quan tâm đến trình độ học vấn của nam giới; nghiên cứu không tìm thấy bằng chứng đàn ông né tránh những phụ nữ có học vấn cao. Nói cách khác, đời thực có một vài pattern đáng nghiên cứu, nhưng nó chẳng ngoan ngoãn biến thành hai con số 70% và 90% của tôi.

That's the difference between a model you like and a model the data actually supports.

Nhưng sau Tinder, t lại có thêm một câu hỏi.

Giả sử bạn đã match với một cô gái. Giả sử cô ấy cũng có một chút interest với bạn.

How much effort should you actually invest to make her like you?

## The Marginal Cost of Attraction

Okay, let's talk about diminishing marginal returns. T nghĩ có một thứ khá thú vị về dating mà mọi người thường overlook.

Giả sử t build một logistic regression model để predict liệu một cô gái có thích bạn hay không.

Outcome được define rất đơn giản:

Y = 1: She likes you.

Y = 0: She doesn't.

Đương nhiên attraction ngoài đời là cả một spectrum, chứ chẳng có cái switch on/off nào trong đầu con người. Nhưng vì t đang muốn giải một binary classification problem nên cứ tạm simplify nó như vậy.

T sử dụng một sigmoid function để estimate probability của outcome.

P(Y = 1) = 1 / (1 + e^(-z))

Trong đó z là một weighted combination của những features ảnh hưởng tới attraction.

Bây giờ thử đơn giản hóa model thêm một chút.

T đặt effort invested lên trục X, bao gồm time, money, attention và emotional investment mà bạn bỏ ra để theo đuổi một cô gái.

Trục Y là probability that she likes you.

Đương nhiên, đây mới chỉ là một hypothetical model, không thể đơn giản cộng một triệu tiền ăn tối với hai tiếng nhắn tin thành một metric được. Và effort chưa chắc đã có positive effect trong mọi trường hợp.

Nhưng giả sử chúng ta đã normalize được effort thành một index, và trong khoảng đang xét, tăng effort giúp tăng attraction probability, thì sigmoid có một property rất thú vị.

Diminishing marginal returns.

Khi probability còn rất thấp, thêm một chút effort có thể chẳng thay đổi được bao nhiêu.

Khi probability đã rất cao, bạn cũng chẳng nhận được bao nhiêu marginal gain từ việc tiếp tục tăng investment.

Sensitivity lớn nhất xuất hiện ở vùng giữa, gần decision boundary.

Bây giờ thử xem một ví dụ nhé.

Giả sử có một cô gái đã rất thích bạn từ trước. Attraction probability trong cái hypothetical model của t đang là 90%.

Bạn đưa cô ấy đi ăn một bữa tối hai triệu.

Maybe it goes up to 92%.

Bạn mua thêm một bó hoa.

Maybe 93%.

Rồi bạn book thêm một nhà hàng fine dining năm triệu, chuẩn bị một outfit chỉn chu, dành cả ngày lên kế hoạch cho buổi hẹn.

Maybe 94%.

Đây là những con số t bịa ra để illustrate thôi, chứ không phải calibrated probabilities nhé.

But you get the idea.

You're already on the right side of the sigmoid.

Bỏ thêm rất nhiều resources chưa chắc tạo ra một improvement tương xứng trong probability.

Và có khi bạn chẳng cần một bữa tối đắt tiền nào cả.

T lấy một ví dụ khá buồn cười.

Giả sử có một cô gái đã rất thích bạn. Một hôm cô ấy muốn qua nhà chơi, và bạn nhắn:

"Hey, on your way here, can you grab us some pizza?"

Cô ấy có thể vui vẻ đáp lại:

"Hahaha, you're funny. What pizza do you want?"

Rồi hai người ngồi ăn pizza trên sofa, xem một bộ phim, kể vài câu chuyện ngớ ngẩn, và có khi đó lại là một buổi tối vui hơn bất cứ cái fine dining restaurant nào.

Bây giờ tưởng tượng bạn nói đúng câu ấy với một cô gái chẳng hứng thú gì với mình.

"Wait, you're inviting me over and asking me to buy you dinner?"

Same guy. Same request. Completely different interpretation.

Tất nhiên cái pizza này không phải một statistical test. Một cô gái có thể không mua pizza đơn giản vì cô ấy bận, không thích pizza, hoặc thấy việc được nhờ mua đồ chẳng liên quan gì tới chuyện mình thích ai.

Nhưng có một point mà t thấy khá hay.

Khi đã có attraction, người ta có thể interpret những hành động của đối phương theo một hướng tích cực hơn.

Một câu đùa nhạt cũng có thể trở nên funny. Một hành động bình thường cũng có thể trở nên đáng yêu.

Và đôi khi, chính việc được làm điều gì đó cho người mình thích cũng khiến bản thân cảm thấy vui.

T muốn gọi đây là một dạng conditional perceived value.

Giá trị mà người ta gán cho một interaction không chỉ phụ thuộc vào action ấy, mà còn phụ thuộc vào prior attraction họ đã có với bạn.

Nói cách khác, t không nghĩ dating là một cái auction, nơi thằng nào chịu chi nhiều nhất thì thắng.

If she's already into you, you don't have to keep raising your bid.

Ngược lại, nếu cô ấy không có chút interest nào từ đầu, bạn cũng không thể assume rằng cứ tăng spending thì sẽ eventually cross được decision boundary.

Một bữa tối mười triệu không tự nhiên biến một người không thích bạn thành một người thích bạn.

Money can buy dinner.

It can't guarantee chemistry.

Và từ đó, t bắt đầu nghĩ tới một theory khác.

Nếu adding effort không nhất thiết tăng attraction, vậy reducing effort có thể khiến mình trở nên attractive hơn hay không?

## The Economics of Attention

Let's talk about asset pricing.

Trong financial market, giá một asset không chỉ phụ thuộc vào intrinsic value, mà còn chịu ảnh hưởng của supply, demand, liquidity và expectations.

Tất nhiên, con người không phải financial assets. Nhưng thử tạm dùng cái analogy ấy để model perceived attention.

Suppose your attention is an asset.

Và giả sử bạn có một lượng thời gian, energy và emotional capacity hữu hạn để phân bổ cho những người khác nhau.

Một thằng lúc nào cũng available, luôn nhắn trước, luôn chủ động lên kế hoạch, thậm chí sẵn sàng cancel những dự định của riêng mình để gặp một cô gái, đang gửi đi một signal rằng attention của nó rất dễ có được.

Trong khi một thằng khác có công việc, hobbies, bạn bè và một cuộc sống riêng đủ thú vị thì không phải lúc nào cũng available.

Same attention. Different scarcity.

Vậy có phải attention của thằng thứ hai sẽ được perceived là valuable hơn?

Maybe.

Và đây là lúc t nghĩ tới một strategy mà chắc nhiều người từng nghe.

Artificial scarcity.

Giả sử bạn thích một cô gái, nhưng thay vì thể hiện interest, bạn cố tình không nhắn trước, không chủ động gặp mặt, thậm chí tỏ ra indifferent.

Mục đích rất đơn giản.

Bạn muốn cô ấy nghĩ rằng attention của mình là một thứ scarce resource, và muốn có được nó thì cô ấy phải bỏ effort.

Basically, reduce supply to increase perceived price.

Economics 101.

Pretty smart, right?

Điều buồn cười là psychology thực sự có một vài nghiên cứu khiến cái theory này nghe không hoàn toàn vô lý.

Năm 2011, Whitchurch và cộng sự thực hiện một experiment, trong đó những nữ sinh viên xem Facebook profiles của một số chàng trai được cho là đã xem profile của họ.

Một nhóm được nói rằng những chàng trai ấy rất thích mình. Một nhóm khác được nói rằng họ chỉ thích ở mức trung bình. Nhóm cuối cùng thì không biết chính xác những chàng trai ấy thích mình nhiều hay vừa phải.

Guess what?

Trong experiment ấy, nhóm uncertain báo cáo mức attraction cao nhất. Họ cũng nghĩ tới những chàng trai ấy nhiều nhất.

Interesting.

Khi không chắc người kia nghĩ gì về mình, đôi khi não bộ lại dành nhiều resources hơn để cố giải thích cái uncertainty ấy.

Nó khiến t liên tưởng tới việc một người cứ mở điện thoại lên kiểm tra xem đối phương đã trả lời chưa, hoặc ngồi phân tích tại sao hôm qua người ấy còn nhắn tin rất nhiệt tình mà hôm nay lại im lặng.

Một cái uncertainty có thể chiếm rất nhiều cognitive bandwidth.

Nhưng trước khi các bạn bắt đầu áp dụng chiến thuật ba ngày không trả lời tin nhắn, có một nghiên cứu khác còn thú vị hơn.

Năm 2014, Dai, Dong và Jia nghiên cứu hiện tượng playing hard to get.

Họ phân biệt hai outcomes mà rất nhiều người thường nhầm lẫn.

Wanting and liking.

Trong các experiments của họ, khi một người đã có psychological commitment với việc theo đuổi đối phương, việc người kia tỏ ra khó có được có thể làm tăng desire to pursue, nhưng lại giảm mức độ liking.

Còn khi chưa có commitment từ trước, playing hard to get có thể làm giảm cả wanting lẫn liking.

Wait a minute.

Vậy tức là bạn có thể khiến một cô gái muốn chase mình nhiều hơn, nhưng chưa chắc cô ấy thực sự thích mình hơn?

Exactly.

Và đây là một classic optimization problem.

Nếu objective function của t chỉ là số lần cô ấy nhắn trước, số lần cô ấy đề nghị gặp hay bao nhiêu effort cô ấy bỏ ra để có được attention của mình, model có thể báo success.

Nhưng relationship quality có khi đang đi xuống.

You've optimized the wrong metric.

Có một nghiên cứu từ năm 1973 của Walster và cộng sự cũng khá hay. Họ phát hiện rằng trong một experiment, người phụ nữ thể hiện sự quan tâm có chọn lọc đối với chính người tham gia được đánh giá hấp dẫn hơn những người luôn dễ có được hoặc khó có được với tất cả mọi người.

T thích cái intuition của nghiên cứu này.

Scarcity không nhất thiết có nghĩa là bạn phải indifferent với người mình thích.

Nó có thể đơn giản là bạn selective.

Bạn không dành attention cho tất cả mọi người, nhưng khi thực sự thích ai đó, bạn vẫn chủ động dành thời gian cho họ.

That's selective scarcity.

Và ở đây có một lỗi economics rất cơ bản mà nhiều người dễ mắc phải.

Scarcity only matters if there's demand.

Giả sử cô gái kia vốn đã thích bạn, việc bạn không phải lúc nào cũng available có thể khiến những lần tương tác trở nên đáng mong đợi hơn trong một số hoàn cảnh.

Nhưng nếu cô ấy chẳng có interest gì với bạn, biến mất ba ngày chưa chắc khiến cô ấy nhớ bạn.

Có khi cô ấy còn chẳng nhận ra bạn đã biến mất.

No demand. No pricing power.

Thế nên t không tin zero effort là một universally optimal strategy.

Và cái belief rằng người bỏ nhiều effort hơn chắc chắn có perceived value thấp hơn cũng không phải một quy luật.

Một người có thể đầu tư rất nhiều vào relationship vì họ thật lòng thích đối phương, chứ không phải vì họ có ít options hơn.

Ngược lại, có người gần như không bỏ effort đơn giản vì họ chẳng quan tâm, chứ không phải vì họ high-value.

Nhưng t vẫn nghĩ concept về allocation of effort rất đáng bàn.

T có thể thích một cô gái, chủ động rủ cô ấy đi chơi, nhưng nếu mọi interaction đều chỉ có t cố gắng, t cần đặt câu hỏi liệu có nên tiếp tục đầu tư hay không.

Không phải vì t muốn manipulate cô ấy bằng artificial scarcity.

Mà vì t không thể tiếp tục allocate unlimited resources vào một position không có tín hiệu reciprocation.

Sounds familiar?

That's the quant mindset.

If I can't maximize the return, I'll minimize the loss.

Nhưng dating có một điểm khác với financial market.

Một cổ phiếu không quan tâm bạn có thích nó hay không. Nó không cảm thấy vui vì được bạn chọn, cũng chẳng buồn khi bạn quyết định bán.

Con người thì khác.

Nếu cả hai cùng cố tình không nhắn trước để tăng perceived value, cuối cùng sẽ có hai người ngồi nhìn điện thoại, mỗi người đều tin rằng mình đang thắng một cái game chẳng ai thực sự muốn chơi.

A very efficient strategy for achieving absolutely nothing.

Congratulations.

You've optimized your dating game into zero dates.

## Poker Theory

Okay, let's talk about poker. T từng xem một video khá thú vị của Lit Nomad, trong đó ông ấy nói về những similarities giữa poker, quant trading và dating,

Một trong những thứ khiến t thích poker là nó không chỉ là một trò chơi về xác suất. Nó còn là một trò chơi về information asymmetry, risk management, expected utility và cách bạn ra quyết định khi không thực sự biết đối phương đang cầm quân gì.

Sounds familiar?

Trong dating cũng vậy. Bạn không thực sự biết cô gái kia đang nghĩ gì về mình, cô ấy có bao nhiêu options, hay liệu việc mình vừa bỏ ra hai triệu cho một bữa tối có thực sự improve được cơ hội gặp lại cô ấy hay không.

Bạn chỉ có một vài observations, một ít signals, và rất nhiều uncertainty.

Và như mọi khi, t nghĩ có thể ngồi link rất nhiều concept để build một strategy có thể giúp t chiến thắng trên cả bàn pokers và trên thị trường hẹn hò.

## Short-stack Play — Exposure to Variance

Đầu tiên là *short-stack play*.

Trong poker tournament, khi bạn chỉ còn rất ít chips và sắp bị blinds ăn hết stack, việc tiếp tục chơi quá an toàn đôi khi chẳng còn ý nghĩa. Bạn phải lựa chọn một cơ hội phù hợp để shove or fold, bởi nếu cứ ngồi chờ một hand đủ đẹp, có khi bạn đã bị eliminated trước cả khi nó xuất hiện.

Dating cũng có những tình huống khá giống vậy.

Giả sử bạn đang theo đuổi một cô gái, nhưng càng ngày càng cảm thấy cô ấy mất interest. Những tin nhắn bắt đầu ngắn dần, response time tăng lên, và những lời mời đi chơi liên tục bị từ chối.

You're slowly getting blinded out.

Bạn có thể tiếp tục play safe, nhắn những câu xã giao vô thưởng vô phạt và chờ cái connection ấy từ từ biến mất.

Hoặc bạn có thể làm một việc khác.

**Expose yourself to variance.**

Lit Nomad đưa ra một ví dụ mà t thấy vừa buồn cười vừa khá genius.

Giả sử bạn đang date một cô gái trẻ, tốt nghiệp đại học, có vẻ khá progressive. Bạn cảm thấy mình sắp bị reject, và cơ hội cứu vãn gần như bằng không.

Thay vì cố gắng làm mọi thứ thật perfect để lấy lòng cô ấy, bạn quyết định xuất hiện trong buổi hẹn tiếp theo với một cái MAGA hat ủng hộ Trump.

Yes. A Trump MAGA hat.

Và khi cô ấy nhìn bạn với vẻ mặt khó hiểu, bạn bắt đầu giải thích rất tự tin rằng mình có quyền thể hiện political beliefs và sẽ không thay đổi bản thân chỉ để làm hài lòng người khác.

Now, what happens?

Theo cái hypothetical scenario của Lit Nomad, có tới 95% khả năng cô ấy sẽ thấy bạn cực kỳ kỳ quặc, thậm chí repulsive, rồi quyết định chẳng bao giờ gặp lại.

Nhưng có 5% khả năng cô ấy lại là một secret Trump supporter, hoặc ít nhất cảm thấy ấn tượng với sự tự tin và cái attitude chẳng quan tâm người khác nghĩ gì của bạn.

Suddenly, you're back in the game.

Đương nhiên 95% và 5% chỉ là những con số illustrative mà Lit Nomad đưa ra, không phải một statistical finding nào cả.

Nhưng t thích cái mathematical intuition đằng sau nó.

Khi bạn đang nắm một position gần như chắc chắn thua, một strategy có high variance đôi khi lại hấp dẫn hơn việc tiếp tục chấp nhận một cái outcome đang dần tiến về zero.

Trong poker, nếu bạn chỉ còn vài chips, downside của việc all-in bị giới hạn bởi số chips còn lại. Nhưng upside, nếu thắng, có thể đủ lớn để đưa bạn quay trở lại tournament.

Trong finance, nó hơi giống một call option.

Bạn có một limited downside, nhưng vẫn giữ được exposure với một potential upside đáng kể.

Nếu cứ tiếp tục chơi safe, bạn có thể đang bảo vệ một position vốn chẳng còn bao nhiêu value.

Còn khi expose yourself to variance, bạn chấp nhận một xác suất thua rất cao để đổi lấy cơ hội tạo ra một outcome mà strategy cũ gần như không thể mang lại.

Tất nhiên, high variance không tự động đồng nghĩa với positive expected value. Nếu upside không đủ lớn, hoặc downside thực ra vẫn còn đáng kể, thì bạn chỉ đang gamble một cách ngu ngốc.

Và dating cũng chẳng phải poker. Một cái MAGA hat có thể khiến bạn mất cơ hội, khiến người khác khó chịu, hoặc tạo ra một ấn tượng sai lệch về con người thật của mình.

Nhưng cái point ở đây không nhất thiết là phải đội MAGA hat, hay cố tình gây shock bằng một political opinion mà mình thậm chí chẳng tin.

Nó là việc dám thực hiện một action có khả năng thay đổi outcome, thay vì cứ tiếp tục một strategy mà bạn đã có đủ observations để biết rằng nó không hiệu quả.

Có thể là chủ động rủ cô ấy đi một buổi hẹn khác biệt hơn, nói thẳng một điều mà trước giờ bạn ngại nói, hoặc đơn giản là thể hiện một khía cạnh chân thật nhưng hơi unusual của bản thân.

Một move có thể khiến người kia thích bạn hơn, hoặc nhận ra hai người thực sự chẳng phù hợp.

Either way, you get new information.

T thấy concept này khá thú vị vì nó gần như đi ngược lại cái quant mindset mà t luôn tự hào.

T có thói quen minimize exposure, control downside và chuẩn bị exit strategy trước khi làm bất cứ chuyện gì.

Nhưng đôi khi, khi downside đã gần chạm đáy, việc tiếp tục minimize variance chẳng còn giúp mình đạt được điều gì nữa.

**You can't win a tournament by folding every hand.**

Và có lẽ trong dating cũng vậy.

Đôi khi bạn phải chấp nhận một xác suất bị reject để có cơ hội đạt được outcome mình muốn.

Không phải cứ all-in là thông minh.

Nhưng một thằng không bao giờ dám bet thì cũng chẳng thể thắng được pot nào.

Anyway, nếu short-stack play là cách bạn xử lý một position sắp thua, thì có một concept khác trong poker giúp bạn biết mình đang đứng ở đâu trước khi quyết định bet thêm.

It's called the *feeler bet*.

## The Feeler Bet

Trong poker, đôi khi bạn thực hiện một bet nhỏ không chỉ để thắng pot, mà còn để tìm hiểu cách đối phương phản ứng, từ đó update estimate về range của họ.

Liên hệ nó với chuyện dating, giả sử bạn vừa đi first date với một cô gái. Buổi tối khá vui, hai người nói chuyện được vài tiếng, nhưng bạn vẫn không thực sự biết cô ấy có muốn gặp lại mình hay không.

Bạn có thể ngồi phân tích hàng trăm signals.

Cô ấy có cười nhiều không? Có hỏi về công việc của bạn không? Lúc về có nhắn tin trước không? Có sử dụng emoji trong tin nhắn không?

Hoặc bạn có thể thực hiện một cái probe rất đơn giản.

"Hey, I had fun tonight. Wanna grab coffee this weekend?"

Small investment. New information.

Nếu cô ấy đồng ý và chủ động chọn thời gian, đó là một positive signal.

Nếu cô ấy bận nhưng đề xuất một ngày khác, cũng là một signal đáng chú ý.

Còn nếu cô ấy liên tục từ chối và không hề muốn tìm một alternative, thì có lẽ bạn đã có thêm lý do để update prior của mình.

Tất nhiên một observation không phải proof. Có những người không giỏi nhắn tin, có người thực sự bận, và cũng có người cần thêm thời gian để hiểu người khác.

Nhưng thay vì ngồi guessing mãi, một lời mời rõ ràng đôi khi đem lại nhiều information hơn cả trăm cái emoji.

Lit Nomad còn đề xuất quan sát những metrics như text length ratio, response time, tỷ lệ tin nhắn được gửi và nhận, hay mức độ chủ động của mỗi người.

Và t phải công nhận, với tư cách một data scientist, t thấy cái idea ấy khá hấp dẫn.

Imagine building an attraction classifier from text messages. Một cái app tên là Are They Into You?

Input: text messages.

Output: attraction probability.

Model confidence: questionable.

Features có thể bao gồm số lần hai người chủ động bắt đầu conversation, số câu hỏi được đặt ra, mức độ reciprocation hay tần suất chủ động đề xuất gặp nhau.

Nhưng reply time bằng nhau không có nghĩa attraction bằng nhau. Một người có thể trả lời rất nhanh vì đang rảnh, hoặc rất chậm vì công việc bận rộn.

Và một cái model đọc tin nhắn cũng không thể tự hiểu toàn bộ relationship context, chưa kể những vấn đề về privacy nếu đem private conversations đi phân tích mà chưa có sự đồng ý.

Still, the concept is interesting.

Instead of assuming you know someone's preferences, make an observation and update your prediction.

That's literally what Bayesian thinking is about.

## Continuation Bet

There ss another concept in pokers i think it's very related to dating, Continuation bet.

Trong poker, sau khi là người raise ở vòng trước, bạn có thể tiếp tục bet ở vòng tiếp theo trong những tình huống phù hợp, kể cả khi bài của mình chưa thực sự mạnh.

Điều thú vị là đôi khi người ta ngại bet không phải vì nó có negative expected value, mà vì họ sợ bị call hoặc raise khi đang bluff.

Basically, their ego gets in the way.

Trong dating cũng vậy.

Rất nhiều người không dám chủ động rủ người mình thích đi chơi vì sợ bị từ chối.

Họ sợ mất mặt, sợ người khác biết mình bị reject, hay đơn giản là không muốn nhận một cái outcome bằng 0.

Nhưng nếu không bao giờ hỏi thì probability of getting a date thông qua lời mời ấy cũng bằng 0.

You miss every shot you don't take.

T nghĩ có một sự khác biệt lớn giữa việc sợ thua và việc chơi để thắng.

Nếu t thực sự thích một cô gái, và cost của việc hỏi cô ấy có muốn đi cà phê không tương đối nhỏ, tại sao t lại không thử?

Worst case, she says no.

Of course, there's an emotional cost. Rejection chẳng bao giờ hoàn toàn miễn phí.

Nhưng nếu chỉ vì sợ một lần bị từ chối mà không bao giờ thực hiện action nào, bạn có thể đang minimize losses bằng cách eliminate luôn cả potential returns.

Và đấy là lúc t thấy cái poker analogy này còn liên quan tới chính mình.

T luôn thích control exposure. Tính risk budget, estimate downside, chuẩn bị exit strategy trước khi bước vào một chuyện gì đó.

Nhưng đôi khi, chính việc quá tập trung vào protecting downside khiến t quên mất rằng muốn thắng thì trước hết phải chấp nhận một xác suất thua nào đó.

Không phải cứ all-in là thông minh.

Nhưng fold every hand cũng chẳng phải một winning strategy.

## Don't Play Your Cards. Play the Player.

Có một câu nói rất nổi tiếng trong poker.

Don't play your cards. Play the player.

Trong dating, cái cards của bạn có thể là appearance, intelligence, money, status và những thứ mà t đã cố quantify bằng SMV ở đầu chương.

Nhưng sở hữu một bộ features đủ đẹp không đảm bảo rằng cô gái kia sẽ thích bạn.

Bởi vì còn một variable khác.

Her preferences.

Một cô gái có thể thích những người cực kỳ ambitious, còn một người khác chỉ muốn một partner có nhiều thời gian dành cho gia đình.

Có người thích fine dining. Có người lại thích cùng nhau khám phá một quán cà phê nhỏ hay đi dạo quanh thành phố.

Vậy nên một strategy thành công với người này chưa chắc có tác dụng với người khác.

T nghĩ đây mới là điều đáng học từ poker: thay vì chỉ cố improve hand strength của mình, hãy tìm hiểu người mà mình đang thực sự tương tác.

Nhưng t không nghĩ điều đó có nghĩa là phải giả vờ trở thành đúng kiểu người cô ấy muốn.

Trong poker, bạn có thể bluff.

Dating thì phức tạp hơn, vì một cái bluff thành công ở first date có thể trở thành một lời nói dối mà bạn phải duy trì trong cả relationship.

Giả vờ giàu hơn, thông minh hơn hay sống một cuộc đời thú vị hơn mình thực sự có thể giúp bạn tạo first impression tốt hơn trong một vài phút.

Nhưng sau đó thì sao?

Bạn sẽ phải maintain cả cái character ấy.

Sounds exhausting.

Và có lẽ đó là một khoản investment còn đắt hơn bất cứ bữa tối nào.

## The First Date Algorithm

Okay, enough theory.

Let's get practical.

Giả sử sau tất cả những theory vừa rồi, bạn tìm được một cô gái mà mình thực sự muốn đi chơi cùng.

Từng có một thời gian t nghĩ cách optimize ngân sách của một buổi hẹn cũng rất đơn giản.

Look at the girl, estimate her attractiveness, then decide how much you're willing to spend.

Một triệu, ba triệu hay mười triệu.

T còn từng nghĩ nhan sắc càng cao thì mình càng dễ cảm thấy một bữa tối đắt tiền là worth it.

Nghe khá giống investment analysis nhỉ.

Có điều sau cái sigmoid model vừa rồi, rõ ràng việc maximize spending không hẳn là optimal strategy.

Bởi vì bản thân việc được ngồi ăn tối với ai đó chưa chắc phụ thuộc vào số tiền bạn bỏ ra.

Và đôi khi, bạn còn chẳng cần nghĩ nhiều đến thế.

T nhớ từng có một cuộc nói chuyện khá buồn cười với một thằng bạn.

Nó hỏi t có chắc mình muốn rủ một cô gái đi chơi không.

"Are you sure?"

"Absolutely."

"Sao mày nghĩ cô ấy sẽ đồng ý?"

"Why not?"

"Không, tao đang hỏi tại sao cô ấy muốn đi chơi với mày?"

"Yeah. Why not? That's my answer."

Nó nhìn t như thể vừa nghe một cái regression model không có dependent variable.

T bắt đầu giải thích.

Cô ấy được đi ăn một bữa tối mà không phải trả tiền. Có một người ngồi nghe cô ấy yapping cả buổi. Và quan trọng nhất, cô ấy được hang out với một người như t.

I'm funny, you know.

Nó hỏi tiếp:

"À, còn được đi với một thằng đẹp trai nữa nhỉ?"

"Exactly! You got it now."

T nói với vẻ mặt như vừa đặt dấu chấm cuối cùng cho một mathematical proof.

Nhưng sau đó t nhận ra hai đứa đang giải hai bài toán khác nhau.

Nó hỏi why would she say yes?

T lại hỏi why would she say no?

Nó muốn tìm evidence rằng cô ấy có demand đối với t.

Còn t đang tìm cách remove friction khỏi một cái conversion funnel.

Nếu cô ấy ngại mất tiền, dinner is on me.

Nếu địa điểm quá xa, t chọn một nơi khác.

Nếu sợ buổi tối awkward, t có thể chủ động trò chuyện.

Nếu cô ấy muốn ăn gì đó, t có thể tìm một chỗ phù hợp.

T đang optimize những điều kiện khiến lời mời trở nên dễ chấp nhận hơn.

Nhưng thằng bạn t hỏi một câu mà toàn bộ optimization ấy chưa thực sự trả lời.

Does she actually want to spend time with you?

Và đúng là có những thứ không thể giải quyết chỉ bằng cách remove blockers.

Một người có thể hoàn toàn rảnh, không phải trả tiền, địa điểm lại ngay gần nhà, nhưng vẫn chẳng muốn đi ăn tối với bạn.

Not because your offer is bad.

Maybe there's simply no attraction.

Đấy chính là sự khác biệt giữa demand validation và conversion optimization.

Và nếu có một điều t rút ra từ việc nghĩ quá nhiều về dating, thì đó là mình nên giải đúng bài toán trước khi optimize nó.

Dù vậy, t vẫn thích nghĩ về dating như một data pipeline.

Job 01 là first date.

Input gồm hai người chưa hiểu nhau đủ, một bữa tối và rất nhiều uncertainty.

Output không phải việc bạn đã thuyết phục được cô ấy đồng ý đi chơi.

Output tốt nhất là cả hai có một buổi tối vui vẻ và đều muốn gặp lại.

Job 01 successful?

Trigger Job 02.

Có thể là cà phê, một bộ phim, đi dạo, hoặc một activity nào đó mà cả hai đều thích.

Job 02 successful?

Trigger Job 03.

Cứ thế.

Don't overengineer your wedding before finishing the first dinner.

Và nếu một người không muốn tiếp tục, đó không phải transient error để bạn retry thêm mười lần.

Pipeline ends.

T thích approach này vì thay vì cố predict toàn bộ future từ vài bức ảnh trên Tinder, t có thể update model bằng observations sau mỗi interaction.

Trên profile, cô ấy có thể nói mình thích những người thông minh, hài hước, thành công và có chiều sâu.

Nhưng lúc hai người gặp nhau, đôi khi chemistry chẳng tuân theo bất kỳ feature importance nào mà chúng ta đã estimate.

Eastwick và Finkel từng có nghiên cứu speed-dating cho thấy những preferences mà người tham gia tuyên bố trước đó không dự đoán tốt điều gì khiến họ thực sự muốn một người sau khi gặp mặt.

Càng thú vị hơn khi t nghĩ chính mình cũng có thể rơi vào cái bias ấy.

T có thể ngồi một buổi để rank appearance, intelligence, money, status, rồi tự tin nói rằng mình biết chính xác mẫu người mình thích.

Nhưng sau đó lại gặp một cô gái mà mọi thứ trên giấy chẳng có gì quá đặc biệt, và chẳng hiểu sao vẫn muốn nói chuyện với cô ấy tới tận lúc quán đóng cửa.

Vậy nên có lẽ cái original SMV function của t cũng cần thêm vài features.

Hoặc t đã assign sai weights ngay từ đầu.

## The Objective Function

Sau cả đống evolutionary biology, game theory, Tinder analytics, logistic regression và asset pricing, cuối cùng t vẫn phải quay về một câu hỏi khá đơn giản.

What am I actually optimizing for?

Nếu mục tiêu chỉ là getting matches, t có thể optimize profile pictures.

Nếu muốn nhiều first dates, t có thể improve messaging strategy và reduce friction.

Nếu muốn một cô gái chủ động chase mình, t có thể thử tạo uncertainty hoặc artificial scarcity.

Nhưng nếu t thực sự muốn một relationship thì sao?

T nghĩ cái objective function lúc ấy phải khác.

Appearance tất nhiên vẫn quan trọng. T cũng chẳng giả vờ nói rằng mình không quan tâm tới ngoại hình.

Đương nhiên vẫn phải xinh chứ, lol.

Nhưng nếu phải assign weights, t nghĩ intelligence và intellectual compatibility mới là hai features mà t coi trọng hơn.

Liệu cô ấy có thể ngồi với t cả buổi để nói về philosophy, science, history, economics, conspiracy theories hay những thứ random mà hai đứa vừa đọc được trên internet hay không?

Liệu cô ấy có thể challenge một cái theory của t, chỉ ra tại sao cái logic nghe rất hợp lý ấy thực ra lại sai?

Liệu t có thể kể một câu chuyện rất dài, rất nerdy, mà cô ấy vẫn thực sự muốn nghe, không phải vì lịch sự, cũng chẳng phải vì cô ấy đang cố impress t?

Và ngược lại, liệu t có đủ tò mò để hiểu thế giới của cô ấy, thay vì lúc nào cũng cố explain nó bằng models của mình?

T nghĩ những thứ ấy quan trọng hơn nhiều so với việc cô ấy được bao nhiêu điểm trên một cái SMV scale mà chính t tạo ra.

Có lẽ sau tất cả, thứ t muốn không phải một người có perceived market value cao nhất.

Mà là một người khiến t cảm thấy việc dành thời gian cho cô ấy chưa bao giờ giống một khoản investment phải tính toán.

Một buổi tối ăn pizza trên sofa, nói đủ thứ chuyện trên đời.

No fancy restaurant. No artificial scarcity. No need to play hard to get.

Just two people who genuinely want to be there.

Tất nhiên, t vẫn sẽ tiếp tục build models. It's literally what I do.

Nhưng có một điều mà t nghĩ mình bắt đầu hiểu.

A model can optimize a metric perfectly and still miss the entire point.

Anyway.

Thank you for coming to my TED Talk.
