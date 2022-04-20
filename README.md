### Heroku Link
[Link Here](http://honeywheat.herokuapp.com/)

### Description
Our app lets you take a survey about your genre preferences of video games and then gives you recommendations of games you might be interested in.

### Linting
Majority of these errors were caused by styling choices (ways we enumerated our dictionaries) or by the amount of arguments/parameters we passed in certain locations. Lastly there were errors regarding functions used to add/commit to our DB not being recognized by pylint.

    W0107 - Our teardown for our tests needed the pass statement so we ignored this warning.
    R0914 - Warned for having too many local vars, but was needed in this case.
    C0206 - Suggested using .items() to iterate dict, not what we needed.
    C0200 - Suggested using enumerate, not what we needed.
    E1101 - Pylint not recognizing add/commit methods for our db instance
    R0902 - Warned for having too many instance vars, but was needed in this case.
    R0913 - Warned for having too many arguments, but was needed in this case.
    R0903 - Warned for having too few public methods, but was not needed.

