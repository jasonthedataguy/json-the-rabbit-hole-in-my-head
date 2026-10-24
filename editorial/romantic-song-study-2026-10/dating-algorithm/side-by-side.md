# Dating Algorithm — Side-by-side editorial reading

**Music lens:** fake love don't last — mgk / iann dior; You Got The Part — New West

**Assessment:** A 8.9/10 · B 8.8/10 · **Recommendation: A**

The approved version already contains its own self-correction and elaborate models. B adds distrust as an emotional source but gives away the later arc too early and lengthens an already long chapter.

Source version: [approved repository manuscript](../../chapters/dating-algorithm/source/approved.md). Text in Version A below is a literal snapshot, not an edited revision. Version B retains the full source and adds 2 original interpolations inspired by emotional themes, without song lyrics.

<table><thead><tr><th>VERSION A — Current approved</th><th>VERSION B — Song-informed alternative</th></tr></thead><tbody><tr><td valign="top"><p>Let a data scientist teach you how to optimize your dating game.</p>
<p>It's all based on a metric called SMV (Sexual Market Value), and this value is perceived differently between genders.</p>
<p>Suppose we have a few factors: appearance, intelligence, status, money… For men, I'd argue that money and status account for 70% of the total weight, while for women, appearance alone accounts for 90%.</p>
<p>From there, you can easily estimate your value and the girl's value. And the game is simple: you want to date up, right?</p>
<p>I mean, why would you date a girl with a lower SMV than yours? You're basically downgrading your own position in the dating market. Think of it like investing in a financial asset. Why would you allocate your resources to a lower-return investment when you could get a better one?</p>
<p>But here's the catch.</p>
<p>If you date a girl whose perceived value is significantly higher than yours, there's a possibility she's only settling for you because she couldn't find a better option. And if that's the case, she might eventually start to undermine you, lose respect for you, or constantly compare you with the alternatives she thinks she deserves.</p>
<p>That's my rather brutal interpretation of female mate selection.</p>
<p>So what's the optimal strategy?</p>
<p>Find someone whose perceived value is roughly equivalent to yours. Neither player has a strong incentive to seek a better alternative, and both are getting a fair deal.</p>
<p>That's what I called Nash equilibrium.</p>
<p>Simple as that.</p>
<p>Welcome to my TED Talk on dating.</p>
<p>T vừa giải thích tình yêu bằng một scoring function, vài weights và Nash equilibrium. Một vấn đề mà nhân loại vật lộn hàng nghìn năm, t xử lý trong đúng một paragraph.</p>
<p>You're welcome.</p>
<p>Và trước khi các bạn bắt đầu hỏi 70% và 90% kia đến từ đâu, nguồn dataset nào, sample size bao nhiêu, p-value có significant không — please, hold your questions until the end.</p>
<p>First, a little evolutionary biology.</p>
<p>Có một lý do khiến tôi thích đặt những giả thuyết khó chịu về mating strategies. Robert Trivers có Parental Investment Theory: ở nhiều loài, giới đầu tư nhiều hơn vào việc tạo và nuôi con có thể chịu những áp lực lựa chọn bạn tình khác biệt. Con người không giống một mô hình sinh học tối giản, nhưng nó gợi ra một câu hỏi về incentives: khi cost và risk khác nhau, hai players có nhất thiết dùng cùng strategy không?</p>
<p>Các nghiên cứu cross-cultural về mate preferences của David Buss từng tìm thấy những khác biệt trung bình giữa nam và nữ trong mức độ coi trọng ngoại hình và khả năng kiếm nguồn lực. Lịch sử cũng có những xã hội cho phép đa thê, thậm chí hậu cung của hoàng đế, nơi quyền lực và cơ hội sinh sản gắn với nhau. Nhưng trung bình của một mẫu không phải tính cách của một cá nhân. Và hậu cung không phải Tinder: quyền lực chính trị, ép buộc và trật tự xã hội đều có mặt trong câu chuyện.</p>
<p>Harari trong Sapiens khiến tôi hứng thú với chính khoảng giao nhau giữa sinh học và trật tự do con người tạo ra. Những gì ta gọi là 'natural' đôi khi đã qua vô số lớp văn hóa và thể chế. Thú vị là tôi có thể đọc những điều ấy rồi vẫn tự tin nhét toàn bộ con người vào bốn features và hai bộ weight bịa ra trong một buổi chiều.</p>
<p>70% và 90% không phải evidence. They're hyperparameters. Assigned by Jason, peer-reviewed by Jason, approved by Jason.</p>
<p>Còn Nash equilibrium? Tôi dùng từ ấy rất hào hứng. Nhưng hai người có cùng SMV không tự động tạo ra Nash equilibrium. Đúng nghĩa game theory, equilibrium liên quan tới những chiến lược mà không ai muốn đơn phương đổi khi người kia giữ nguyên. Cái tôi đang mô tả có lẽ gần một matching problem hơn. Có lẽ ngay từ đầu tôi đã trộn game theory với một trò xếp hạng người yêu.</p>
<p>## The Dating Game</p>
<p>Okay, có một chuyện khá buồn cười ở đây. Trong lúc tôi tự nhận mình vừa giải xong dating market, một người khác đã đem gần như cùng một mô hình lên bảng. Professor Jiang Xueqin, trong bài giảng Game Theory #1: The Dating Game, lấy năm người đàn ông và năm người phụ nữ, rồi xếp mỗi bên từ 1 đến 5 dựa trên genes, wealth và status.</p>
<p>Nếu tất cả đều muốn người top-ranked, người đàn ông số 5 có thể muốn theo đuổi cả năm người. Nhưng lúc ấy, những players còn lại đâu có đứng yên chờ được chọn. Họ đổi strategy. Người ta có thể chọn một partner ít nổi bật hơn nhưng đáng tin cậy hơn, và cuối cùng gã số 5, vì muốn maximize mọi cơ hội, lại có nguy cơ chẳng giữ được điều mình muốn nhất.</p>
<p>Trong minh họa của Jiang, các cặp 5–5, 4–4, 3–3, 2–2, 1–1 tạo ra một phương án hợp tác. Ông gọi nó là Nash equilibrium. Strictly speaking, xếp hạng bằng nhau chưa đủ để chứng minh equilibrium nếu ta chưa định nghĩa đầy đủ payoffs và deviations. Nhưng cái point của ông thì hay: your best move depends on what everybody else is going to do.</p>
<p>Ông còn kể một bài tập trên lớp: hỏi sinh viên rằng nếu đã ba mươi tuổi và rất muốn kết hôn, họ cần điều kiện tối thiểu gì ở partner. Câu trả lời của các bạn nam và nữ trong lớp được ông dùng để bàn về incentives. Fun story, nhưng đấy là một classroom anecdote, không phải randomized controlled trial.</p>
<p>Có điều Professor Jiang có một cái bảng trắng. Jason thì có Tinder.</p>
<p>## The Tinder Experiment</p>
<p>T từng đem chính cái model ấy ra đối chiếu với một bộ data nhỏ: 10 Tinder profiles, gồm năm thằng bạn và năm cô bạn gái của t.</p>
<p>Five guys. Five girls. A very questionable research grant of exactly zero dollars.</p>
<p>T bắt đầu bằng cách chấm mỗi profile trên thang 1 đến 10. T gọi chỉ số ấy là perceived visual SMV — không phải giá trị của một con người, cũng chẳng phải SMV thật trong đời sống, mà là điểm hấp dẫn chủ quan mà một người xem có thể gán cho cách profile được trình bày trên app: ảnh đại diện, outfit, expression, cách chọn góc chụp, overall vibe và first impression.</p>
<p>Một người ngoài đời rất cuốn hút có thể lên ảnh cực kỳ nhạt nhẽo. Một người chụp ảnh đẹp chưa chắc nói chuyện thú vị. Cho nên 8/10 ở đây có nghĩa là “Jason nhìn profile này và chấm 8”, chứ không phải “người này có giá trị bằng 8”.</p>
<p>Scientific rigor, ladies and gentlemen.</p>
<p>T gắn nhãn M1 đến M5 và F1 đến F5, rồi muốn nhìn vào từng bước của funnel: bao nhiêu lượt swipe right, bao nhiêu match, tỷ lệ match trên số likes đã gửi, ai chủ động nhắn trước, bao nhiêu cuộc trò chuyện thực sự tiếp tục sau lời chào đầu tiên.</p>
<p>Vì sao phải tách chúng ra? Bởi vì getting liked, getting matched, và being worth meeting again là ba outcome khác nhau. Bạn có thể có rất nhiều matches mà chẳng có nổi một cuộc nói chuyện ra hồn. Cũng có thể có rất ít matches, nhưng mỗi cuộc trò chuyện lại đáng để tiếp tục.</p>
<p>Đương nhiên, N = 10 là một sample size đáng xấu hổ nếu muốn generalize cho toàn bộ dating market, và không ai có thể dùng dataset này để công bố quy luật về toàn bộ đàn ông và phụ nữ. Chưa kể Tinder algorithm còn quyết định profile nào được hiển thị cho ai, vào thời điểm nào. Tuổi, địa điểm, hình ảnh và cách mỗi người swipe đều có thể là confounding variables. Cái perceived SMV score lại còn do chính t chấm. Biased as hell.</p>
<p>Nhưng nếu coi nó như một observational case study về những người t biết, thì đây là một experiment đủ thú vị để đặt ra câu hỏi. Nó cho tôi cơ hội kiểm tra xem cái lý thuyết về attraction mà tôi vừa hùng hồn giảng có chịu nổi một chút real-world data hay không.</p>
<p>T cũng đọc một nghiên cứu field experiment trên Tinder với 3.600 profile evaluations: trong mẫu nghiên cứu ấy, phụ nữ có xu hướng chọn lọc hơn và quan tâm đến trình độ học vấn của nam giới; nghiên cứu không tìm thấy bằng chứng đàn ông né tránh những phụ nữ có học vấn cao. Nói cách khác, đời thực có một vài pattern đáng nghiên cứu, nhưng nó chẳng ngoan ngoãn biến thành hai con số 70% và 90% của tôi.</p>
<p>That's the difference between a model you like and a model the data actually supports.</p>
<p>Nhưng sau Tinder, t lại có thêm một câu hỏi.</p>
<p>Giả sử bạn đã match với một cô gái. Giả sử cô ấy cũng có một chút interest với bạn.</p>
<p>How much effort should you actually invest to make her like you?</p>
<p>## The Marginal Cost of Attraction</p>
<p>Okay, let's talk about diminishing marginal returns. T nghĩ có một thứ khá thú vị về dating mà mọi người thường overlook.</p>
<p>Giả sử t build một logistic regression model để predict liệu một cô gái có thích bạn hay không.</p>
<p>Outcome được define rất đơn giản:</p>
<p>Y = 1: She likes you.</p>
<p>Y = 0: She doesn't.</p>
<p>Đương nhiên attraction ngoài đời là cả một spectrum, chứ chẳng có cái switch on/off nào trong đầu con người. Nhưng vì t đang muốn giải một binary classification problem nên cứ tạm simplify nó như vậy.</p>
<p>T sử dụng một sigmoid function để estimate probability của outcome.</p>
<p>P(Y = 1) = 1 / (1 + e^(-z))</p>
<p>Trong đó z là một weighted combination của những features ảnh hưởng tới attraction.</p>
<p>Bây giờ thử đơn giản hóa model thêm một chút.</p>
<p>T đặt effort invested lên trục X, bao gồm time, money, attention và emotional investment mà bạn bỏ ra để theo đuổi một cô gái.</p>
<p>Trục Y là probability that she likes you.</p>
<p>Đương nhiên, đây mới chỉ là một hypothetical model, không thể đơn giản cộng một triệu tiền ăn tối với hai tiếng nhắn tin thành một metric được. Và effort chưa chắc đã có positive effect trong mọi trường hợp.</p>
<p>Nhưng giả sử chúng ta đã normalize được effort thành một index, và trong khoảng đang xét, tăng effort giúp tăng attraction probability, thì sigmoid có một property rất thú vị.</p>
<p>Diminishing marginal returns.</p>
<p>Khi probability còn rất thấp, thêm một chút effort có thể chẳng thay đổi được bao nhiêu.</p>
<p>Khi probability đã rất cao, bạn cũng chẳng nhận được bao nhiêu marginal gain từ việc tiếp tục tăng investment.</p>
<p>Sensitivity lớn nhất xuất hiện ở vùng giữa, gần decision boundary.</p>
<p>Bây giờ thử xem một ví dụ nhé.</p>
<p>Giả sử có một cô gái đã rất thích bạn từ trước. Attraction probability trong cái hypothetical model của t đang là 90%.</p>
<p>Bạn đưa cô ấy đi ăn một bữa tối hai triệu.</p>
<p>Maybe it goes up to 92%.</p>
<p>Bạn mua thêm một bó hoa.</p>
<p>Maybe 93%.</p>
<p>Rồi bạn book thêm một nhà hàng fine dining năm triệu, chuẩn bị một outfit chỉn chu, dành cả ngày lên kế hoạch cho buổi hẹn.</p>
<p>Maybe 94%.</p>
<p>Đây là những con số t bịa ra để illustrate thôi, chứ không phải calibrated probabilities nhé.</p>
<p>But you get the idea.</p>
<p>You're already on the right side of the sigmoid.</p>
<p>Bỏ thêm rất nhiều resources chưa chắc tạo ra một improvement tương xứng trong probability.</p>
<p>Và có khi bạn chẳng cần một bữa tối đắt tiền nào cả.</p>
<p>T lấy một ví dụ khá buồn cười.</p>
<p>Giả sử có một cô gái đã rất thích bạn. Một hôm cô ấy muốn qua nhà chơi, và bạn nhắn:</p>
<p>"Hey, on your way here, can you grab us some pizza?"</p>
<p>Cô ấy có thể vui vẻ đáp lại:</p>
<p>"Hahaha, you're funny. What pizza do you want?"</p>
<p>Rồi hai người ngồi ăn pizza trên sofa, xem một bộ phim, kể vài câu chuyện ngớ ngẩn, và có khi đó lại là một buổi tối vui hơn bất cứ cái fine dining restaurant nào.</p>
<p>Bây giờ tưởng tượng bạn nói đúng câu ấy với một cô gái chẳng hứng thú gì với mình.</p>
<p>"Wait, you're inviting me over and asking me to buy you dinner?"</p>
<p>Same guy. Same request. Completely different interpretation.</p>
<p>Tất nhiên cái pizza này không phải một statistical test. Một cô gái có thể không mua pizza đơn giản vì cô ấy bận, không thích pizza, hoặc thấy việc được nhờ mua đồ chẳng liên quan gì tới chuyện mình thích ai.</p>
<p>Nhưng có một point mà t thấy khá hay.</p>
<p>Khi đã có attraction, người ta có thể interpret những hành động của đối phương theo một hướng tích cực hơn.</p>
<p>Một câu đùa nhạt cũng có thể trở nên funny. Một hành động bình thường cũng có thể trở nên đáng yêu.</p>
<p>Và đôi khi, chính việc được làm điều gì đó cho người mình thích cũng khiến bản thân cảm thấy vui.</p>
<p>T muốn gọi đây là một dạng conditional perceived value.</p>
<p>Giá trị mà người ta gán cho một interaction không chỉ phụ thuộc vào action ấy, mà còn phụ thuộc vào prior attraction họ đã có với bạn.</p>
<p>Nói cách khác, t không nghĩ dating là một cái auction, nơi thằng nào chịu chi nhiều nhất thì thắng.</p>
<p>If she's already into you, you don't have to keep raising your bid.</p>
<p>Ngược lại, nếu cô ấy không có chút interest nào từ đầu, bạn cũng không thể assume rằng cứ tăng spending thì sẽ eventually cross được decision boundary.</p>
<p>Một bữa tối mười triệu không tự nhiên biến một người không thích bạn thành một người thích bạn.</p>
<p>Money can buy dinner.</p>
<p>It can't guarantee chemistry.</p>
<p>Và từ đó, t bắt đầu nghĩ tới một theory khác.</p>
<p>Nếu adding effort không nhất thiết tăng attraction, vậy reducing effort có thể khiến mình trở nên attractive hơn hay không?</p>
<p>## The Economics of Attention</p>
<p>Let's talk about asset pricing.</p>
<p>Trong financial market, giá một asset không chỉ phụ thuộc vào intrinsic value, mà còn chịu ảnh hưởng của supply, demand, liquidity và expectations.</p>
<p>Tất nhiên, con người không phải financial assets. Nhưng thử tạm dùng cái analogy ấy để model perceived attention.</p>
<p>Suppose your attention is an asset.</p>
<p>Và giả sử bạn có một lượng thời gian, energy và emotional capacity hữu hạn để phân bổ cho những người khác nhau.</p>
<p>Một thằng lúc nào cũng available, luôn nhắn trước, luôn chủ động lên kế hoạch, thậm chí sẵn sàng cancel những dự định của riêng mình để gặp một cô gái, đang gửi đi một signal rằng attention của nó rất dễ có được.</p>
<p>Trong khi một thằng khác có công việc, hobbies, bạn bè và một cuộc sống riêng đủ thú vị thì không phải lúc nào cũng available.</p>
<p>Same attention. Different scarcity.</p>
<p>Vậy có phải attention của thằng thứ hai sẽ được perceived là valuable hơn?</p>
<p>Maybe.</p>
<p>Và đây là lúc t nghĩ tới một strategy mà chắc nhiều người từng nghe.</p>
<p>Artificial scarcity.</p>
<p>Giả sử bạn thích một cô gái, nhưng thay vì thể hiện interest, bạn cố tình không nhắn trước, không chủ động gặp mặt, thậm chí tỏ ra indifferent.</p>
<p>Mục đích rất đơn giản.</p>
<p>Bạn muốn cô ấy nghĩ rằng attention của mình là một thứ scarce resource, và muốn có được nó thì cô ấy phải bỏ effort.</p>
<p>Basically, reduce supply to increase perceived price.</p>
<p>Economics 101.</p>
<p>Pretty smart, right?</p>
<p>Điều buồn cười là psychology thực sự có một vài nghiên cứu khiến cái theory này nghe không hoàn toàn vô lý.</p>
<p>Năm 2011, Whitchurch và cộng sự thực hiện một experiment, trong đó những nữ sinh viên xem Facebook profiles của một số chàng trai được cho là đã xem profile của họ.</p>
<p>Một nhóm được nói rằng những chàng trai ấy rất thích mình. Một nhóm khác được nói rằng họ chỉ thích ở mức trung bình. Nhóm cuối cùng thì không biết chính xác những chàng trai ấy thích mình nhiều hay vừa phải.</p>
<p>Guess what?</p>
<p>Trong experiment ấy, nhóm uncertain báo cáo mức attraction cao nhất. Họ cũng nghĩ tới những chàng trai ấy nhiều nhất.</p>
<p>Interesting.</p>
<p>Khi không chắc người kia nghĩ gì về mình, đôi khi não bộ lại dành nhiều resources hơn để cố giải thích cái uncertainty ấy.</p>
<p>Nó khiến t liên tưởng tới việc một người cứ mở điện thoại lên kiểm tra xem đối phương đã trả lời chưa, hoặc ngồi phân tích tại sao hôm qua người ấy còn nhắn tin rất nhiệt tình mà hôm nay lại im lặng.</p>
<p>Một cái uncertainty có thể chiếm rất nhiều cognitive bandwidth.</p>
<p>Nhưng trước khi các bạn bắt đầu áp dụng chiến thuật ba ngày không trả lời tin nhắn, có một nghiên cứu khác còn thú vị hơn.</p>
<p>Năm 2014, Dai, Dong và Jia nghiên cứu hiện tượng playing hard to get.</p>
<p>Họ phân biệt hai outcomes mà rất nhiều người thường nhầm lẫn.</p>
<p>Wanting and liking.</p>
<p>Trong các experiments của họ, khi một người đã có psychological commitment với việc theo đuổi đối phương, việc người kia tỏ ra khó có được có thể làm tăng desire to pursue, nhưng lại giảm mức độ liking.</p>
<p>Còn khi chưa có commitment từ trước, playing hard to get có thể làm giảm cả wanting lẫn liking.</p>
<p>Wait a minute.</p>
<p>Vậy tức là bạn có thể khiến một cô gái muốn chase mình nhiều hơn, nhưng chưa chắc cô ấy thực sự thích mình hơn?</p>
<p>Exactly.</p>
<p>Và đây là một classic optimization problem.</p>
<p>Nếu objective function của t chỉ là số lần cô ấy nhắn trước, số lần cô ấy đề nghị gặp hay bao nhiêu effort cô ấy bỏ ra để có được attention của mình, model có thể báo success.</p>
<p>Nhưng relationship quality có khi đang đi xuống.</p>
<p>You've optimized the wrong metric.</p>
<p>Có một nghiên cứu từ năm 1973 của Walster và cộng sự cũng khá hay. Họ phát hiện rằng trong một experiment, người phụ nữ thể hiện sự quan tâm có chọn lọc đối với chính người tham gia được đánh giá hấp dẫn hơn những người luôn dễ có được hoặc khó có được với tất cả mọi người.</p>
<p>T thích cái intuition của nghiên cứu này.</p>
<p>Scarcity không nhất thiết có nghĩa là bạn phải indifferent với người mình thích.</p>
<p>Nó có thể đơn giản là bạn selective.</p>
<p>Bạn không dành attention cho tất cả mọi người, nhưng khi thực sự thích ai đó, bạn vẫn chủ động dành thời gian cho họ.</p>
<p>That's selective scarcity.</p>
<p>Và ở đây có một lỗi economics rất cơ bản mà nhiều người dễ mắc phải.</p>
<p>Scarcity only matters if there's demand.</p>
<p>Giả sử cô gái kia vốn đã thích bạn, việc bạn không phải lúc nào cũng available có thể khiến những lần tương tác trở nên đáng mong đợi hơn trong một số hoàn cảnh.</p>
<p>Nhưng nếu cô ấy chẳng có interest gì với bạn, biến mất ba ngày chưa chắc khiến cô ấy nhớ bạn.</p>
<p>Có khi cô ấy còn chẳng nhận ra bạn đã biến mất.</p>
<p>No demand. No pricing power.</p>
<p>Thế nên t không tin zero effort là một universally optimal strategy.</p>
<p>Và cái belief rằng người bỏ nhiều effort hơn chắc chắn có perceived value thấp hơn cũng không phải một quy luật.</p>
<p>Một người có thể đầu tư rất nhiều vào relationship vì họ thật lòng thích đối phương, chứ không phải vì họ có ít options hơn.</p>
<p>Ngược lại, có người gần như không bỏ effort đơn giản vì họ chẳng quan tâm, chứ không phải vì họ high-value.</p>
<p>Nhưng t vẫn nghĩ concept về allocation of effort rất đáng bàn.</p>
<p>T có thể thích một cô gái, chủ động rủ cô ấy đi chơi, nhưng nếu mọi interaction đều chỉ có t cố gắng, t cần đặt câu hỏi liệu có nên tiếp tục đầu tư hay không.</p>
<p>Không phải vì t muốn manipulate cô ấy bằng artificial scarcity.</p>
<p>Mà vì t không thể tiếp tục allocate unlimited resources vào một position không có tín hiệu reciprocation.</p>
<p>Sounds familiar?</p>
<p>That's the quant mindset.</p>
<p>If I can't maximize the return, I'll minimize the loss.</p>
<p>Nhưng dating có một điểm khác với financial market.</p>
<p>Một cổ phiếu không quan tâm bạn có thích nó hay không. Nó không cảm thấy vui vì được bạn chọn, cũng chẳng buồn khi bạn quyết định bán.</p>
<p>Con người thì khác.</p>
<p>Nếu cả hai cùng cố tình không nhắn trước để tăng perceived value, cuối cùng sẽ có hai người ngồi nhìn điện thoại, mỗi người đều tin rằng mình đang thắng một cái game chẳng ai thực sự muốn chơi.</p>
<p>A very efficient strategy for achieving absolutely nothing.</p>
<p>Congratulations.</p>
<p>You've optimized your dating game into zero dates.</p>
<p>## Poker Theory</p>
<p>Okay, let's talk about poker. T từng xem một video khá thú vị của Lit Nomad, trong đó ông ấy nói về những similarities giữa poker, quant trading và dating,</p>
<p>Một trong những thứ khiến t thích poker là nó không chỉ là một trò chơi về xác suất. Nó còn là một trò chơi về information asymmetry, risk management, expected utility và cách bạn ra quyết định khi không thực sự biết đối phương đang cầm quân gì.</p>
<p>Sounds familiar?</p>
<p>Trong dating cũng vậy. Bạn không thực sự biết cô gái kia đang nghĩ gì về mình, cô ấy có bao nhiêu options, hay liệu việc mình vừa bỏ ra hai triệu cho một bữa tối có thực sự improve được cơ hội gặp lại cô ấy hay không.</p>
<p>Bạn chỉ có một vài observations, một ít signals, và rất nhiều uncertainty.</p>
<p>Và như mọi khi, t nghĩ có thể ngồi link rất nhiều concept để build một strategy có thể giúp t chiến thắng trên cả bàn pokers và trên thị trường hẹn hò.</p>
<p>## Short-stack Play — Exposure to Variance</p>
<p>Đầu tiên là *short-stack play*.</p>
<p>Trong poker tournament, khi bạn chỉ còn rất ít chips và sắp bị blinds ăn hết stack, việc tiếp tục chơi quá an toàn đôi khi chẳng còn ý nghĩa. Bạn phải lựa chọn một cơ hội phù hợp để shove or fold, bởi nếu cứ ngồi chờ một hand đủ đẹp, có khi bạn đã bị eliminated trước cả khi nó xuất hiện.</p>
<p>Dating cũng có những tình huống khá giống vậy.</p>
<p>Giả sử bạn đang theo đuổi một cô gái, nhưng càng ngày càng cảm thấy cô ấy mất interest. Những tin nhắn bắt đầu ngắn dần, response time tăng lên, và những lời mời đi chơi liên tục bị từ chối.</p>
<p>You're slowly getting blinded out.</p>
<p>Bạn có thể tiếp tục play safe, nhắn những câu xã giao vô thưởng vô phạt và chờ cái connection ấy từ từ biến mất.</p>
<p>Hoặc bạn có thể làm một việc khác.</p>
<p>**Expose yourself to variance.**</p>
<p>Lit Nomad đưa ra một ví dụ mà t thấy vừa buồn cười vừa khá genius.</p>
<p>Giả sử bạn đang date một cô gái trẻ, tốt nghiệp đại học, có vẻ khá progressive. Bạn cảm thấy mình sắp bị reject, và cơ hội cứu vãn gần như bằng không.</p>
<p>Thay vì cố gắng làm mọi thứ thật perfect để lấy lòng cô ấy, bạn quyết định xuất hiện trong buổi hẹn tiếp theo với một cái MAGA hat ủng hộ Trump.</p>
<p>Yes. A Trump MAGA hat.</p>
<p>Và khi cô ấy nhìn bạn với vẻ mặt khó hiểu, bạn bắt đầu giải thích rất tự tin rằng mình có quyền thể hiện political beliefs và sẽ không thay đổi bản thân chỉ để làm hài lòng người khác.</p>
<p>Now, what happens?</p>
<p>Theo cái hypothetical scenario của Lit Nomad, có tới 95% khả năng cô ấy sẽ thấy bạn cực kỳ kỳ quặc, thậm chí repulsive, rồi quyết định chẳng bao giờ gặp lại.</p>
<p>Nhưng có 5% khả năng cô ấy lại là một secret Trump supporter, hoặc ít nhất cảm thấy ấn tượng với sự tự tin và cái attitude chẳng quan tâm người khác nghĩ gì của bạn.</p>
<p>Suddenly, you're back in the game.</p>
<p>Đương nhiên 95% và 5% chỉ là những con số illustrative mà Lit Nomad đưa ra, không phải một statistical finding nào cả.</p>
<p>Nhưng t thích cái mathematical intuition đằng sau nó.</p>
<p>Khi bạn đang nắm một position gần như chắc chắn thua, một strategy có high variance đôi khi lại hấp dẫn hơn việc tiếp tục chấp nhận một cái outcome đang dần tiến về zero.</p>
<p>Trong poker, nếu bạn chỉ còn vài chips, downside của việc all-in bị giới hạn bởi số chips còn lại. Nhưng upside, nếu thắng, có thể đủ lớn để đưa bạn quay trở lại tournament.</p>
<p>Trong finance, nó hơi giống một call option.</p>
<p>Bạn có một limited downside, nhưng vẫn giữ được exposure với một potential upside đáng kể.</p>
<p>Nếu cứ tiếp tục chơi safe, bạn có thể đang bảo vệ một position vốn chẳng còn bao nhiêu value.</p>
<p>Còn khi expose yourself to variance, bạn chấp nhận một xác suất thua rất cao để đổi lấy cơ hội tạo ra một outcome mà strategy cũ gần như không thể mang lại.</p>
<p>Tất nhiên, high variance không tự động đồng nghĩa với positive expected value. Nếu upside không đủ lớn, hoặc downside thực ra vẫn còn đáng kể, thì bạn chỉ đang gamble một cách ngu ngốc.</p>
<p>Và dating cũng chẳng phải poker. Một cái MAGA hat có thể khiến bạn mất cơ hội, khiến người khác khó chịu, hoặc tạo ra một ấn tượng sai lệch về con người thật của mình.</p>
<p>Nhưng cái point ở đây không nhất thiết là phải đội MAGA hat, hay cố tình gây shock bằng một political opinion mà mình thậm chí chẳng tin.</p>
<p>Nó là việc dám thực hiện một action có khả năng thay đổi outcome, thay vì cứ tiếp tục một strategy mà bạn đã có đủ observations để biết rằng nó không hiệu quả.</p>
<p>Có thể là chủ động rủ cô ấy đi một buổi hẹn khác biệt hơn, nói thẳng một điều mà trước giờ bạn ngại nói, hoặc đơn giản là thể hiện một khía cạnh chân thật nhưng hơi unusual của bản thân.</p>
<p>Một move có thể khiến người kia thích bạn hơn, hoặc nhận ra hai người thực sự chẳng phù hợp.</p>
<p>Either way, you get new information.</p>
<p>T thấy concept này khá thú vị vì nó gần như đi ngược lại cái quant mindset mà t luôn tự hào.</p>
<p>T có thói quen minimize exposure, control downside và chuẩn bị exit strategy trước khi làm bất cứ chuyện gì.</p>
<p>Nhưng đôi khi, khi downside đã gần chạm đáy, việc tiếp tục minimize variance chẳng còn giúp mình đạt được điều gì nữa.</p>
<p>**You can't win a tournament by folding every hand.**</p>
<p>Và có lẽ trong dating cũng vậy.</p>
<p>Đôi khi bạn phải chấp nhận một xác suất bị reject để có cơ hội đạt được outcome mình muốn.</p>
<p>Không phải cứ all-in là thông minh.</p>
<p>Nhưng một thằng không bao giờ dám bet thì cũng chẳng thể thắng được pot nào.</p>
<p>Anyway, nếu short-stack play là cách bạn xử lý một position sắp thua, thì có một concept khác trong poker giúp bạn biết mình đang đứng ở đâu trước khi quyết định bet thêm.</p>
<p>It's called the *feeler bet*.</p>
<p>## The Feeler Bet</p>
<p>Trong poker, đôi khi bạn thực hiện một bet nhỏ không chỉ để thắng pot, mà còn để tìm hiểu cách đối phương phản ứng, từ đó update estimate về range của họ.</p>
<p>Liên hệ nó với chuyện dating, giả sử bạn vừa đi first date với một cô gái. Buổi tối khá vui, hai người nói chuyện được vài tiếng, nhưng bạn vẫn không thực sự biết cô ấy có muốn gặp lại mình hay không.</p>
<p>Bạn có thể ngồi phân tích hàng trăm signals.</p>
<p>Cô ấy có cười nhiều không? Có hỏi về công việc của bạn không? Lúc về có nhắn tin trước không? Có sử dụng emoji trong tin nhắn không?</p>
<p>Hoặc bạn có thể thực hiện một cái probe rất đơn giản.</p>
<p>"Hey, I had fun tonight. Wanna grab coffee this weekend?"</p>
<p>Small investment. New information.</p>
<p>Nếu cô ấy đồng ý và chủ động chọn thời gian, đó là một positive signal.</p>
<p>Nếu cô ấy bận nhưng đề xuất một ngày khác, cũng là một signal đáng chú ý.</p>
<p>Còn nếu cô ấy liên tục từ chối và không hề muốn tìm một alternative, thì có lẽ bạn đã có thêm lý do để update prior của mình.</p>
<p>Tất nhiên một observation không phải proof. Có những người không giỏi nhắn tin, có người thực sự bận, và cũng có người cần thêm thời gian để hiểu người khác.</p>
<p>Nhưng thay vì ngồi guessing mãi, một lời mời rõ ràng đôi khi đem lại nhiều information hơn cả trăm cái emoji.</p>
<p>Lit Nomad còn đề xuất quan sát những metrics như text length ratio, response time, tỷ lệ tin nhắn được gửi và nhận, hay mức độ chủ động của mỗi người.</p>
<p>Và t phải công nhận, với tư cách một data scientist, t thấy cái idea ấy khá hấp dẫn.</p>
<p>Imagine building an attraction classifier from text messages. Một cái app tên là Are They Into You?</p>
<p>Input: text messages.</p>
<p>Output: attraction probability.</p>
<p>Model confidence: questionable.</p>
<p>Features có thể bao gồm số lần hai người chủ động bắt đầu conversation, số câu hỏi được đặt ra, mức độ reciprocation hay tần suất chủ động đề xuất gặp nhau.</p>
<p>Nhưng reply time bằng nhau không có nghĩa attraction bằng nhau. Một người có thể trả lời rất nhanh vì đang rảnh, hoặc rất chậm vì công việc bận rộn.</p>
<p>Và một cái model đọc tin nhắn cũng không thể tự hiểu toàn bộ relationship context, chưa kể những vấn đề về privacy nếu đem private conversations đi phân tích mà chưa có sự đồng ý.</p>
<p>Still, the concept is interesting.</p>
<p>Instead of assuming you know someone's preferences, make an observation and update your prediction.</p>
<p>That's literally what Bayesian thinking is about.</p>
<p>## Continuation Bet</p>
<p>There ss another concept in pokers i think it's very related to dating, Continuation bet.</p>
<p>Trong poker, sau khi là người raise ở vòng trước, bạn có thể tiếp tục bet ở vòng tiếp theo trong những tình huống phù hợp, kể cả khi bài của mình chưa thực sự mạnh.</p>
<p>Điều thú vị là đôi khi người ta ngại bet không phải vì nó có negative expected value, mà vì họ sợ bị call hoặc raise khi đang bluff.</p>
<p>Basically, their ego gets in the way.</p>
<p>Trong dating cũng vậy.</p>
<p>Rất nhiều người không dám chủ động rủ người mình thích đi chơi vì sợ bị từ chối.</p>
<p>Họ sợ mất mặt, sợ người khác biết mình bị reject, hay đơn giản là không muốn nhận một cái outcome bằng 0.</p>
<p>Nhưng nếu không bao giờ hỏi thì probability of getting a date thông qua lời mời ấy cũng bằng 0.</p>
<p>You miss every shot you don't take.</p>
<p>T nghĩ có một sự khác biệt lớn giữa việc sợ thua và việc chơi để thắng.</p>
<p>Nếu t thực sự thích một cô gái, và cost của việc hỏi cô ấy có muốn đi cà phê không tương đối nhỏ, tại sao t lại không thử?</p>
<p>Worst case, she says no.</p>
<p>Of course, there's an emotional cost. Rejection chẳng bao giờ hoàn toàn miễn phí.</p>
<p>Nhưng nếu chỉ vì sợ một lần bị từ chối mà không bao giờ thực hiện action nào, bạn có thể đang minimize losses bằng cách eliminate luôn cả potential returns.</p>
<p>Và đấy là lúc t thấy cái poker analogy này còn liên quan tới chính mình.</p>
<p>T luôn thích control exposure. Tính risk budget, estimate downside, chuẩn bị exit strategy trước khi bước vào một chuyện gì đó.</p>
<p>Nhưng đôi khi, chính việc quá tập trung vào protecting downside khiến t quên mất rằng muốn thắng thì trước hết phải chấp nhận một xác suất thua nào đó.</p>
<p>Không phải cứ all-in là thông minh.</p>
<p>Nhưng fold every hand cũng chẳng phải một winning strategy.</p>
<p>## Don't Play Your Cards. Play the Player.</p>
<p>Có một câu nói rất nổi tiếng trong poker.</p>
<p>Don't play your cards. Play the player.</p>
<p>Trong dating, cái cards của bạn có thể là appearance, intelligence, money, status và những thứ mà t đã cố quantify bằng SMV ở đầu chương.</p>
<p>Nhưng sở hữu một bộ features đủ đẹp không đảm bảo rằng cô gái kia sẽ thích bạn.</p>
<p>Bởi vì còn một variable khác.</p>
<p>Her preferences.</p>
<p>Một cô gái có thể thích những người cực kỳ ambitious, còn một người khác chỉ muốn một partner có nhiều thời gian dành cho gia đình.</p>
<p>Có người thích fine dining. Có người lại thích cùng nhau khám phá một quán cà phê nhỏ hay đi dạo quanh thành phố.</p>
<p>Vậy nên một strategy thành công với người này chưa chắc có tác dụng với người khác.</p>
<p>T nghĩ đây mới là điều đáng học từ poker: thay vì chỉ cố improve hand strength của mình, hãy tìm hiểu người mà mình đang thực sự tương tác.</p>
<p>Nhưng t không nghĩ điều đó có nghĩa là phải giả vờ trở thành đúng kiểu người cô ấy muốn.</p>
<p>Trong poker, bạn có thể bluff.</p>
<p>Dating thì phức tạp hơn, vì một cái bluff thành công ở first date có thể trở thành một lời nói dối mà bạn phải duy trì trong cả relationship.</p>
<p>Giả vờ giàu hơn, thông minh hơn hay sống một cuộc đời thú vị hơn mình thực sự có thể giúp bạn tạo first impression tốt hơn trong một vài phút.</p>
<p>Nhưng sau đó thì sao?</p>
<p>Bạn sẽ phải maintain cả cái character ấy.</p>
<p>Sounds exhausting.</p>
<p>Và có lẽ đó là một khoản investment còn đắt hơn bất cứ bữa tối nào.</p>
<p>## The First Date Algorithm</p>
<p>Okay, enough theory.</p>
<p>Let's get practical.</p>
<p>Giả sử sau tất cả những theory vừa rồi, bạn tìm được một cô gái mà mình thực sự muốn đi chơi cùng.</p>
<p>Từng có một thời gian t nghĩ cách optimize ngân sách của một buổi hẹn cũng rất đơn giản.</p>
<p>Look at the girl, estimate her attractiveness, then decide how much you're willing to spend.</p>
<p>Một triệu, ba triệu hay mười triệu.</p>
<p>T còn từng nghĩ nhan sắc càng cao thì mình càng dễ cảm thấy một bữa tối đắt tiền là worth it.</p>
<p>Nghe khá giống investment analysis nhỉ.</p>
<p>Có điều sau cái sigmoid model vừa rồi, rõ ràng việc maximize spending không hẳn là optimal strategy.</p>
<p>Bởi vì bản thân việc được ngồi ăn tối với ai đó chưa chắc phụ thuộc vào số tiền bạn bỏ ra.</p>
<p>Và đôi khi, bạn còn chẳng cần nghĩ nhiều đến thế.</p>
<p>T nhớ từng có một cuộc nói chuyện khá buồn cười với một thằng bạn.</p>
<p>Nó hỏi t có chắc mình muốn rủ một cô gái đi chơi không.</p>
<p>"Are you sure?"</p>
<p>"Absolutely."</p>
<p>"Sao mày nghĩ cô ấy sẽ đồng ý?"</p>
<p>"Why not?"</p>
<p>"Không, tao đang hỏi tại sao cô ấy muốn đi chơi với mày?"</p>
<p>"Yeah. Why not? That's my answer."</p>
<p>Nó nhìn t như thể vừa nghe một cái regression model không có dependent variable.</p>
<p>T bắt đầu giải thích.</p>
<p>Cô ấy được đi ăn một bữa tối mà không phải trả tiền. Có một người ngồi nghe cô ấy yapping cả buổi. Và quan trọng nhất, cô ấy được hang out với một người như t.</p>
<p>I'm funny, you know.</p>
<p>Nó hỏi tiếp:</p>
<p>"À, còn được đi với một thằng đẹp trai nữa nhỉ?"</p>
<p>"Exactly! You got it now."</p>
<p>T nói với vẻ mặt như vừa đặt dấu chấm cuối cùng cho một mathematical proof.</p>
<p>Nhưng sau đó t nhận ra hai đứa đang giải hai bài toán khác nhau.</p>
<p>Nó hỏi why would she say yes?</p>
<p>T lại hỏi why would she say no?</p>
<p>Nó muốn tìm evidence rằng cô ấy có demand đối với t.</p>
<p>Còn t đang tìm cách remove friction khỏi một cái conversion funnel.</p>
<p>Nếu cô ấy ngại mất tiền, dinner is on me.</p>
<p>Nếu địa điểm quá xa, t chọn một nơi khác.</p>
<p>Nếu sợ buổi tối awkward, t có thể chủ động trò chuyện.</p>
<p>Nếu cô ấy muốn ăn gì đó, t có thể tìm một chỗ phù hợp.</p>
<p>T đang optimize những điều kiện khiến lời mời trở nên dễ chấp nhận hơn.</p>
<p>Nhưng thằng bạn t hỏi một câu mà toàn bộ optimization ấy chưa thực sự trả lời.</p>
<p>Does she actually want to spend time with you?</p>
<p>Và đúng là có những thứ không thể giải quyết chỉ bằng cách remove blockers.</p>
<p>Một người có thể hoàn toàn rảnh, không phải trả tiền, địa điểm lại ngay gần nhà, nhưng vẫn chẳng muốn đi ăn tối với bạn.</p>
<p>Not because your offer is bad.</p>
<p>Maybe there's simply no attraction.</p>
<p>Đấy chính là sự khác biệt giữa demand validation và conversion optimization.</p>
<p>Và nếu có một điều t rút ra từ việc nghĩ quá nhiều về dating, thì đó là mình nên giải đúng bài toán trước khi optimize nó.</p>
<p>Dù vậy, t vẫn thích nghĩ về dating như một data pipeline.</p>
<p>Job 01 là first date.</p>
<p>Input gồm hai người chưa hiểu nhau đủ, một bữa tối và rất nhiều uncertainty.</p>
<p>Output không phải việc bạn đã thuyết phục được cô ấy đồng ý đi chơi.</p>
<p>Output tốt nhất là cả hai có một buổi tối vui vẻ và đều muốn gặp lại.</p>
<p>Job 01 successful?</p>
<p>Trigger Job 02.</p>
<p>Có thể là cà phê, một bộ phim, đi dạo, hoặc một activity nào đó mà cả hai đều thích.</p>
<p>Job 02 successful?</p>
<p>Trigger Job 03.</p>
<p>Cứ thế.</p>
<p>Don't overengineer your wedding before finishing the first dinner.</p>
<p>Và nếu một người không muốn tiếp tục, đó không phải transient error để bạn retry thêm mười lần.</p>
<p>Pipeline ends.</p>
<p>T thích approach này vì thay vì cố predict toàn bộ future từ vài bức ảnh trên Tinder, t có thể update model bằng observations sau mỗi interaction.</p>
<p>Trên profile, cô ấy có thể nói mình thích những người thông minh, hài hước, thành công và có chiều sâu.</p>
<p>Nhưng lúc hai người gặp nhau, đôi khi chemistry chẳng tuân theo bất kỳ feature importance nào mà chúng ta đã estimate.</p>
<p>Eastwick và Finkel từng có nghiên cứu speed-dating cho thấy những preferences mà người tham gia tuyên bố trước đó không dự đoán tốt điều gì khiến họ thực sự muốn một người sau khi gặp mặt.</p>
<p>Càng thú vị hơn khi t nghĩ chính mình cũng có thể rơi vào cái bias ấy.</p>
<p>T có thể ngồi một buổi để rank appearance, intelligence, money, status, rồi tự tin nói rằng mình biết chính xác mẫu người mình thích.</p>
<p>Nhưng sau đó lại gặp một cô gái mà mọi thứ trên giấy chẳng có gì quá đặc biệt, và chẳng hiểu sao vẫn muốn nói chuyện với cô ấy tới tận lúc quán đóng cửa.</p>
<p>Vậy nên có lẽ cái original SMV function của t cũng cần thêm vài features.</p>
<p>Hoặc t đã assign sai weights ngay từ đầu.</p>
<p>## The Objective Function</p>
<p>Sau cả đống evolutionary biology, game theory, Tinder analytics, logistic regression và asset pricing, cuối cùng t vẫn phải quay về một câu hỏi khá đơn giản.</p>
<p>What am I actually optimizing for?</p>
<p>Nếu mục tiêu chỉ là getting matches, t có thể optimize profile pictures.</p>
<p>Nếu muốn nhiều first dates, t có thể improve messaging strategy và reduce friction.</p>
<p>Nếu muốn một cô gái chủ động chase mình, t có thể thử tạo uncertainty hoặc artificial scarcity.</p>
<p>Nhưng nếu t thực sự muốn một relationship thì sao?</p>
<p>T nghĩ cái objective function lúc ấy phải khác.</p>
<p>Appearance tất nhiên vẫn quan trọng. T cũng chẳng giả vờ nói rằng mình không quan tâm tới ngoại hình.</p>
<p>Đương nhiên vẫn phải xinh chứ, lol.</p>
<p>Nhưng nếu phải assign weights, t nghĩ intelligence và intellectual compatibility mới là hai features mà t coi trọng hơn.</p>
<p>Liệu cô ấy có thể ngồi với t cả buổi để nói về philosophy, science, history, economics, conspiracy theories hay những thứ random mà hai đứa vừa đọc được trên internet hay không?</p>
<p>Liệu cô ấy có thể challenge một cái theory của t, chỉ ra tại sao cái logic nghe rất hợp lý ấy thực ra lại sai?</p>
<p>Liệu t có thể kể một câu chuyện rất dài, rất nerdy, mà cô ấy vẫn thực sự muốn nghe, không phải vì lịch sự, cũng chẳng phải vì cô ấy đang cố impress t?</p>
<p>Và ngược lại, liệu t có đủ tò mò để hiểu thế giới của cô ấy, thay vì lúc nào cũng cố explain nó bằng models của mình?</p>
<p>T nghĩ những thứ ấy quan trọng hơn nhiều so với việc cô ấy được bao nhiêu điểm trên một cái SMV scale mà chính t tạo ra.</p>
<p>Có lẽ sau tất cả, thứ t muốn không phải một người có perceived market value cao nhất.</p>
<p>Mà là một người khiến t cảm thấy việc dành thời gian cho cô ấy chưa bao giờ giống một khoản investment phải tính toán.</p>
<p>Một buổi tối ăn pizza trên sofa, nói đủ thứ chuyện trên đời.</p>
<p>No fancy restaurant. No artificial scarcity. No need to play hard to get.</p>
<p>Just two people who genuinely want to be there.</p>
<p>Tất nhiên, t vẫn sẽ tiếp tục build models. It's literally what I do.</p>
<p>Nhưng có một điều mà t nghĩ mình bắt đầu hiểu.</p>
<p>A model can optimize a metric perfectly and still miss the entire point.</p>
<p>Anyway.</p>
<p>Thank you for coming to my TED Talk.</p></td><td valign="top"><p>Let a data scientist teach you how to optimize your dating game.</p>
<p>It's all based on a metric called SMV (Sexual Market Value), and this value is perceived differently between genders.</p>
<p>Suppose we have a few factors: appearance, intelligence, status, money… For men, I'd argue that money and status account for 70% of the total weight, while for women, appearance alone accounts for 90%.</p>
<p>From there, you can easily estimate your value and the girl's value. And the game is simple: you want to date up, right?</p>
<p>I mean, why would you date a girl with a lower SMV than yours? You're basically downgrading your own position in the dating market. Think of it like investing in a financial asset. Why would you allocate your resources to a lower-return investment when you could get a better one?</p>
<p>But here's the catch.</p>
<p>If you date a girl whose perceived value is significantly higher than yours, there's a possibility she's only settling for you because she couldn't find a better option. And if that's the case, she might eventually start to undermine you, lose respect for you, or constantly compare you with the alternatives she thinks she deserves.</p>
<p>That's my rather brutal interpretation of female mate selection.</p>
<p>So what's the optimal strategy?</p>
<p>Find someone whose perceived value is roughly equivalent to yours. Neither player has a strong incentive to seek a better alternative, and both are getting a fair deal.</p>
<p>That's what I called Nash equilibrium.</p>
<p>Simple as that.</p>
<p>Welcome to my TED Talk on dating.</p>
<p>Đôi lúc t tự hỏi mình thích cái dating model này vì nó predict được điều gì, hay vì nó giúp t không phải nói ra một thứ đơn giản hơn nhiều: t sợ bị đem ra so sánh với một người khác. Một bảng điểm nghe lạnh lùng và scientific hơn câu ‘t không muốn là lựa chọn dự phòng của ai đó’. But a better vocabulary doesn't automatically mean a better theory.</p>
<p>Một bài hát về fake love có thể làm t gật gù như thể người viết vừa đọc được hết history của mình. Nhưng đó vẫn là một bài hát, không phải dataset. T có thể relate tới một câu chuyện mà chẳng cần biến nó thành kết luận về tất cả phụ nữ trên thế giới.</p>
<p>T vừa giải thích tình yêu bằng một scoring function, vài weights và Nash equilibrium. Một vấn đề mà nhân loại vật lộn hàng nghìn năm, t xử lý trong đúng một paragraph.</p>
<p>You're welcome.</p>
<p>Và trước khi các bạn bắt đầu hỏi 70% và 90% kia đến từ đâu, nguồn dataset nào, sample size bao nhiêu, p-value có significant không — please, hold your questions until the end.</p>
<p>First, a little evolutionary biology.</p>
<p>Có một lý do khiến tôi thích đặt những giả thuyết khó chịu về mating strategies. Robert Trivers có Parental Investment Theory: ở nhiều loài, giới đầu tư nhiều hơn vào việc tạo và nuôi con có thể chịu những áp lực lựa chọn bạn tình khác biệt. Con người không giống một mô hình sinh học tối giản, nhưng nó gợi ra một câu hỏi về incentives: khi cost và risk khác nhau, hai players có nhất thiết dùng cùng strategy không?</p>
<p>Các nghiên cứu cross-cultural về mate preferences của David Buss từng tìm thấy những khác biệt trung bình giữa nam và nữ trong mức độ coi trọng ngoại hình và khả năng kiếm nguồn lực. Lịch sử cũng có những xã hội cho phép đa thê, thậm chí hậu cung của hoàng đế, nơi quyền lực và cơ hội sinh sản gắn với nhau. Nhưng trung bình của một mẫu không phải tính cách của một cá nhân. Và hậu cung không phải Tinder: quyền lực chính trị, ép buộc và trật tự xã hội đều có mặt trong câu chuyện.</p>
<p>Harari trong Sapiens khiến tôi hứng thú với chính khoảng giao nhau giữa sinh học và trật tự do con người tạo ra. Những gì ta gọi là 'natural' đôi khi đã qua vô số lớp văn hóa và thể chế. Thú vị là tôi có thể đọc những điều ấy rồi vẫn tự tin nhét toàn bộ con người vào bốn features và hai bộ weight bịa ra trong một buổi chiều.</p>
<p>70% và 90% không phải evidence. They're hyperparameters. Assigned by Jason, peer-reviewed by Jason, approved by Jason.</p>
<p>Còn Nash equilibrium? Tôi dùng từ ấy rất hào hứng. Nhưng hai người có cùng SMV không tự động tạo ra Nash equilibrium. Đúng nghĩa game theory, equilibrium liên quan tới những chiến lược mà không ai muốn đơn phương đổi khi người kia giữ nguyên. Cái tôi đang mô tả có lẽ gần một matching problem hơn. Có lẽ ngay từ đầu tôi đã trộn game theory với một trò xếp hạng người yêu.</p>
<p>## The Dating Game</p>
<p>Okay, có một chuyện khá buồn cười ở đây. Trong lúc tôi tự nhận mình vừa giải xong dating market, một người khác đã đem gần như cùng một mô hình lên bảng. Professor Jiang Xueqin, trong bài giảng Game Theory #1: The Dating Game, lấy năm người đàn ông và năm người phụ nữ, rồi xếp mỗi bên từ 1 đến 5 dựa trên genes, wealth và status.</p>
<p>Nếu tất cả đều muốn người top-ranked, người đàn ông số 5 có thể muốn theo đuổi cả năm người. Nhưng lúc ấy, những players còn lại đâu có đứng yên chờ được chọn. Họ đổi strategy. Người ta có thể chọn một partner ít nổi bật hơn nhưng đáng tin cậy hơn, và cuối cùng gã số 5, vì muốn maximize mọi cơ hội, lại có nguy cơ chẳng giữ được điều mình muốn nhất.</p>
<p>Trong minh họa của Jiang, các cặp 5–5, 4–4, 3–3, 2–2, 1–1 tạo ra một phương án hợp tác. Ông gọi nó là Nash equilibrium. Strictly speaking, xếp hạng bằng nhau chưa đủ để chứng minh equilibrium nếu ta chưa định nghĩa đầy đủ payoffs và deviations. Nhưng cái point của ông thì hay: your best move depends on what everybody else is going to do.</p>
<p>Ông còn kể một bài tập trên lớp: hỏi sinh viên rằng nếu đã ba mươi tuổi và rất muốn kết hôn, họ cần điều kiện tối thiểu gì ở partner. Câu trả lời của các bạn nam và nữ trong lớp được ông dùng để bàn về incentives. Fun story, nhưng đấy là một classroom anecdote, không phải randomized controlled trial.</p>
<p>Có điều Professor Jiang có một cái bảng trắng. Jason thì có Tinder.</p>
<p>## The Tinder Experiment</p>
<p>T từng đem chính cái model ấy ra đối chiếu với một bộ data nhỏ: 10 Tinder profiles, gồm năm thằng bạn và năm cô bạn gái của t.</p>
<p>Five guys. Five girls. A very questionable research grant of exactly zero dollars.</p>
<p>T bắt đầu bằng cách chấm mỗi profile trên thang 1 đến 10. T gọi chỉ số ấy là perceived visual SMV — không phải giá trị của một con người, cũng chẳng phải SMV thật trong đời sống, mà là điểm hấp dẫn chủ quan mà một người xem có thể gán cho cách profile được trình bày trên app: ảnh đại diện, outfit, expression, cách chọn góc chụp, overall vibe và first impression.</p>
<p>Một người ngoài đời rất cuốn hút có thể lên ảnh cực kỳ nhạt nhẽo. Một người chụp ảnh đẹp chưa chắc nói chuyện thú vị. Cho nên 8/10 ở đây có nghĩa là “Jason nhìn profile này và chấm 8”, chứ không phải “người này có giá trị bằng 8”.</p>
<p>Scientific rigor, ladies and gentlemen.</p>
<p>T gắn nhãn M1 đến M5 và F1 đến F5, rồi muốn nhìn vào từng bước của funnel: bao nhiêu lượt swipe right, bao nhiêu match, tỷ lệ match trên số likes đã gửi, ai chủ động nhắn trước, bao nhiêu cuộc trò chuyện thực sự tiếp tục sau lời chào đầu tiên.</p>
<p>Vì sao phải tách chúng ra? Bởi vì getting liked, getting matched, và being worth meeting again là ba outcome khác nhau. Bạn có thể có rất nhiều matches mà chẳng có nổi một cuộc nói chuyện ra hồn. Cũng có thể có rất ít matches, nhưng mỗi cuộc trò chuyện lại đáng để tiếp tục.</p>
<p>Đương nhiên, N = 10 là một sample size đáng xấu hổ nếu muốn generalize cho toàn bộ dating market, và không ai có thể dùng dataset này để công bố quy luật về toàn bộ đàn ông và phụ nữ. Chưa kể Tinder algorithm còn quyết định profile nào được hiển thị cho ai, vào thời điểm nào. Tuổi, địa điểm, hình ảnh và cách mỗi người swipe đều có thể là confounding variables. Cái perceived SMV score lại còn do chính t chấm. Biased as hell.</p>
<p>Nhưng nếu coi nó như một observational case study về những người t biết, thì đây là một experiment đủ thú vị để đặt ra câu hỏi. Nó cho tôi cơ hội kiểm tra xem cái lý thuyết về attraction mà tôi vừa hùng hồn giảng có chịu nổi một chút real-world data hay không.</p>
<p>T cũng đọc một nghiên cứu field experiment trên Tinder với 3.600 profile evaluations: trong mẫu nghiên cứu ấy, phụ nữ có xu hướng chọn lọc hơn và quan tâm đến trình độ học vấn của nam giới; nghiên cứu không tìm thấy bằng chứng đàn ông né tránh những phụ nữ có học vấn cao. Nói cách khác, đời thực có một vài pattern đáng nghiên cứu, nhưng nó chẳng ngoan ngoãn biến thành hai con số 70% và 90% của tôi.</p>
<p>That's the difference between a model you like and a model the data actually supports.</p>
<p>Nhưng sau Tinder, t lại có thêm một câu hỏi.</p>
<p>Giả sử bạn đã match với một cô gái. Giả sử cô ấy cũng có một chút interest với bạn.</p>
<p>How much effort should you actually invest to make her like you?</p>
<p>## The Marginal Cost of Attraction</p>
<p>Okay, let's talk about diminishing marginal returns. T nghĩ có một thứ khá thú vị về dating mà mọi người thường overlook.</p>
<p>Giả sử t build một logistic regression model để predict liệu một cô gái có thích bạn hay không.</p>
<p>Outcome được define rất đơn giản:</p>
<p>Y = 1: She likes you.</p>
<p>Y = 0: She doesn't.</p>
<p>Đương nhiên attraction ngoài đời là cả một spectrum, chứ chẳng có cái switch on/off nào trong đầu con người. Nhưng vì t đang muốn giải một binary classification problem nên cứ tạm simplify nó như vậy.</p>
<p>T sử dụng một sigmoid function để estimate probability của outcome.</p>
<p>P(Y = 1) = 1 / (1 + e^(-z))</p>
<p>Trong đó z là một weighted combination của những features ảnh hưởng tới attraction.</p>
<p>Bây giờ thử đơn giản hóa model thêm một chút.</p>
<p>T đặt effort invested lên trục X, bao gồm time, money, attention và emotional investment mà bạn bỏ ra để theo đuổi một cô gái.</p>
<p>Trục Y là probability that she likes you.</p>
<p>Đương nhiên, đây mới chỉ là một hypothetical model, không thể đơn giản cộng một triệu tiền ăn tối với hai tiếng nhắn tin thành một metric được. Và effort chưa chắc đã có positive effect trong mọi trường hợp.</p>
<p>Nhưng giả sử chúng ta đã normalize được effort thành một index, và trong khoảng đang xét, tăng effort giúp tăng attraction probability, thì sigmoid có một property rất thú vị.</p>
<p>Diminishing marginal returns.</p>
<p>Khi probability còn rất thấp, thêm một chút effort có thể chẳng thay đổi được bao nhiêu.</p>
<p>Khi probability đã rất cao, bạn cũng chẳng nhận được bao nhiêu marginal gain từ việc tiếp tục tăng investment.</p>
<p>Sensitivity lớn nhất xuất hiện ở vùng giữa, gần decision boundary.</p>
<p>Bây giờ thử xem một ví dụ nhé.</p>
<p>Giả sử có một cô gái đã rất thích bạn từ trước. Attraction probability trong cái hypothetical model của t đang là 90%.</p>
<p>Bạn đưa cô ấy đi ăn một bữa tối hai triệu.</p>
<p>Maybe it goes up to 92%.</p>
<p>Bạn mua thêm một bó hoa.</p>
<p>Maybe 93%.</p>
<p>Rồi bạn book thêm một nhà hàng fine dining năm triệu, chuẩn bị một outfit chỉn chu, dành cả ngày lên kế hoạch cho buổi hẹn.</p>
<p>Maybe 94%.</p>
<p>Đây là những con số t bịa ra để illustrate thôi, chứ không phải calibrated probabilities nhé.</p>
<p>But you get the idea.</p>
<p>You're already on the right side of the sigmoid.</p>
<p>Bỏ thêm rất nhiều resources chưa chắc tạo ra một improvement tương xứng trong probability.</p>
<p>Và có khi bạn chẳng cần một bữa tối đắt tiền nào cả.</p>
<p>T lấy một ví dụ khá buồn cười.</p>
<p>Giả sử có một cô gái đã rất thích bạn. Một hôm cô ấy muốn qua nhà chơi, và bạn nhắn:</p>
<p>"Hey, on your way here, can you grab us some pizza?"</p>
<p>Cô ấy có thể vui vẻ đáp lại:</p>
<p>"Hahaha, you're funny. What pizza do you want?"</p>
<p>Rồi hai người ngồi ăn pizza trên sofa, xem một bộ phim, kể vài câu chuyện ngớ ngẩn, và có khi đó lại là một buổi tối vui hơn bất cứ cái fine dining restaurant nào.</p>
<p>Bây giờ tưởng tượng bạn nói đúng câu ấy với một cô gái chẳng hứng thú gì với mình.</p>
<p>"Wait, you're inviting me over and asking me to buy you dinner?"</p>
<p>Same guy. Same request. Completely different interpretation.</p>
<p>Tất nhiên cái pizza này không phải một statistical test. Một cô gái có thể không mua pizza đơn giản vì cô ấy bận, không thích pizza, hoặc thấy việc được nhờ mua đồ chẳng liên quan gì tới chuyện mình thích ai.</p>
<p>Nhưng có một point mà t thấy khá hay.</p>
<p>Khi đã có attraction, người ta có thể interpret những hành động của đối phương theo một hướng tích cực hơn.</p>
<p>Một câu đùa nhạt cũng có thể trở nên funny. Một hành động bình thường cũng có thể trở nên đáng yêu.</p>
<p>Và đôi khi, chính việc được làm điều gì đó cho người mình thích cũng khiến bản thân cảm thấy vui.</p>
<p>T muốn gọi đây là một dạng conditional perceived value.</p>
<p>Giá trị mà người ta gán cho một interaction không chỉ phụ thuộc vào action ấy, mà còn phụ thuộc vào prior attraction họ đã có với bạn.</p>
<p>Nói cách khác, t không nghĩ dating là một cái auction, nơi thằng nào chịu chi nhiều nhất thì thắng.</p>
<p>If she's already into you, you don't have to keep raising your bid.</p>
<p>Ngược lại, nếu cô ấy không có chút interest nào từ đầu, bạn cũng không thể assume rằng cứ tăng spending thì sẽ eventually cross được decision boundary.</p>
<p>Một bữa tối mười triệu không tự nhiên biến một người không thích bạn thành một người thích bạn.</p>
<p>Money can buy dinner.</p>
<p>It can't guarantee chemistry.</p>
<p>Và từ đó, t bắt đầu nghĩ tới một theory khác.</p>
<p>Nếu adding effort không nhất thiết tăng attraction, vậy reducing effort có thể khiến mình trở nên attractive hơn hay không?</p>
<p>## The Economics of Attention</p>
<p>Let's talk about asset pricing.</p>
<p>Trong financial market, giá một asset không chỉ phụ thuộc vào intrinsic value, mà còn chịu ảnh hưởng của supply, demand, liquidity và expectations.</p>
<p>Tất nhiên, con người không phải financial assets. Nhưng thử tạm dùng cái analogy ấy để model perceived attention.</p>
<p>Suppose your attention is an asset.</p>
<p>Và giả sử bạn có một lượng thời gian, energy và emotional capacity hữu hạn để phân bổ cho những người khác nhau.</p>
<p>Một thằng lúc nào cũng available, luôn nhắn trước, luôn chủ động lên kế hoạch, thậm chí sẵn sàng cancel những dự định của riêng mình để gặp một cô gái, đang gửi đi một signal rằng attention của nó rất dễ có được.</p>
<p>Trong khi một thằng khác có công việc, hobbies, bạn bè và một cuộc sống riêng đủ thú vị thì không phải lúc nào cũng available.</p>
<p>Same attention. Different scarcity.</p>
<p>Vậy có phải attention của thằng thứ hai sẽ được perceived là valuable hơn?</p>
<p>Maybe.</p>
<p>Và đây là lúc t nghĩ tới một strategy mà chắc nhiều người từng nghe.</p>
<p>Artificial scarcity.</p>
<p>Giả sử bạn thích một cô gái, nhưng thay vì thể hiện interest, bạn cố tình không nhắn trước, không chủ động gặp mặt, thậm chí tỏ ra indifferent.</p>
<p>Mục đích rất đơn giản.</p>
<p>Bạn muốn cô ấy nghĩ rằng attention của mình là một thứ scarce resource, và muốn có được nó thì cô ấy phải bỏ effort.</p>
<p>Basically, reduce supply to increase perceived price.</p>
<p>Economics 101.</p>
<p>Pretty smart, right?</p>
<p>Điều buồn cười là psychology thực sự có một vài nghiên cứu khiến cái theory này nghe không hoàn toàn vô lý.</p>
<p>Năm 2011, Whitchurch và cộng sự thực hiện một experiment, trong đó những nữ sinh viên xem Facebook profiles của một số chàng trai được cho là đã xem profile của họ.</p>
<p>Một nhóm được nói rằng những chàng trai ấy rất thích mình. Một nhóm khác được nói rằng họ chỉ thích ở mức trung bình. Nhóm cuối cùng thì không biết chính xác những chàng trai ấy thích mình nhiều hay vừa phải.</p>
<p>Guess what?</p>
<p>Trong experiment ấy, nhóm uncertain báo cáo mức attraction cao nhất. Họ cũng nghĩ tới những chàng trai ấy nhiều nhất.</p>
<p>Interesting.</p>
<p>Khi không chắc người kia nghĩ gì về mình, đôi khi não bộ lại dành nhiều resources hơn để cố giải thích cái uncertainty ấy.</p>
<p>Nó khiến t liên tưởng tới việc một người cứ mở điện thoại lên kiểm tra xem đối phương đã trả lời chưa, hoặc ngồi phân tích tại sao hôm qua người ấy còn nhắn tin rất nhiệt tình mà hôm nay lại im lặng.</p>
<p>Một cái uncertainty có thể chiếm rất nhiều cognitive bandwidth.</p>
<p>Nhưng trước khi các bạn bắt đầu áp dụng chiến thuật ba ngày không trả lời tin nhắn, có một nghiên cứu khác còn thú vị hơn.</p>
<p>Năm 2014, Dai, Dong và Jia nghiên cứu hiện tượng playing hard to get.</p>
<p>Họ phân biệt hai outcomes mà rất nhiều người thường nhầm lẫn.</p>
<p>Wanting and liking.</p>
<p>Trong các experiments của họ, khi một người đã có psychological commitment với việc theo đuổi đối phương, việc người kia tỏ ra khó có được có thể làm tăng desire to pursue, nhưng lại giảm mức độ liking.</p>
<p>Còn khi chưa có commitment từ trước, playing hard to get có thể làm giảm cả wanting lẫn liking.</p>
<p>Wait a minute.</p>
<p>Vậy tức là bạn có thể khiến một cô gái muốn chase mình nhiều hơn, nhưng chưa chắc cô ấy thực sự thích mình hơn?</p>
<p>Exactly.</p>
<p>Và đây là một classic optimization problem.</p>
<p>Nếu objective function của t chỉ là số lần cô ấy nhắn trước, số lần cô ấy đề nghị gặp hay bao nhiêu effort cô ấy bỏ ra để có được attention của mình, model có thể báo success.</p>
<p>Nhưng relationship quality có khi đang đi xuống.</p>
<p>You've optimized the wrong metric.</p>
<p>Có một nghiên cứu từ năm 1973 của Walster và cộng sự cũng khá hay. Họ phát hiện rằng trong một experiment, người phụ nữ thể hiện sự quan tâm có chọn lọc đối với chính người tham gia được đánh giá hấp dẫn hơn những người luôn dễ có được hoặc khó có được với tất cả mọi người.</p>
<p>T thích cái intuition của nghiên cứu này.</p>
<p>Scarcity không nhất thiết có nghĩa là bạn phải indifferent với người mình thích.</p>
<p>Nó có thể đơn giản là bạn selective.</p>
<p>Bạn không dành attention cho tất cả mọi người, nhưng khi thực sự thích ai đó, bạn vẫn chủ động dành thời gian cho họ.</p>
<p>That's selective scarcity.</p>
<p>Và ở đây có một lỗi economics rất cơ bản mà nhiều người dễ mắc phải.</p>
<p>Scarcity only matters if there's demand.</p>
<p>Giả sử cô gái kia vốn đã thích bạn, việc bạn không phải lúc nào cũng available có thể khiến những lần tương tác trở nên đáng mong đợi hơn trong một số hoàn cảnh.</p>
<p>Nhưng nếu cô ấy chẳng có interest gì với bạn, biến mất ba ngày chưa chắc khiến cô ấy nhớ bạn.</p>
<p>Có khi cô ấy còn chẳng nhận ra bạn đã biến mất.</p>
<p>No demand. No pricing power.</p>
<p>Thế nên t không tin zero effort là một universally optimal strategy.</p>
<p>Và cái belief rằng người bỏ nhiều effort hơn chắc chắn có perceived value thấp hơn cũng không phải một quy luật.</p>
<p>Một người có thể đầu tư rất nhiều vào relationship vì họ thật lòng thích đối phương, chứ không phải vì họ có ít options hơn.</p>
<p>Ngược lại, có người gần như không bỏ effort đơn giản vì họ chẳng quan tâm, chứ không phải vì họ high-value.</p>
<p>Nhưng t vẫn nghĩ concept về allocation of effort rất đáng bàn.</p>
<p>T có thể thích một cô gái, chủ động rủ cô ấy đi chơi, nhưng nếu mọi interaction đều chỉ có t cố gắng, t cần đặt câu hỏi liệu có nên tiếp tục đầu tư hay không.</p>
<p>Không phải vì t muốn manipulate cô ấy bằng artificial scarcity.</p>
<p>Mà vì t không thể tiếp tục allocate unlimited resources vào một position không có tín hiệu reciprocation.</p>
<p>Sounds familiar?</p>
<p>That's the quant mindset.</p>
<p>If I can't maximize the return, I'll minimize the loss.</p>
<p>Nhưng dating có một điểm khác với financial market.</p>
<p>Một cổ phiếu không quan tâm bạn có thích nó hay không. Nó không cảm thấy vui vì được bạn chọn, cũng chẳng buồn khi bạn quyết định bán.</p>
<p>Con người thì khác.</p>
<p>Nếu cả hai cùng cố tình không nhắn trước để tăng perceived value, cuối cùng sẽ có hai người ngồi nhìn điện thoại, mỗi người đều tin rằng mình đang thắng một cái game chẳng ai thực sự muốn chơi.</p>
<p>A very efficient strategy for achieving absolutely nothing.</p>
<p>Congratulations.</p>
<p>You've optimized your dating game into zero dates.</p>
<p>## Poker Theory</p>
<p>Okay, let's talk about poker. T từng xem một video khá thú vị của Lit Nomad, trong đó ông ấy nói về những similarities giữa poker, quant trading và dating,</p>
<p>Một trong những thứ khiến t thích poker là nó không chỉ là một trò chơi về xác suất. Nó còn là một trò chơi về information asymmetry, risk management, expected utility và cách bạn ra quyết định khi không thực sự biết đối phương đang cầm quân gì.</p>
<p>Sounds familiar?</p>
<p>Trong dating cũng vậy. Bạn không thực sự biết cô gái kia đang nghĩ gì về mình, cô ấy có bao nhiêu options, hay liệu việc mình vừa bỏ ra hai triệu cho một bữa tối có thực sự improve được cơ hội gặp lại cô ấy hay không.</p>
<p>Bạn chỉ có một vài observations, một ít signals, và rất nhiều uncertainty.</p>
<p>Và như mọi khi, t nghĩ có thể ngồi link rất nhiều concept để build một strategy có thể giúp t chiến thắng trên cả bàn pokers và trên thị trường hẹn hò.</p>
<p>## Short-stack Play — Exposure to Variance</p>
<p>Đầu tiên là *short-stack play*.</p>
<p>Trong poker tournament, khi bạn chỉ còn rất ít chips và sắp bị blinds ăn hết stack, việc tiếp tục chơi quá an toàn đôi khi chẳng còn ý nghĩa. Bạn phải lựa chọn một cơ hội phù hợp để shove or fold, bởi nếu cứ ngồi chờ một hand đủ đẹp, có khi bạn đã bị eliminated trước cả khi nó xuất hiện.</p>
<p>Dating cũng có những tình huống khá giống vậy.</p>
<p>Giả sử bạn đang theo đuổi một cô gái, nhưng càng ngày càng cảm thấy cô ấy mất interest. Những tin nhắn bắt đầu ngắn dần, response time tăng lên, và những lời mời đi chơi liên tục bị từ chối.</p>
<p>You're slowly getting blinded out.</p>
<p>Bạn có thể tiếp tục play safe, nhắn những câu xã giao vô thưởng vô phạt và chờ cái connection ấy từ từ biến mất.</p>
<p>Hoặc bạn có thể làm một việc khác.</p>
<p>**Expose yourself to variance.**</p>
<p>Lit Nomad đưa ra một ví dụ mà t thấy vừa buồn cười vừa khá genius.</p>
<p>Giả sử bạn đang date một cô gái trẻ, tốt nghiệp đại học, có vẻ khá progressive. Bạn cảm thấy mình sắp bị reject, và cơ hội cứu vãn gần như bằng không.</p>
<p>Thay vì cố gắng làm mọi thứ thật perfect để lấy lòng cô ấy, bạn quyết định xuất hiện trong buổi hẹn tiếp theo với một cái MAGA hat ủng hộ Trump.</p>
<p>Yes. A Trump MAGA hat.</p>
<p>Và khi cô ấy nhìn bạn với vẻ mặt khó hiểu, bạn bắt đầu giải thích rất tự tin rằng mình có quyền thể hiện political beliefs và sẽ không thay đổi bản thân chỉ để làm hài lòng người khác.</p>
<p>Now, what happens?</p>
<p>Theo cái hypothetical scenario của Lit Nomad, có tới 95% khả năng cô ấy sẽ thấy bạn cực kỳ kỳ quặc, thậm chí repulsive, rồi quyết định chẳng bao giờ gặp lại.</p>
<p>Nhưng có 5% khả năng cô ấy lại là một secret Trump supporter, hoặc ít nhất cảm thấy ấn tượng với sự tự tin và cái attitude chẳng quan tâm người khác nghĩ gì của bạn.</p>
<p>Suddenly, you're back in the game.</p>
<p>Đương nhiên 95% và 5% chỉ là những con số illustrative mà Lit Nomad đưa ra, không phải một statistical finding nào cả.</p>
<p>Nhưng t thích cái mathematical intuition đằng sau nó.</p>
<p>Khi bạn đang nắm một position gần như chắc chắn thua, một strategy có high variance đôi khi lại hấp dẫn hơn việc tiếp tục chấp nhận một cái outcome đang dần tiến về zero.</p>
<p>Trong poker, nếu bạn chỉ còn vài chips, downside của việc all-in bị giới hạn bởi số chips còn lại. Nhưng upside, nếu thắng, có thể đủ lớn để đưa bạn quay trở lại tournament.</p>
<p>Trong finance, nó hơi giống một call option.</p>
<p>Bạn có một limited downside, nhưng vẫn giữ được exposure với một potential upside đáng kể.</p>
<p>Nếu cứ tiếp tục chơi safe, bạn có thể đang bảo vệ một position vốn chẳng còn bao nhiêu value.</p>
<p>Còn khi expose yourself to variance, bạn chấp nhận một xác suất thua rất cao để đổi lấy cơ hội tạo ra một outcome mà strategy cũ gần như không thể mang lại.</p>
<p>Tất nhiên, high variance không tự động đồng nghĩa với positive expected value. Nếu upside không đủ lớn, hoặc downside thực ra vẫn còn đáng kể, thì bạn chỉ đang gamble một cách ngu ngốc.</p>
<p>Và dating cũng chẳng phải poker. Một cái MAGA hat có thể khiến bạn mất cơ hội, khiến người khác khó chịu, hoặc tạo ra một ấn tượng sai lệch về con người thật của mình.</p>
<p>Nhưng cái point ở đây không nhất thiết là phải đội MAGA hat, hay cố tình gây shock bằng một political opinion mà mình thậm chí chẳng tin.</p>
<p>Nó là việc dám thực hiện một action có khả năng thay đổi outcome, thay vì cứ tiếp tục một strategy mà bạn đã có đủ observations để biết rằng nó không hiệu quả.</p>
<p>Có thể là chủ động rủ cô ấy đi một buổi hẹn khác biệt hơn, nói thẳng một điều mà trước giờ bạn ngại nói, hoặc đơn giản là thể hiện một khía cạnh chân thật nhưng hơi unusual của bản thân.</p>
<p>Một move có thể khiến người kia thích bạn hơn, hoặc nhận ra hai người thực sự chẳng phù hợp.</p>
<p>Either way, you get new information.</p>
<p>T thấy concept này khá thú vị vì nó gần như đi ngược lại cái quant mindset mà t luôn tự hào.</p>
<p>T có thói quen minimize exposure, control downside và chuẩn bị exit strategy trước khi làm bất cứ chuyện gì.</p>
<p>Nhưng đôi khi, khi downside đã gần chạm đáy, việc tiếp tục minimize variance chẳng còn giúp mình đạt được điều gì nữa.</p>
<p>**You can't win a tournament by folding every hand.**</p>
<p>Và có lẽ trong dating cũng vậy.</p>
<p>Đôi khi bạn phải chấp nhận một xác suất bị reject để có cơ hội đạt được outcome mình muốn.</p>
<p>Không phải cứ all-in là thông minh.</p>
<p>Nhưng một thằng không bao giờ dám bet thì cũng chẳng thể thắng được pot nào.</p>
<p>Anyway, nếu short-stack play là cách bạn xử lý một position sắp thua, thì có một concept khác trong poker giúp bạn biết mình đang đứng ở đâu trước khi quyết định bet thêm.</p>
<p>It's called the *feeler bet*.</p>
<p>## The Feeler Bet</p>
<p>Trong poker, đôi khi bạn thực hiện một bet nhỏ không chỉ để thắng pot, mà còn để tìm hiểu cách đối phương phản ứng, từ đó update estimate về range của họ.</p>
<p>Liên hệ nó với chuyện dating, giả sử bạn vừa đi first date với một cô gái. Buổi tối khá vui, hai người nói chuyện được vài tiếng, nhưng bạn vẫn không thực sự biết cô ấy có muốn gặp lại mình hay không.</p>
<p>Bạn có thể ngồi phân tích hàng trăm signals.</p>
<p>Cô ấy có cười nhiều không? Có hỏi về công việc của bạn không? Lúc về có nhắn tin trước không? Có sử dụng emoji trong tin nhắn không?</p>
<p>Hoặc bạn có thể thực hiện một cái probe rất đơn giản.</p>
<p>"Hey, I had fun tonight. Wanna grab coffee this weekend?"</p>
<p>Small investment. New information.</p>
<p>Nếu cô ấy đồng ý và chủ động chọn thời gian, đó là một positive signal.</p>
<p>Nếu cô ấy bận nhưng đề xuất một ngày khác, cũng là một signal đáng chú ý.</p>
<p>Còn nếu cô ấy liên tục từ chối và không hề muốn tìm một alternative, thì có lẽ bạn đã có thêm lý do để update prior của mình.</p>
<p>Tất nhiên một observation không phải proof. Có những người không giỏi nhắn tin, có người thực sự bận, và cũng có người cần thêm thời gian để hiểu người khác.</p>
<p>Nhưng thay vì ngồi guessing mãi, một lời mời rõ ràng đôi khi đem lại nhiều information hơn cả trăm cái emoji.</p>
<p>Lit Nomad còn đề xuất quan sát những metrics như text length ratio, response time, tỷ lệ tin nhắn được gửi và nhận, hay mức độ chủ động của mỗi người.</p>
<p>Và t phải công nhận, với tư cách một data scientist, t thấy cái idea ấy khá hấp dẫn.</p>
<p>Imagine building an attraction classifier from text messages. Một cái app tên là Are They Into You?</p>
<p>Input: text messages.</p>
<p>Output: attraction probability.</p>
<p>Model confidence: questionable.</p>
<p>Features có thể bao gồm số lần hai người chủ động bắt đầu conversation, số câu hỏi được đặt ra, mức độ reciprocation hay tần suất chủ động đề xuất gặp nhau.</p>
<p>Nhưng reply time bằng nhau không có nghĩa attraction bằng nhau. Một người có thể trả lời rất nhanh vì đang rảnh, hoặc rất chậm vì công việc bận rộn.</p>
<p>Và một cái model đọc tin nhắn cũng không thể tự hiểu toàn bộ relationship context, chưa kể những vấn đề về privacy nếu đem private conversations đi phân tích mà chưa có sự đồng ý.</p>
<p>Still, the concept is interesting.</p>
<p>Instead of assuming you know someone's preferences, make an observation and update your prediction.</p>
<p>That's literally what Bayesian thinking is about.</p>
<p>## Continuation Bet</p>
<p>There ss another concept in pokers i think it's very related to dating, Continuation bet.</p>
<p>Trong poker, sau khi là người raise ở vòng trước, bạn có thể tiếp tục bet ở vòng tiếp theo trong những tình huống phù hợp, kể cả khi bài của mình chưa thực sự mạnh.</p>
<p>Điều thú vị là đôi khi người ta ngại bet không phải vì nó có negative expected value, mà vì họ sợ bị call hoặc raise khi đang bluff.</p>
<p>Basically, their ego gets in the way.</p>
<p>Trong dating cũng vậy.</p>
<p>Rất nhiều người không dám chủ động rủ người mình thích đi chơi vì sợ bị từ chối.</p>
<p>Họ sợ mất mặt, sợ người khác biết mình bị reject, hay đơn giản là không muốn nhận một cái outcome bằng 0.</p>
<p>Nhưng nếu không bao giờ hỏi thì probability of getting a date thông qua lời mời ấy cũng bằng 0.</p>
<p>You miss every shot you don't take.</p>
<p>T nghĩ có một sự khác biệt lớn giữa việc sợ thua và việc chơi để thắng.</p>
<p>Nếu t thực sự thích một cô gái, và cost của việc hỏi cô ấy có muốn đi cà phê không tương đối nhỏ, tại sao t lại không thử?</p>
<p>Worst case, she says no.</p>
<p>Of course, there's an emotional cost. Rejection chẳng bao giờ hoàn toàn miễn phí.</p>
<p>Nhưng nếu chỉ vì sợ một lần bị từ chối mà không bao giờ thực hiện action nào, bạn có thể đang minimize losses bằng cách eliminate luôn cả potential returns.</p>
<p>Và đấy là lúc t thấy cái poker analogy này còn liên quan tới chính mình.</p>
<p>T luôn thích control exposure. Tính risk budget, estimate downside, chuẩn bị exit strategy trước khi bước vào một chuyện gì đó.</p>
<p>Nhưng đôi khi, chính việc quá tập trung vào protecting downside khiến t quên mất rằng muốn thắng thì trước hết phải chấp nhận một xác suất thua nào đó.</p>
<p>Không phải cứ all-in là thông minh.</p>
<p>Nhưng fold every hand cũng chẳng phải một winning strategy.</p>
<p>## Don't Play Your Cards. Play the Player.</p>
<p>Có một câu nói rất nổi tiếng trong poker.</p>
<p>Don't play your cards. Play the player.</p>
<p>Trong dating, cái cards của bạn có thể là appearance, intelligence, money, status và những thứ mà t đã cố quantify bằng SMV ở đầu chương.</p>
<p>Nhưng sở hữu một bộ features đủ đẹp không đảm bảo rằng cô gái kia sẽ thích bạn.</p>
<p>Bởi vì còn một variable khác.</p>
<p>Her preferences.</p>
<p>Một cô gái có thể thích những người cực kỳ ambitious, còn một người khác chỉ muốn một partner có nhiều thời gian dành cho gia đình.</p>
<p>Có người thích fine dining. Có người lại thích cùng nhau khám phá một quán cà phê nhỏ hay đi dạo quanh thành phố.</p>
<p>Vậy nên một strategy thành công với người này chưa chắc có tác dụng với người khác.</p>
<p>T nghĩ đây mới là điều đáng học từ poker: thay vì chỉ cố improve hand strength của mình, hãy tìm hiểu người mà mình đang thực sự tương tác.</p>
<p>Từng có lúc t tưởng một người yêu mình thật thì sẽ chẳng bao giờ muốn mình thay đổi. Còn ai góp ý về lối sống, lịch trình hay thói quen của t đều đang cố kéo Jason vào một cái khuôn có sẵn. Nghĩ cũng buồn cười: t muốn được nhìn thấy như một individual, nhưng lại đưa tất cả những người khác vào đúng một mô hình chọn lọc bạn tình. A really elegant contradiction, built by yours truly.</p>
<p>Nhưng t không nghĩ điều đó có nghĩa là phải giả vờ trở thành đúng kiểu người cô ấy muốn.</p>
<p>Trong poker, bạn có thể bluff.</p>
<p>Dating thì phức tạp hơn, vì một cái bluff thành công ở first date có thể trở thành một lời nói dối mà bạn phải duy trì trong cả relationship.</p>
<p>Giả vờ giàu hơn, thông minh hơn hay sống một cuộc đời thú vị hơn mình thực sự có thể giúp bạn tạo first impression tốt hơn trong một vài phút.</p>
<p>Nhưng sau đó thì sao?</p>
<p>Bạn sẽ phải maintain cả cái character ấy.</p>
<p>Sounds exhausting.</p>
<p>Và có lẽ đó là một khoản investment còn đắt hơn bất cứ bữa tối nào.</p>
<p>## The First Date Algorithm</p>
<p>Okay, enough theory.</p>
<p>Let's get practical.</p>
<p>Giả sử sau tất cả những theory vừa rồi, bạn tìm được một cô gái mà mình thực sự muốn đi chơi cùng.</p>
<p>Từng có một thời gian t nghĩ cách optimize ngân sách của một buổi hẹn cũng rất đơn giản.</p>
<p>Look at the girl, estimate her attractiveness, then decide how much you're willing to spend.</p>
<p>Một triệu, ba triệu hay mười triệu.</p>
<p>T còn từng nghĩ nhan sắc càng cao thì mình càng dễ cảm thấy một bữa tối đắt tiền là worth it.</p>
<p>Nghe khá giống investment analysis nhỉ.</p>
<p>Có điều sau cái sigmoid model vừa rồi, rõ ràng việc maximize spending không hẳn là optimal strategy.</p>
<p>Bởi vì bản thân việc được ngồi ăn tối với ai đó chưa chắc phụ thuộc vào số tiền bạn bỏ ra.</p>
<p>Và đôi khi, bạn còn chẳng cần nghĩ nhiều đến thế.</p>
<p>T nhớ từng có một cuộc nói chuyện khá buồn cười với một thằng bạn.</p>
<p>Nó hỏi t có chắc mình muốn rủ một cô gái đi chơi không.</p>
<p>"Are you sure?"</p>
<p>"Absolutely."</p>
<p>"Sao mày nghĩ cô ấy sẽ đồng ý?"</p>
<p>"Why not?"</p>
<p>"Không, tao đang hỏi tại sao cô ấy muốn đi chơi với mày?"</p>
<p>"Yeah. Why not? That's my answer."</p>
<p>Nó nhìn t như thể vừa nghe một cái regression model không có dependent variable.</p>
<p>T bắt đầu giải thích.</p>
<p>Cô ấy được đi ăn một bữa tối mà không phải trả tiền. Có một người ngồi nghe cô ấy yapping cả buổi. Và quan trọng nhất, cô ấy được hang out với một người như t.</p>
<p>I'm funny, you know.</p>
<p>Nó hỏi tiếp:</p>
<p>"À, còn được đi với một thằng đẹp trai nữa nhỉ?"</p>
<p>"Exactly! You got it now."</p>
<p>T nói với vẻ mặt như vừa đặt dấu chấm cuối cùng cho một mathematical proof.</p>
<p>Nhưng sau đó t nhận ra hai đứa đang giải hai bài toán khác nhau.</p>
<p>Nó hỏi why would she say yes?</p>
<p>T lại hỏi why would she say no?</p>
<p>Nó muốn tìm evidence rằng cô ấy có demand đối với t.</p>
<p>Còn t đang tìm cách remove friction khỏi một cái conversion funnel.</p>
<p>Nếu cô ấy ngại mất tiền, dinner is on me.</p>
<p>Nếu địa điểm quá xa, t chọn một nơi khác.</p>
<p>Nếu sợ buổi tối awkward, t có thể chủ động trò chuyện.</p>
<p>Nếu cô ấy muốn ăn gì đó, t có thể tìm một chỗ phù hợp.</p>
<p>T đang optimize những điều kiện khiến lời mời trở nên dễ chấp nhận hơn.</p>
<p>Nhưng thằng bạn t hỏi một câu mà toàn bộ optimization ấy chưa thực sự trả lời.</p>
<p>Does she actually want to spend time with you?</p>
<p>Và đúng là có những thứ không thể giải quyết chỉ bằng cách remove blockers.</p>
<p>Một người có thể hoàn toàn rảnh, không phải trả tiền, địa điểm lại ngay gần nhà, nhưng vẫn chẳng muốn đi ăn tối với bạn.</p>
<p>Not because your offer is bad.</p>
<p>Maybe there's simply no attraction.</p>
<p>Đấy chính là sự khác biệt giữa demand validation và conversion optimization.</p>
<p>Và nếu có một điều t rút ra từ việc nghĩ quá nhiều về dating, thì đó là mình nên giải đúng bài toán trước khi optimize nó.</p>
<p>Dù vậy, t vẫn thích nghĩ về dating như một data pipeline.</p>
<p>Job 01 là first date.</p>
<p>Input gồm hai người chưa hiểu nhau đủ, một bữa tối và rất nhiều uncertainty.</p>
<p>Output không phải việc bạn đã thuyết phục được cô ấy đồng ý đi chơi.</p>
<p>Output tốt nhất là cả hai có một buổi tối vui vẻ và đều muốn gặp lại.</p>
<p>Job 01 successful?</p>
<p>Trigger Job 02.</p>
<p>Có thể là cà phê, một bộ phim, đi dạo, hoặc một activity nào đó mà cả hai đều thích.</p>
<p>Job 02 successful?</p>
<p>Trigger Job 03.</p>
<p>Cứ thế.</p>
<p>Don't overengineer your wedding before finishing the first dinner.</p>
<p>Và nếu một người không muốn tiếp tục, đó không phải transient error để bạn retry thêm mười lần.</p>
<p>Pipeline ends.</p>
<p>T thích approach này vì thay vì cố predict toàn bộ future từ vài bức ảnh trên Tinder, t có thể update model bằng observations sau mỗi interaction.</p>
<p>Trên profile, cô ấy có thể nói mình thích những người thông minh, hài hước, thành công và có chiều sâu.</p>
<p>Nhưng lúc hai người gặp nhau, đôi khi chemistry chẳng tuân theo bất kỳ feature importance nào mà chúng ta đã estimate.</p>
<p>Eastwick và Finkel từng có nghiên cứu speed-dating cho thấy những preferences mà người tham gia tuyên bố trước đó không dự đoán tốt điều gì khiến họ thực sự muốn một người sau khi gặp mặt.</p>
<p>Càng thú vị hơn khi t nghĩ chính mình cũng có thể rơi vào cái bias ấy.</p>
<p>T có thể ngồi một buổi để rank appearance, intelligence, money, status, rồi tự tin nói rằng mình biết chính xác mẫu người mình thích.</p>
<p>Nhưng sau đó lại gặp một cô gái mà mọi thứ trên giấy chẳng có gì quá đặc biệt, và chẳng hiểu sao vẫn muốn nói chuyện với cô ấy tới tận lúc quán đóng cửa.</p>
<p>Vậy nên có lẽ cái original SMV function của t cũng cần thêm vài features.</p>
<p>Hoặc t đã assign sai weights ngay từ đầu.</p>
<p>## The Objective Function</p>
<p>Sau cả đống evolutionary biology, game theory, Tinder analytics, logistic regression và asset pricing, cuối cùng t vẫn phải quay về một câu hỏi khá đơn giản.</p>
<p>What am I actually optimizing for?</p>
<p>Nếu mục tiêu chỉ là getting matches, t có thể optimize profile pictures.</p>
<p>Nếu muốn nhiều first dates, t có thể improve messaging strategy và reduce friction.</p>
<p>Nếu muốn một cô gái chủ động chase mình, t có thể thử tạo uncertainty hoặc artificial scarcity.</p>
<p>Nhưng nếu t thực sự muốn một relationship thì sao?</p>
<p>T nghĩ cái objective function lúc ấy phải khác.</p>
<p>Appearance tất nhiên vẫn quan trọng. T cũng chẳng giả vờ nói rằng mình không quan tâm tới ngoại hình.</p>
<p>Đương nhiên vẫn phải xinh chứ, lol.</p>
<p>Nhưng nếu phải assign weights, t nghĩ intelligence và intellectual compatibility mới là hai features mà t coi trọng hơn.</p>
<p>Liệu cô ấy có thể ngồi với t cả buổi để nói về philosophy, science, history, economics, conspiracy theories hay những thứ random mà hai đứa vừa đọc được trên internet hay không?</p>
<p>Liệu cô ấy có thể challenge một cái theory của t, chỉ ra tại sao cái logic nghe rất hợp lý ấy thực ra lại sai?</p>
<p>Liệu t có thể kể một câu chuyện rất dài, rất nerdy, mà cô ấy vẫn thực sự muốn nghe, không phải vì lịch sự, cũng chẳng phải vì cô ấy đang cố impress t?</p>
<p>Và ngược lại, liệu t có đủ tò mò để hiểu thế giới của cô ấy, thay vì lúc nào cũng cố explain nó bằng models của mình?</p>
<p>T nghĩ những thứ ấy quan trọng hơn nhiều so với việc cô ấy được bao nhiêu điểm trên một cái SMV scale mà chính t tạo ra.</p>
<p>Có lẽ sau tất cả, thứ t muốn không phải một người có perceived market value cao nhất.</p>
<p>Mà là một người khiến t cảm thấy việc dành thời gian cho cô ấy chưa bao giờ giống một khoản investment phải tính toán.</p>
<p>Một buổi tối ăn pizza trên sofa, nói đủ thứ chuyện trên đời.</p>
<p>No fancy restaurant. No artificial scarcity. No need to play hard to get.</p>
<p>Just two people who genuinely want to be there.</p>
<p>Tất nhiên, t vẫn sẽ tiếp tục build models. It's literally what I do.</p>
<p>Nhưng có một điều mà t nghĩ mình bắt đầu hiểu.</p>
<p>A model can optimize a metric perfectly and still miss the entire point.</p>
<p>Anyway.</p>
<p>Thank you for coming to my TED Talk.</p></td></tr></tbody></table>
