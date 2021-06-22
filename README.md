
<!-- PROJECT OVERVIEW -->
<p align="center">
  <img width="500" src="https://i.imgur.com/mJOjtvo.png">
</p>
<!-- <h1 align="center">Kindle2Notion</h1> -->
<p align="center">
  A program to copy all your Kindle highlights and notes to a page in Notion. 
  <br />
  <a href="https://github.com/paperboi/Kindle2Notion">Explore the docs</a>
  ·
  <a href="https://github.com/paperboi/Kindle2Notion/issues">File issues and feature requests here</a>
</p>
<p align="center">
  If you found this script helpful or appreciate my work, you can support me here:
  <br><br>
  <a href="https://www.producthunt.com/posts/kindle2notion?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-kindle2notion" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=295918&theme=light" alt="Kindle2Notion - Export your Kindle clippings to a Notion database. | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
  <a href="https://www.buymeacoffee.com/jeffreyjacob" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 54px;" height="54"></a>
</p>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

![Kindle2Notion Demo][product-demo]

A Python package to export all the clippings from your Kindle device to a page in Notion. Run this script whenever you plug in your Kindle device to your PC.

A key inspiration behind this project was the notes saving feature on Google Play Books, which automatically syncs all your highlights from a book hosted on the service to a Google Doc in real time. I wanted a similar feature for my Kindle and this project is one step towards a solution for this problem.

**Intended for**
- Avid readers who would want to browse through their prior reads and highlights anytime anywhere.
- For those who take notes alongside their highlights.


<!-- GETTING STARTED -->
## Getting Started


> **NOTE**
> Need a step-by-step guide to setting this package up? Click [here](https://www.notion.so/kindle2notion/Kindle2Notion-8a9683c9b19546c3b1cf42a68aceebee) for the full guide. 

To get a local copy up and running follow these simple steps.

### Prerequisites

* A Kindle device.
* A Notion account to store your links.
* Python 3 on your system to run the code.

### Installation
 
1. Install the library.
    ```sh
    pip install kindle2notion
    ```
2. Export your Kindle highlights and notes to Notion!
   - On MacOS and UNIX,
   ```sh
   kindle2notion 'your_notion_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
   - On Windows
   ```sh
   python -m kindle2notion 'your_notion_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```



<!-- USAGE EXAMPLES -->
## Usage

1. Plug in your Kindle device to your PC.
   
2. Duplicate this [database template](https://www.notion.so/kindle2notion/6d26062e3bb04dd89b988806978c1fe7?v=0d394a8162cc481280966b35a37465c2) to your Notion workspace.
   
3. Find your Notion token. Since this code requires access of non-public pages, an authentication token from your Notion page is required. This token is stored in the `token_v2` cookie. This can be found in the *Storage* tab of your browser's developer tools.
   - For Chrome: Open Developer Tools (*Menu > Other tools > Developer Tools*), navigate to Application tab and go to *Storage\Cookies* to find the token listed next to *tokenv2_*.
    
4. Find your Notion table ID: it's simply the URL of the database you have copied to your workspace.  
   
5. You may modify some default parameters of the command-line with the following options of the CLI:
   - ```--enable_highlight_date```  Set to False if you don't want to see the "Date Added" information in Notion.
   - ```--enable_book_cover```      Set to False if you don't want to store the book cover in Notion.
    
Example:
   ```sh
   kindle2notion --enable_highlight_date=True --enable_book_cover=False 'your_notion_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
   
6. Export your Kindle highlights and notes to Notion!
   - On MacOS and UNIX,
   ```sh
   kindle2notion 'your_notion_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
   - On Windows
   ```sh
   python -m kindle2notion 'your_notion_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
You may also avail help with the following command:
   ```sh
   kindle2notion --help
   python -m kindle2notion --help
   ```

[**Note:** This code has been tested on a 4th Gen Kindle Paperwhite on both MacOS and Windows.]


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/paperboi/Kindle2Notion/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

<!-- Contributions are what make the open source community such an amazing place to be learn, inspire, and create. -->
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE][license-url] for more information.



<!-- CONTACT -->
## Contact

Jeffrey Jacob ([Twitter](https://twitter.com/jeffreysamjacob) | [Email](mailto:jeffreysamjacob@gmail.com) | [LinkedIn](https://www.linkedin.com/in/jeffreysamjacob/))



[contributors-shield]: https://img.shields.io/github/contributors/paperboi/Kindle2Notion.svg?style=flat-square
[contributors-url]: https://github.com/paperboi/Kindle2Notion/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/paperboi/Kindle2Notion.svg?style=flat-square
[forks-url]: https://github.com/paperboi/Kindle2Notion/network/members
[stars-shield]: https://img.shields.io/github/stars/paperboi/Kindle2Notion.svg?style=flat-square
[stars-url]: https://github.com/paperboi/Kindle2Notion/stargazers
[issues-shield]: https://img.shields.io/github/issues/paperboi/Kindle2Notion.svg?style=flat-square
[issues-url]: https://github.com/paperboi/Kindle2Notion/issues
[license-shield]: https://img.shields.io/github/license/paperboi/Kindle2Notion.svg?style=flat-square
[license-url]: https://github.com/paperboi/kindle2notion/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jeffreysamjacob/
[product-demo]: https://i.imgur.com/IlDmEOy.gif
