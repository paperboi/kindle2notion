# Kindle2Notion

Export all the clippings from your Kindle to a page in Notion.

## To Do

- [x] Parse through the  My Clippings.txt file and break it down to discrete chunks of data, namely
  - [x] Remove all unnecessary characters.
  - [x] Get book title, author(s) and other auxiliary information.
  - [x] Format the highlights into consistent text.
  - [x] Place these contents together in a class object.
- [ ] Send these chunks of data through the notion.py API to be placed into pages and blocks.
  - [ ] Create Book Vault page in Notion.
  - [ ] Add a database with relevant properties for the page.
  - [ ] Write a class to handle Notion/write operations and functions.
- [ ] Keep track of data already processed - so as to avoid any redundancies.
- [ ] Write a script to run this process upon mounting the Kindle for Windows.
- [ ] Notion logger calls throughout the script