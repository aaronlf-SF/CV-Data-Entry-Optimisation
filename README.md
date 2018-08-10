# Caliber Data Entry Optimisation

#### Current version: v2.1.3

This program is designed to increase productivity when filling out skills from a CV onto the Caliber database. By taking the raw text from the CV, this program finds relevant keywords and matches potential skills. To help counteract false positives, contextual sentences in which keyword(s) are contained are provided to the user, as well as the occurrence count of keywords found for each skill.

This is presented in an easy-to-read, coloured format designed to maximise productivity - the order of skills printed to the console is the same as the order on Caliber's interface. A summary section is given at the bottom showing all caught skills with the number of keyword occurrences for each, so before diving into the contextual sentences the user can already has an idea of what skills the candidate has.

Although this script functions as it should, it is still in development and keywords caught will be closely monitored in comparison with the real CV, to see if any extra keywords can be added, false positives deleted, etc.


#### Future implementations:
 - Ability to detect if keywords are found below the words 'References' or 'Reference' and to warn the user of this in red writing (this ensures their last boss's title isn't included accidentally!)
 - Conditional keyword searches - having AND conditions on selected keywords that wil only be registered if another specified keyword is found somewhere else in the document, not necessarily beside it (what the current script can handle)
