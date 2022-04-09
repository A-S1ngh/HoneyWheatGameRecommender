### Heroku Link
[Link Here](https://still-badlands-81214.herokuapp.com)

### Description
Our app lets you take a survey about your genre preferences of video games and then gives you recommendations of games you might be interested in.

### Linting
Majority of these errors were caused by styling choices (ways we enumerated our dictionaries) or by the amount of arguments/parameters we passed in certain locations. The import errors were disabled because they were on my local machine but weren't actual errors. All imported libraries were working but I still had import errors. Some docstring errors were also ignored. Lastly there were errors regarding functions used to add/commit to our DB not being recognized by pylint.

    C0114, # missing-module-docstring
    C0116, # missing-function-docstring
    E1101,
    C0115,
    R0903,
    R0902, # too many instance attributes
    R0913, # too many args
    R0914,
    C0206, #enumeration tips
    C0201,
    C0200
