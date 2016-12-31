from codex.basetest import *
from .models import *
from .utils import Parser

# import logging
# __logger__ = logging.getLogger(name=__name__)

class LectureTests(APITest):

    def test_list(self):
        resp = self.simulate('get', '/api/lecture/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertGreater(len(resp.json()['data']), 0)

    def test_detail(self):
        id = Lecture.objects.all()[0].id
        resp = self.simulate('get', '/api/lecture/detail/', {
            'lecture_id': id
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertEqual(resp.json()['data']['lecture_id'], id)
        resp = self.simulate('get', '/api/lecture/detail/', {
            'lecture_id': 2333333
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0)

    def test_count(self):
        len1 = len(Notice.objects.filter(course=Lecture.objects.all()[0].origin.course))
        len2 = len(Lecture.objects.all())
        self.assertGreater(len1, len2)


class UtilTests(BaseTest):

    def test_parser(self):
        content = '''
        清华大学《文化素质教育讲座》课程
 （清华大学学生社团协会专场）

演讲题目：两岸历史记忆的失落：“二二八”后七十年
演讲人：台湾报告文学家  蓝博洲
             清华大学人文学院教授  汪晖
             清华大学马克思主义学院副教授  刘震
时    间：2016年11月28日（周一）19:00-21:00
地    点：清华大学三教3300
主    办：清华大学学生学生海峡两岸交流协会
协    办：清华大学国家大学生文化素质教育基地

演讲人介绍：
蓝博洲，台湾苗栗人，著名记者、报导文学家和小说家。曾任杂志编辑采访，报社专栏记者和政经研究员。台湾中央大学新锐文化工作坊主持教授，香港浸会大学国际作家工作坊，东华大学驻校作家，台湾大学东亚文明研究中心计划主持人。1987年初，加入《人间》杂志报导文学队伍，展开迄今仍在进行的台湾民众史调查、研究与写作。是最早揭露与研究台湾白色恐怖时期历史的作家。主要著作包括《幌马车之歌》、《台共党人的悲歌》、《台北恋人》等。曾任中国统一联盟副主席。现任中华两岸和平发展联合会主席。曾于2016年3月受邀前来清华大学举办座谈活动，近年也多次受邀前往北京大学等大陆高校举办讲座。
汪晖，江苏扬州人，中国大陆著名学者。1978年录取为扬州师院中文系77级本科生。1981年本科毕业，1982年考取该校现代文学专业研究生，1985年在南京大学获得硕士学位。1985年考取中国社会科学院研究生院，从师唐弢教授攻读博士学位，于1988年毕业并获得博士学位。随即分配至中国社会科学院文学研究所工作，先后任助理研究员、副研究员、研究员。1991年与友人共同创办《学人》丛刊，1996年至2007年担任《读书》杂志主编，曾先后在哈佛大学、加州大学、北欧亚洲研究所、华盛顿大学、香港中文大学、柏林高等研究所等大学和研究机构担任研究员、访问教授。主要著作有：《反抗绝望：鲁迅及其文学世界》、《无地彷徨：“五四”及其回声》、《死火重温》、《现代中国思想的兴起》等，现任清华大学人文学院教授。
刘震，清华大学马克思主义学院副教授。本科就读于清华大学精密仪器系，硕士、博士就读于清华大学经管学院。兼任世界政治经济学会会员，国际发展经济学学会（IDEAS）会员，世界政治经济学学会（WAPE）理事，台湾“两岸公评网”特约撰稿人等职务。

演讲主题介绍:
本次“海峡论坛”邀请到台湾报告文学作家蓝博洲先生、清华大学人文学院教授汪晖老师和马克思主义学院副教授刘震老师围绕“两岸历史记忆的失落：‘二二八’后七十年”为主题进行演讲。演讲将以生动的人文关怀回溯台湾四五十年代台湾人民反殖民、反压迫的历史事实，批驳当行于台湾教科书中误导性的“台独史观”，增进对民族复兴和祖国统一的信念。
“二二八事件”发生于1947年2月28日，是台湾人民反专制、反独裁、争民主的群众运动。1947年2月27日，国民党警员在台北误伤烟贩，群情激动。1947年2月28日，台北市民罢市、游行请愿，又遭当局的镇压，激起了民众的愤怒，爆发了大规模武装暴动。几天后军队进驻台北，对群众进行大规模镇压，运动最终失败。长于报告文学写作的蓝博洲先生先后在大陆出版《幌马车之歌》和《台共党人的悲歌》折射出近代国人求索理想道路的一段缩影，汪晖教授更为后者作逾二万字序言，形容其为“一部被埋藏在地下的台湾现代史”。

特别提示：（1）请本科同学携带学生IC卡刷卡入场；（2）入场时间为当日18:30；（3）根据《北京市消防条例（2011修订）》相关规定，为确保安全，入场人数控制在170人，额满即止。
        '''
        _, res = Parser.parse('第12周（周一）学生社团暨《文化素质教育讲座》课程预告-【蓝博洲 汪晖 刘震】', content)
        self.assertEqual(res, {
            'time': '2016年11月28日（周一）19:00-21:00',
            'place': '清华大学三教3300',
            'lecturer': '台湾报告文学家  蓝博洲',  # TODO: multi-line lecturer
            'title': '两岸历史记忆的失落：“二二八”后七十年'
        })
