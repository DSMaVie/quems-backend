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

## Schema

The schemata below are subject to change.

### EventTable

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| ID | int | primary key | the global id, by which events can be identified |
| time | int | | unix time of starting time |
| recurrent | bool | | flag if recurrent event (1) or not (0) |
| dID | int | | data ID, key of RecurringEventTable or singularTable, where rest of data can be found |

### RecurringEventTable

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| ID | int | primary key | unique identifier for entry |
| place | str |  | place where event is held, could be ref to some placeTable later as a lot of doubling|
| reg | str |strong format constrains needed| regularity descriptor (see below table) |
| outdated | bool || flag if data is outdated info (1) or not(0) |
| name_de | str || name of event in german |
| name_en | str || name of event in english |
| end | int | can be NaN | unix time when the event ends |
| desc_de | str || Description in german |
| desc_en | str || Description in english |
| assignees | str | format check in frontend | who is responsible, could be ref to people table later  |
| nl | bool || newsletter flag |
| insta | bool || insta flag |
| fb_event | bool || flag for fb_event |
| twitter | bool || twitter flag |
| discord | bool || discord flag |

#### regularity descriptor

Recurring Events usually follow specific patterns. A few examples:

* every wednesday (Queercafe)
* every first tuesday per month (Plenum)
* every sunday before a plenum (board meeting)
* no regularity but still occurring often (Polyabend)

### SingularEventTable

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| ID | int | primary key | unique identifier for entry |
| name_de | str || name of event in german |
| name_en | str || name of event in english |
| end | int | can be NaN | unix time when the event ends |
| desc_de | str || Description in german |
| desc_en | str || Description in english |
| assignees | str | format check in frontend | who is responsible |
| nl | bool || newsletter flag |
| insta | bool || insta flag |
| fb_event | bool || flag for fb_event |
| twitter | bool || twitter flag |
| discord | bool || discord flag |
