CREATE TABLE courses (
    id integer primary key autoincrement,
    name text
);

CREATE TABLE students (
    id integer primary key autoincrement,
    alias text,
    name text
);

CREATE TABLE student_course_relations (
    id integer primary key autoincrement,
    student integer,
    course integer,
    FOREIGN KEY(student) REFERENCES students(id),
    FOREIGN KEY(course) REFERENCES courses(id)
);

CREATE TABLE mark_categories (
    id integer primary key autoincrement,
    name text,
    weight integer,
    course integer,
    FOREIGN KEY(course) REFERENCES courses(id)
);
CREATE TABLE mark_category_subs (
    id integer primary key autoincrement,
    category integer,
    parent integer,
    FOREIGN KEY(category) REFERENCES mark_categories(id)
    FOREIGN KEY(parent) REFERENCES mark_categories(id)
);

CREATE TABLE markitems (
    id integer primary key autoincrement,
    name text,
    outa integer,
    weight integer,
    category integer,
    FOREIGN KEY(category) REFERENCES mark_categories(id)
);

CREATE TABLE marks (
    id integer primary key autoincrement,
    name text,
    score integer,
    markitem integer,
    student integer,
    FOREIGN KEY(markitem) REFERENCES markitems(id),
    FOREIGN KEY(student) REFERENCES students(id)
);
