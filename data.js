export async function getData() {
  const response = await fetch("course_data.json");
  const responseJson = await response.json();
  return responseJson;
}
