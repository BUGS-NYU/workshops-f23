from typing import List
from playwright.sync_api import Locator, Page, sync_playwright
import json
import re


"""
Removes whitespace and formats the `textContent` of DOM elements
"""
def cleanTextContent(text_content: str | None):
    if text_content is None:
        return ""
    return re.sub("[\\n\\r]+|[\\s]{2,}", " ", text_content).strip()


"""
Returns a string list of the names of columns in the course schedule table
"""
# Challenge 3.1 (Bonus challenge!)
# Convert this function to use list comprehension. That is, an expression of the
# form [... for ... in ...]
def get_column_names(header_columns: Locator):
    column_names: List[str] = []
    for i in range(header_columns.count()):
        column = header_columns.nth(i)
        column_name = cleanTextContent(column.text_content())
        column_names.append(column_name)
    return column_names


"""
Scrapes the descriptions of a row, representing a course, in the course schedule table
"""
def scrape_course(course: Locator, column_names: List[str]):
    # not needed, but scrolling to the course gives some visual feedback of progress
    course.scroll_into_view_if_needed()

    course_data = {}

    # Challenge 1
    # Replace the TODO below with the right locator to get the descriptions in a
    # row. It may be helpful use the Playwright inspector here.
    #
    # Hint: what HTML element (<p>, <div>, etc.) are each of the descriptions
    # children of?
    descriptions = course.locator("TODO")
    for i, column_name in enumerate(column_names):
        description = descriptions.nth(i)
        # Challenge 2
        # Implement code to get the description text using the above
        # `description` object and set `description_text`
        #
        # Hint: how does `get_column_names(...)` scrape column names?
        description_text = None
        course_data[column_name] = description_text
    return course_data


"""
Scrapes the course schedule table for the given columns
"""
# Challenge 3.2 (Bonus challenge!)
# Convert this function to use list comprehension. That is, an expression of the
# form [... for ... in ...]
def scrape_courses(courses: Locator, column_names: List[str]):
    courses_data = []
    for i in range(courses.count()):
        course = courses.nth(i)
        course_data = scrape_course(course, column_names)
        courses_data.append(course_data)
    return courses_data


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://cs.nyu.edu/dynamic/courses/schedule/")

        page.pause() # Open the Playwright inspector -- comment out this line if you don't want to open it

        header_columns = page.locator(".tableheader div")
        courses = page.locator(".schedule-listing").get_by_role("listitem")

        column_names = get_column_names(header_columns)
        courses_data = scrape_courses(courses, column_names)

        with open("courses.json", "w") as f:
            json.dump(courses_data, f, indent=2)
        print(f"Done scraping {len(courses_data)} courses.")

        browser.close()


if __name__ == "__main__":
    main()
