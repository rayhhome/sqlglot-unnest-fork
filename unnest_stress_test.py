from sqlglot.optimizer.unnest_subqueries import unnest_subqueries
from sqlglot.executor import execute
import sqlglot

# Dummy table
tables = {
  "students": [
    {"id": 1, "name": "Alice", "major": "CS",          "year": 2023},
    {"id": 2, "name": "Bob",   "major": "CS",          "year": 2022},
    {"id": 3, "name": "Carl",  "major": "Games Eng",   "year": 2023},
    {"id": 4, "name": "Diane", "major": "Business",    "year": 2023},
  ],
    "exams": [
    {"sid": 1, "course": "Math101", "grade": 90, "curriculum": "CS",        "date": 2022},
    {"sid": 1, "course": "CS102",   "grade": 85, "curriculum": "CS",        "date": 2023},
    {"sid": 2, "course": "CS102",   "grade": 70, "curriculum": "CS",        "date": 2023},
    {"sid": 3, "course": "ART101",  "grade": 95, "curriculum": "Games Eng", "date": 2022},
    {"sid": 3, "course": "ENG205",  "grade": 88, "curriculum": "Games Eng", "date": 2023},
    {"sid": 4, "course": "Math101", "grade": 60, "curriculum": "Business",  "date": 2022},
  ],
}


# Query 2 from German 2015 paper
query = """
SELECT s.name, e.course
FROM students s, exams e
WHERE s.id = e.sid
  AND (s.major = 'CS' OR s.major = 'Games Eng')
  AND e.grade >= (
    SELECT AVG(e2.grade) + 1
    FROM exams e2
    WHERE (s.id = e2.sid)
       OR (e2.curriculum = s.major AND s.year > e2.date)
  )
"""

# Parse the query with the current SQLglot Unnesting code
expression = sqlglot.parse_one(query)
# print(expression)
print("nested:", expression.sql())
unnested = unnest_subqueries(expression)
print("unnested:", unnested.sql())

# Try executing the query, should error for now
result = execute(unnested.sql(), tables=tables)
print(result)