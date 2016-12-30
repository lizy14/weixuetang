class Work:
    def __init__(self, user, id, course_id,
        title, start_time, end_time,
        completion,
        detail=None, attachment="",
        graded=False, grading="", grading_comment="", grading_author=""):

        self.id = id
        self.course_id = course_id
        self.title = title.strip()
        self.start_time = start_time
        self.end_time = end_time
        self.completion = completion  # 0 for 尚未提交, 1 for 已经提交, 2 for 已经批改
        self.user = user
        self.detail = detail
        self.attachment = attachment
        self.grading = grading
        self.graded = completion > 1
        self.graded_by = grading_author
        self.grading_comment = grading_comment
        self.submitted = completion > 0


    @property
    async def dict(self):
        d = self.__dict__.copy()
        d["detail"] = await self.detail
        del d['user']
        return d
