import json

with open("raw_data.json") as f:
    data = json.load(f)

nodes = []
links = []

for crn, course_data in data.items():
    course_id = f"{course_data['subject_code']} {course_data['course_number']}"

    node_ids = [node["id"] for node in nodes]

    if course_id in node_ids:
        continue

    nodes.append(
        {
            "id": course_id,
            "group": 1,
            "additionalInfo": [
                "Course Title: " + course_data["course_title"],
            ],
        }
    )

    if not course_data["instructors"]:
        continue

    for instructor in course_data["instructors"]:
        links.append(
            {
                "source": course_id,
                "target": instructor["name"],
                "value": 1,
                "id": "",
            }
        )

        if instructor["name"] in node_ids:
            continue

        additionalInfo = []
        if "rating" in instructor and instructor["rating"]:
            additionalInfo.append(
                f"Average Rating: {instructor['rating']['avgRating']}"
            )

            additionalInfo.append(
                f"Average Difficulty: {instructor['rating']['avgDifficulty']}"
            )

            additionalInfo.append(
                f"Number of ratings: {instructor['rating']['numRatings']}"
            )

            additionalInfo.append(
                f"<a href='https://www.ratemyprofessors.com/professor/{instructor['rating']['legacyId']}' target='_blank'>View ratings</a>"
            )

        nodes.append(
            {"id": instructor["name"], "group": 2, "additionalInfo": additionalInfo}
        )


groupMapping = {1: "Course", 2: "Instructor"}

with open("course_data.json", "w") as f:
    json.dump(
        {"nodes": nodes, "links": links, "groupMapping": groupMapping}, f, indent=4
    )
