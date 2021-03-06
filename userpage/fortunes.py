from datetime import date


def get_fortune():
    dt = date(1970, 1, 1)
    return fortunes[(date.today() - dt).days % len(fortunes)]


fortunes = [
    "少壮不努力，老大徒悲伤。——汉乐府古辞《长歌行》",
    "业精于勤，荒于嬉。——韩愈《进学解》",
    "一寸光阴一寸金，寸金难买寸光阴。——《增广贤文》",
    "天行健，君子以自强不息。——《周易·乾·象》",
    "志不强者智不达。——《墨子·修身》",
    "青，取之于蓝而青于蓝；冰，水为之而寒于水。——《荀子·劝学》",
    "志当存高远。——诸葛亮《诫外生书》",
    "丈夫志四海，万里犹比邻。——曹植《赠白马王彪》",
    "有志者事竟成。——《后汉书·耿列传》",
    "会当凌绝顶，一览众山小。——杜甫《望岳》",
    "岁寒，然后知松柏之后凋也。——《论语·子罕》",
    "天将降大任于是人也，必先苦其心志，劳其筋骨，饿其体肤，空乏其身，行拂乱其所为。——《孟子·告子下》",
    "锲而舍之，朽木不折；锲而不舍，金石可镂。——《荀子·劝学》",
    "石可破也，而不可夺坚；丹可磨也，而不可夺赤。——《吕氏春秋·诚廉》",
    "精诚所加，金石为开。——《后汉书·光武十王列传》",
    "忧劳可以兴国，逸豫可以亡身。——《新五代史·伶官传序》",
    "路曼曼其修远兮，吾将上下而求索。——屈原《离骚》",
    "位卑未敢忘忧国，事定犹须待盖棺。——陆游《病起》",
    "尺有所短；寸有所长。物有所不足；智有所不明。——屈原《卜居》",
    "若要功夫深，铁杵磨成针。——曹学《蜀中广记·上川南道彭山县》",
    "绳锯木断，水滴石穿。——罗大经《鹤林玉露》",
    "日日行，不怕千万里；常常做，不怕千万事。——《格言联璧·处事》",
    "天下之事常成于困约，而败于奢靡。——陆游",
    "积土而为山，积水而为海。——《荀子·儒效》",
    "人非圣贤，孰能无过。——《训俗遗规》",
    "坚志而勇为，谓之刚。刚，生人之德也。——《练兵实纪·刚复害》",
    "捐躯赴国难，视死忽如归。——曹植《白马篇》",
    "天下兴亡，匹夫有责。——顾炎武",
    "丈夫不报国，终为贫贱人。——陈恭尹《射虎射石头》",
    "时危见臣节，世乱识忠良。——鲍照《代出自蓟北门行》",
    "苟利国家生死以，岂因祸福避趋之。——林则徐《赴戎登程口占示家人》",
    "真者，精诚之至也，不精不诚，不能动人。——《庄子·渔夫》",
    "勿以恶小而为之，勿以善小而不为。惟贤惟德，能服于人。——刘备",
    "傲不可长，欲不可纵，乐不可极，志不可满。——魏徵",
    "不傲才以骄人，不以宠而作威。——诸葛亮",
    "人生的旅途，前途很远，也很暗。然而不要怕，不怕的人的面前才有路。——鲁迅",
    "人生像攀登一座山，而找寻出路，却是一种学习的过程，我们应当在这过程中，学习稳定、冷静，学习如何从慌乱中找到生机。——席慕蓉",
    "做人也要像蜡烛一样，在有限的一生中有一分热发一分光，给人以光明，给人以温暖。——萧楚女",
    "所谓天才，只不过是把别人喝咖啡的功夫都用在工作上了。——鲁迅",
    "人类的希望像是一颗永恒的星，乌云掩不住它的光芒。特别是在今天，和平不是一个理想，一个梦，它是万人的愿望。——巴金",
    "我们是国家的主人，应该处处为国家着想。——雷锋",
    "我们爱我们的民族，这是我们自信心的源泉。——周恩来",
    "春蚕到死丝方尽，人至期颐亦不休。一息尚存须努力，留作青年好范畴。——吴玉章",
    "学习的敌人是自己的满足，要认真学习一点东西，必须从不自满开始。对自己，“学而不厌”，对人家，“诲人不倦”，我们应取这种态度。——毛泽东",
    "错误和挫折教训了我们，使我们比较地聪明起来了，我们的情就办得好一些。任何政党，任何个人，错误总是难免的，我们要求犯得少一点。犯了错误则要求改正，改正得越迅速，越彻底，越好。——毛泽东",
    "一分钟一秒钟自满，在这一分一秒间就停止了自己吸收的生命和排泄的生命。只有接受批评才能排泄精神的一切渣滓。只有吸收他人的意见。、我才能添加精神上新的滋养品。——徐特立",
    "形成天才的决定因素应该是勤奋。……有几分勤学苦练是成正比例的，——郭沫若",
    "自觉心是进步之母，自贱心是堕落之源，故自觉心不可无，自贱心不可有。——邹韬奋",
    "在劳力上劳心，是一切发明之母。事事在劳力上劳心，变可得事物之真理。——陶行知",
    "入于污泥而不染、不受资产阶级糖衣炮弹的侵蚀，是最难能可贵的革命品质。——周恩来",
    "一知半解的人，多不谦虚；见多识广有本领的人，一定谦虚。——谢觉哉"
]
