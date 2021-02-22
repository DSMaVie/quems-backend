# Database
This folder contains database files for the application.

## Tables
For the event manager we need three tables:
* EventTable
* DataTable
* PlacesTable
* RegularitiesTable

Th event Table should contain data that every single event has like a start time.
the data table hold information that can also be templated if an event is recurring often.
The places table contains names of places and an id to save space.
The regularities table contains the information about how an recurring event is recurring.
Either by referencing another event or by having it occur in a certain interval during a base (month or week)

## schema

The schemata below are subject to change. To see the current definitions in code look into `database.EventDatabase.__init__`.

### event table

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| id | int | primary key | the global id, by which events can be identified |
| start | int | | unix time of starting time |
| end | int | nullable | unix time of starting time |
| data_id | int | foreign key (data.id) | data ID, key of data table, where rest of data can be found |
| created | int | | time of creation |
| last_edited | int | nullable | time last edited, nullable if same as created |


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

We can deduce 3 modes.
* Reg : The event is happening with some reoccurence on its own (first and second case above)
* Ref : The case 3 above regularity inherited bc event is happening after/before another.
* None: Case 4

Mode 1 and 2 get two colums each which should be constrained to exclude each other.
So far the following schema exists:

| Attribute | Type | additional Info | Description |
| --------- | ---- | -------------- | ----------- |
| id | int | primary key | unique identifier for entry |
| outdated | boolean | | flag that indicates weather the entry is old (1) or for an actual event happening regularily right now (0) |
|ref_event|Integer|foreign key(data.id) | other template the event is happening after/before|
|ref_offset|Integer| | how many days/weeks is the event happening after the ref_event (-1 -> last weekday of month, 0 -> every week, 1 -> every first wekkday of month, etc...)|
|reg_weekday|Integer|| which weekday, between 0 and 6 |
