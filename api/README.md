# API

Time to discribe whats in here:

## schema

This File contains a BaseTable from which all other ORM Objects (thos discribed as Tables in the Readme of the db folder) inherit from.
It also contains smaller queries that only regard a single table.

## QueryManager
The query manager File contains a query manager class that is used to facilitate more complex queries across multiple tables. If only querying a single 
table the method for that should be defined as a classmethod in this particular class (or in the BaseTable, if generalizable to all tables).

## helpers
A file for helper functions

## API
contains basic api calls.
