CREATE TABLE imports (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      path TEXT,
                      starttime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                      endtime TIMESTAMP,
                      count INTEGER,
                      size INTEGER);
CREATE TABLE paths (import_id INTEGER, path TEXT, type TEXT, mtime TIMESTAMP, size INTEGER);
CREATE index idx1 ON paths(path);
CREATE index idx2 ON paths(type);
CREATE index idx3 ON imports(path);
