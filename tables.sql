CREATE TABLE students (
    id integer primary key autoincrement,
    alias text,
    name text
);

CREATE TABLE markgroups (
    id integer primary key autoincrement,
    name text,
    weight integer
);

CREATE TABLE markitems (
    id integer primary key autoincrement,
    name text,
    outa integer,
    weight integer,
    markgroup integer,
    FOREIGN KEY(markgroup) REFERENCES markgroups(id)
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
