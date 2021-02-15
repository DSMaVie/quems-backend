# Database
This folder contains database files for the application.

## Tables
For the event manager we need three tables:
* EventTable
* RecurringEventTable
* SingularEventTable

The singular and recurring event tables contain the actual event data while
the main event table contains the time data when which event takes place.
The EventTable should be backed up and emptied every year or so, to prevent long reads.

## schema

The schemata below are subject to change. To see the current definitions in code look into `database.EventDatabase.__init__`.

### event table

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| id | int | primary key | the global id, by which events can be identified |
| start | int | | unix time of starting time |
| end | int | nullable | unix time of starting time |
| data_id | int | foreign key (data.id) | data ID, key of data table, where rest of data can be found |
| last_edited | int | | time last edited |


### data table

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| id | int | primary key | unique identifier for entry |
| place_id | int | foreign key (place.id), nullable | place where event is held|
| reg_id | int | foreign key (place.id), nullable | link to table where regularity params are stored, can be nulled if event does not repeat |
| name_de | str | | name of event in german |
| name_en | str | | name of event in english |
| desc_de | str | nullable| Description in german |
| desc_en | str | nullable | Description in english |
| assignees | str | no constrains yet | who is responsible, could be ref to people table later  |
| nl | bool || newsletter flag |
| insta | bool || insta flag |
| fb_event | bool || flag for fb_event |
| twitter | bool || twitter flag |
| discord | bool || discord flag |
| calendar | bool || calendar flag |

### regularity table

Recurring Events usually follow specific patterns. A few examples:

* every wednesday (Queercafe)
* every first tuesday per month (Plenum)
* every sunday before a plenum (board meeting)
* no regularity but still occurring often (Polyabend)

The table itself is not yet fleshed out. We need to think about a schema that implements the above mentioned patterns and (ideally) is extensible if needed. So far the following schema exists:

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| id | int | primary key | unique identifier for entry |
| outdated | boolean | | flag that indicates wheather the entry is old (1) or for an actual event happening regularily right now (0) |
