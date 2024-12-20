import json

with open("raw_data.json") as f:
    data = json.load(f)

nodes = []
links = []

for crn, course_data in data.items():
    course_id = f"{course_data['subject_code']} {course_data['course_number']} {course_data['section']} - {course_data['instruction_type']}"

    node_ids = [node["id"] for node in nodes]

    if course_id in node_ids:
        continue

    nodes.append(
        {
            "id": course_id,
            "group": 1,
            "additionalInfo": [
                "Instruction Method: " + course_data["instruction_method"],
                "Section: " + course_data["section"],
                f"CRN: {course_data["crn"]}",
                "Enrollment: " + course_data["enroll"],
                "Max Enrollment: " + course_data["max_enroll"],
                "Course Title: " + course_data["course_title"],
                "Days: " + ", ".join(course_data["days"])
                if course_data["days"]
                else "N/A",
                "Start Time: " + course_data["start_time"]
                if course_data["start_time"]
                else "N/A",
                "End Time: " + course_data["end_time"]
                if course_data["end_time"]
                else "N/A",
                "Credits: " + course_data["credits"],
                "Prerequisites: " + course_data["prereqs"],
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

        nodes.append({"id": instructor["name"], "group": 2, "additionalInfo": []})


groupMapping = {1: "Course", 2: "Instructor"}

with open("course_data.json", "w") as f:
    json.dump(
        {"nodes": nodes, "links": links, "groupMapping": groupMapping}, f, indent=4
    )
