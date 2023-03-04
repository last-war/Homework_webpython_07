from connector import session
from sqlalchemy import select, func, desc, and_
from db_models import Teacher, Student, Subject, Group, Journal


def select_1():
    """
        Найти 5 студентов с наибольшим средним баллом по всем предметам.

    SELECT
    st.full_name,
    ROUND(AVG(j.mark),2) as av_mark
    FROM journal as j
    left join students as st
        on st.id = j.student_id
    GROUP BY j.student_id
    ORDER BY av_mark DESC
    limit 5
    ;
    """
    rez = session.query(Student.full_name, func.round(func.avg(Journal.mark), 2).label('av_mark')) \
        .select_from(Journal).join(Student).group_by(Student.id).order_by(desc('av_mark')).limit(5).all()
    return rez


def select_2(sub_id: int):
    """Найти студента с наивысшим средним баллом по определенному предмету.

        SELECT
            st.full_name,
            sub.sub_name,
            ROUND(AVG(j.mark),2) as av_mark
            FROM journal as j
            left join students as st
                on st.id = j.student_id
            left join subjects as sub
                on sub.id = j.subject_id
            where  j.subject_id = 5
            GROUP BY j.student_id
            ORDER BY av_mark DESC
            limit 5
            ;
    """
    rez = session.query(Student.full_name, Subject.sub_name, func.round(func.avg(Journal.mark), 2).label('av_mark')) \
        .select_from(Journal).join(Student).join(Subject).filter(Subject.id == sub_id) \
        .group_by(Student.id, Subject.sub_name).order_by(desc('av_mark')).limit(1).all()
    return rez


def select_3(sub_id: int):
    """Найти средний балл в группах по определенному предмету.

        SELECT
        st.group_id,
        sub.sub_name,
        ROUND(AVG(j.mark),2) as av_mark
        FROM journal as j
        left join students as st
            on st.id = j.student_id
        left join subjects as sub
            on sub.id = j.subject_id
        where  j.subject_id = 4
        GROUP BY st.group_id
    """
    rez = session.query(Student.group_id, Subject.sub_name, func.round(func.avg(Journal.mark), 2).label('av_mark')) \
        .select_from(Journal).join(Student).join(Subject).filter(Subject.id == sub_id).group_by(Subject.id).all()
    return rez


def select_4():
    """Найти средний балл на потоке (по всей таблице оценок).

        SELECT
    ROUND(AVG(j.mark),2) as av_mark
    FROM journal as j
    """
    rez = session.query(func.round(func.avg(Journal.mark), 2).label('av_mark')).select_from(Journal).all()
    return rez


def select_5(teacher_id: int):
    """Найти какие курсы читает определенный преподаватель.

    SELECT
    sub.sub_name,
    t.full_name
    FROM subjects as sub left join teachers as t
    on sub.teacher_id = t.id
    where  t.id = 2;
    """
    rez = session.query(Subject.sub_name, Teacher.full_name).select_from(Subject).join(Teacher) \
        .filter(Teacher.id == teacher_id).all()
    return rez


def select_6(group_id: int):
    """Найти список студентов в определенной группе.

        SELECT
        st.full_name,
        g.gr_name
        FROM students as st left join study_groups as g
        on g.id = st.group_id
        where  g.id = 2;
    """
    rez = session.query(Student.full_name, Group.gr_name).select_from(Student).join(Group) \
        .filter(Group.id == group_id).all()
    return rez


def select_7(group_id: int, subject_id: int):
    """Найти оценки студентов в отдельной группе по определенному предмету.

        SELECT
        st.full_name,
        j.mark
        FROM journal as j
        left join students as st
            on st.id = j.student_id
        left join subjects as sub
            on sub.id = j.subject_id
        where  st.group_id = 3 AND j.subject_id = 3
        ORDER BY sub.sub_name
    """
    rez = session.query(Student.full_name, Journal.mark).select_from(Journal).join(Student).join(Subject) \
        .filter(and_(Student.group_id == group_id, Journal.subject_id == subject_id)).order_by(Subject.sub_name).all()
    return rez


def select_8(teacher_id: int):
    """Найти средний балл, который ставит определенный преподаватель по своим предметам.

    SELECT
    sub.sub_name,
    ROUND(AVG(j.mark),2) as av_mark
    FROM journal as j
    left join subjects as sub
        on sub.id = j.subject_id
    where j.subject_id IN (SELECT id FROM subjects WHERE teacher_id = 2)
    GROUP BY j.subject_id, sub.sub_name
    ORDER BY sub.sub_name;
    """
    subquery = (select(Subject.id).where(Subject.teacher_id == teacher_id).subquery())
    rez = session.query(Subject.sub_name, func.round(func.avg(Journal.mark), 2).label('av_mark')) \
        .select_from(Journal).join(Subject).filter(Journal.subject_id.in_(subquery)) \
        .group_by(Journal.subject_id, Subject.sub_name).order_by(Subject.sub_name).all()
    return rez


def select_9(student_id: int):
    """Найти список курсов, которые посещает определенный студент.

    SELECT
    st.full_name,
    sub.sub_name
    FROM journal as j
    left join students as st
        on st.id = j.student_id
    left join subjects as sub
        on sub.id = j.subject_id
    where  j.student_id = 30
    GROUP BY st.full_name, sub.sub_name;
    """
    rez = session.query(Student.full_name, Subject.sub_name).select_from(Journal).join(Student).join(Subject) \
        .filter(Journal.student_id == student_id).group_by(Student.full_name, Subject.sub_name).all()
    return rez


def select_10(student_id: int, teacher_id: int):
    """Список курсов, которые определенному студенту читает определенный преподаватель.

    SELECT
    sub.sub_name
    FROM journal as j
    left join subjects as sub
        on sub.id = j.subject_id
    where j.subject_id IN (SELECT id FROM subjects WHERE teacher_id = 2) AND j.student_id = 17
    GROUP BY sub.sub_name;
    """
    subquery = (select(Subject.id).where(Subject.teacher_id == teacher_id).subquery())
    rez = session.query(Subject.sub_name).select_from(Journal).join(Subject) \
        .filter(and_(Journal.subject_id.in_(subquery), Journal.student_id == student_id)) \
        .group_by(Subject.sub_name).all()
    return rez


def select_11(student_id: int, teacher_id: int):
    """

    SELECT
    sub.sub_name,
    ROUND(AVG(j.mark),2) as av_mark
    FROM journal as j
    left join subjects as sub
        on sub.id = j.subject_id
    where j.subject_id IN (SELECT id FROM subjects WHERE teacher_id = 2) AND j.student_id = 17
    GROUP BY sub.sub_name;
    """
    subquery = (select(Subject.id).where(Subject.teacher_id == teacher_id).subquery())
    rez = session.query(Subject.sub_name, func.round(func.avg(Journal.mark), 2).label('av_mark')) \
        .select_from(Journal).join(Subject) \
        .filter(and_(Journal.subject_id.in_(subquery), Journal.student_id == student_id)) \
        .group_by(Subject.sub_name).all()
    return rez


def select_12():
    """

    SELECT
    st.full_name,
    sub.sub_name,
    j.created_at,
    j.mark
    FROM journal as j
    left join students as st
        on st.id = j.student_id
    left join subjects as sub
        on sub.id = j.subject_id
    where j.student_id IN (SELECT id FROM students WHERE group_id = 2)
        AND j.subject_id = 5
        AND j.created_at IN (SELECT MAX(created_at) FROM journal)
    ORDER BY created_at DESC;
    """