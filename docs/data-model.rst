.. _data-model-chapter:

==========
Data Model
==========

Matchpoint stores each whole namespace as a Mongo document with several
nested document types. Square brackets denote a list. Properties which
are not nested objects have been omitted.


    Namespace
     └[Interest]

    Interest
     ├─InterestVersion (current)
     └[InterestVersion]

    InterestVersion
     └[Match]
     
    Match
