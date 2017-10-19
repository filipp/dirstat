### Introduction

`dirstat` is a fairly crude, but surprisingly useful tool to generate different statistics about directory structures.


### Usage

Let's say you have a network share mounted at /Volumes/SHARE. Let's import it into dirstat:

    $ dirstat.py import /Volumes/SHARE


After the tool is finished, we can use the sqlite3 command line to get some insight into the tree, without disturbing the
file system itself. Here are just a few examples:

#### Top 10 file types by count

    sqlite> select type, count(*) as c from paths where import_id = 1 group by type order by c desc limit 10;
    JPG|172592                   
    PDF|124481                   
    PNG|74889                    
    DWG|51314                    
    GSM|40811
    MXS|14726
    DOC|6479
    PSD|5640
    MXI|4745
    PLT|4684

#### Space usage in gigabytes by year (of modification date):

    sqlite> select strftime('%Y', mtime) as y, sum(size)/1024/1024/1024 as s from paths group by y order by s desc;
    2017|1300
    2016|1256
    2014|994
    2015|974
    2013|584
    2012|260

#### File types and their counts in a given subdirectory:

    sqlite> select type, count(*) from paths where path like '%/PROJECTS/ACTIVE/%' group by type;
    3DM|3
    3DMBAK|3
    AI|1
    BMP|1
    DIR|51
    DOC|65
    DOCX|7
    DOTX|1
    DWF|1
    DWG|8


### System Requirements

- Python 3 (tested with 3.6.3)


### License

    Copyright © 2017 Filipp Lepalaan <filipp@mac.com>
    This work is free. You can redistribute it and/or modify it under the
    terms of the Do What The Fuck You Want To Public License, Version 2,
    as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.
