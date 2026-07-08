from repository import Repository

repository = Repository()

row = {

    "URL":"https://example.com",
    "Title":"Example",

    "Headings":"",
    "Summary":"",

    "Page Title":"",
    "H1":"",
    "Meta Description":"",
    "Canonical URL":"",

    "Depth":0,
    "Status":"Success",

    "Department":"Test",

    "Category":"General",

    "Classification Confidence":0,

    "Emails Found":"",
    "Phones Found":"",
    "Dates Found":"",

    "Opportunity Type":"",
    "Deadline":"",
    "Times Found":"",
    "Amounts Found":"",

    "Priority":0,

    "Change Status":"New",

    "Content Hash":"abc123"

}

repository.insert_page(row)

print("Inserted successfully.")