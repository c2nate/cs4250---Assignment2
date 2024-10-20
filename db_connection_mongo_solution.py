#-------------------------------------------------------------------------
# AUTHOR: nathaniel dale
# FILENAME: title of the source file
# SPECIFICATION: database connection program to host the functions for index_mongo.py (allows for creation, updates, and deletion of docs)
# FOR: CS 4250- Assignment #2
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient('localhost', 27017)
    db = client['cs4250_db']
    col = db['documents']
    return col


def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    terms = docText.lower().split()

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    # --> add your Python code here
    term_count = {}
    for term in terms:
        if term in term_count:
            term_count[term]+=1
        else:
            term_count[term]=1

    #Producing a final document as a dictionary including all the required fields
    # --> add your Python code here
    document = {
        "_id": docId,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": [{"term": term, "count": term_count[term], "num_char": len(term)} for term in term_count]
    }

    # Insert the document
    # --> add your Python code here
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Create a dictionary (document) with the updated values
    terms = docText.lower().split()
    term_count = {term: terms.count(term) for term in set(terms)}
    
    # Producing the updated document as a dictionary
    document = {
        "_id": docId,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": [{"term": term, "count": term_count[term], "num_char": len(term)} for term in term_count]
    }
    
    # Use replace_one to update the document with the same ID
    col.replace_one({"_id": docId}, document)


def getIndex(col):
    documents = col.find()
    inverted_index = {}

    # Build the inverted index
    for doc in documents:
        for term_data in doc['terms']:
            term = term_data['term']
            count = term_data['count']
            title = doc['title']
            if term in inverted_index:
                inverted_index[term] += f", {title}:{count}"
            else:
                inverted_index[term] = f"{title}:{count}"

    # Sort the inverted index by terms (alphabetically)
    sorted_index = dict(sorted(inverted_index.items()))

    # Print the sorted inverted index
    print(sorted_index)
