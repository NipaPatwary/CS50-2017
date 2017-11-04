# Specification

mashup.db

Per readme.txt, US.txt is quite like a CSV file except that its fields are delimited with \t (a tab character) instead of a comma. Conveniently, SQLite allows you to import CSV files and, as it turns out, TSV (tab-separated values) files as well. But you first need a table into which to import such a file.

Using phpLiteAdmin or sqlite3, create a table in mashup.db called places that has these twelve fields, in this order:

country_code

postal_code

place_name

admin_name1

admin_code1

admin_name2

admin_code2

admin_name3

admin_code3

latitude

longitude

accuracy

See readme.txt (or US.txt itself) for clues as to appropriate types for these fields. Don’t include an id field (else you can’t do what we’re about to do!).

Rather than INSERT the rows from US.txt into your newly created table, let’s now import them in bulk as follows:

$ sqlite3 mashup.db
.separator "\t"
.import US.txt places
If you see any errors, odds are your schema for places isn’t quite right, in which case you’ll want to ALTER (or DROP and re-CREATE) it accordingly. To confirm that an import’s successful, execute

wc -l US.txt
to count how many rows are in US.txt. (That command-line argument is a hyphen followed by a lowercase L.) Then execute a query like

SELECT COUNT(*) FROM places;
in sqlite3 or phpLiteAdmin. The counts should match!

application.py

articles
Complete the implementation of /articles in such a way that it outputs a JSON array of objects, each of which represents an article for  geo, whereby geo is passed into /articles as a GET parameter, as in the staff solution, below.

http://mashup.cs50.net/articles?geo=02138

http://mashup.cs50.net/articles?geo=06511

http://mashup.cs50.net/articles?geo=90210

Odds are you’ll want to call lookup! To test /articles, even before your text box is operational, simply visit URLs like

https://ide50-username.cs50.io/articles?geo=02138

https://ide50-username.cs50.io/articles?geo=06511

https://ide50-username.cs50.io/articles?geo=90210

and other such variants, where username is your own username, to see if you get back the JSON you expect.

search

Complete the implementation of /search in such a way that it outputs a JSON array of objects, each of which represents a row from places that somehow matches the value of q, as in the staff solution below.

http://mashup.cs50.net/search?q=02138

http://mashup.cs50.net/search?q=Cambridge

http://mashup.cs50.net/search?q=06511

http://mashup.cs50.net/search?q=New+Haven

The value of q, passed into /search as a GET parameter, might be a city, state, and/or postal code. We leave it to you to decide what constitutes a match and, therefore, which rows to SELECT. It suffices to support searching by postal codes only, but try to support searching by city and/or state as well. Odds are you’ll find SQL’s LIKE keyword helpful. If feeling adventurous, you might like (but are not required) to experiment with SQLite’s support for full-text searches.

For instance, consider the query below.

db.execute("SELECT * FROM places WHERE postal_code = :q", q=request.args.get("q"))
Unfortunately, that query requires that a user’s input be exactly equal to a postal code (per the =), which isn’t all that compelling for autocomplete. How about this one instead? (Recall that + is Python’s concatenation operator.)

q = request.args.get("q") + "%"
db.execute("SELECT * FROM places WHERE postal_code LIKE :q", q=q)
Notice how this example appends % to the user’s input, which happens to be SQL’s "wildcard" character that means "match any number of characters." The effect is that this query will return rows whose postal codes match whatever the user typed followed by any number of other characters. In other words, any of 0, 02, 021, 0213, and 02138 might return rows, as might any of 0, 06, 065, 0651, and 06511.

If you’d like to support searching by more than just postal codes, keep in mind that SQL supports OR and AND!

To test /search, even before your text box is operational, simply visit URLs like

https://ide50-username.cs50.io/search?q=02138

https://ide50-username.cs50.io/search?q=Cambridge+MA

https://ide50-username.cs50.io/search?q=Cambridge,+MA

https://ide50-username.cs50.io/search?q=Cambridge,+Massachusetts

https://ide50-username.cs50.io/search?q=Cambridge,+Massachusetts,+US

or

https://ide50-username.cs50.io/search?q=06511

https://ide50-username.cs50.io/search?q=New+Haven+CT

https://ide50-username.cs50.io/search?q=New+Haven,+CT

https://ide50-username.cs50.io/search?q=New+Haven,+Connecticut

https://ide50-username.cs50.io/search?q=New+Haven,+Connecticut,+US

and other such variants, where username is your own username, to see if you get back the JSON you expect. Again, though, we leave it to you to decide just how supportive /search will be of such variants. The more flexible, though, the better! Try to implement features that you yourself would expect as a user!

Feel free to tinker with the staff’s solution at http://mashup.cs50.net/, inspecting its HTTP requests via Chrome’s Network tab as needed, if unsure how your own code should work!

scripts.js

First, toward the top of scripts.js, you’ll see an anonymous function, inside of which is a definition of options, an object, one of whose keys is center, the value of which is an object with two keys of its own, lat, and lng. Per the comment alongside that object, your mashup’s map is currently centered on Stanford, California. (D’oh.) Change the coordinates of your map’s center to Cambridge (42.3770, -71.1256) or New Haven (41.3184, -72.9318) or anywhere else! (Though be sure to choose coordinates in the US if you downloaded US.txt!) Once you save your changes and reload your map, you should find yourself there! Zoom out as needed to confirm visually.

As before, feel free to tinker with the staff’s solution at http://mashup.cs50.net/, inspecting its HTTP requests via Chrome’s Network tab as needed, if unsure how your own code should work!

configure

Now that /search and your text box are (hopefully!) working, modify the value of suggestion in configure, the function in scripts.js, so that it displays matches (i.e., place_name, admin_name1, and/or other fields) instead of TODO. Recall that a value like

<div>{{place_name}}, {{admin_name1}}, {{postal_code}}</div>
might do the trick.

addMarker

Implement addMarker in scripts.js in such a way that it adds a marker for place on the map, where place is a JavaScript object that represents a row from places. See https://developers.google.com/maps/documentation/javascript/markers for tips. Note that the latest (experimental) version of Google’s API allows markers to have labels.

When a marker is clicked, it should trigger the mashup’s info window to open, anchored at that same marker, the contents of which should be an unordered list of links to article for that article’s location (unless /articles outputs an empty array)!

Not to worry if some of your markers (or labels) overlap others, assuming such is the result of imperfections in Google’s API or US.txt and not your own code!

If you’d like to customize your markers' icon, see https://developers.google.com/maps/documentation/javascript/markers#simple_icons. For the URLs of icons built-into Google Maps, see http://www.lass.it/Web/viewer.aspx?id=4. For third-party icons, see https://mapicons.mapsmarker.com/.

removeMarkers

Implement removeMarkers in such a way that it removes all markers from the map (and deletes them). Odds are you’ll need addMarker to modify that global variable called markers in order for removeMarkers to work its own magic!