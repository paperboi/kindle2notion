
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
  - [Installation & Setup](#installation--setup)
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
- For those who like to take notes alongside their highlights.


<!-- GETTING STARTED -->
## Getting Started


> **NOTE**
> Need a step-by-step guide to setting this package up? Click [here](https://kindle2notion.notion.site/Kindle2Notion-8a9683c9b19546c3b1cf42a68aceebee) for the full guide. 

To get a local copy up and running follow these simple steps:

### Prerequisites

* A Kindle device.
* A Notion account to store your links.
* Python 3 on your system to run the code.

### Installation & Setup

> **NOTE** 
> As of 10-08-2022, the latest update to this package relies on the offical Notion API for sending API requests. This requires you to create an integration token from [here](https://www.notion.so/my-integrations). For old users, you'd have to switch to this method as well since `notion-py` isn't being maintained anymore.
 
1. Install the library.
    ```sh
    pip install kindle2notion
    ```
2. Create an integration on Notion.
      1. Duplicate this [database template](https://www.notion.so/aea4216c8a4b4269b43c8d4cd7fb9ad2?v=4cbb5a5c6cbb45f6910e606a144d1d79) to your the workspace you want to use for storing your Kindle clippings.
      2. Open _Settings & Members_ from the left navigation bar.
      3. Select the _Integrations_ option listed under _Workspaces_ in the settings modal.
      4. Click on _Develop your own integrations_ to redirect to the integrations page.
      5. On the integrations page, select the _New integration_ option and enter the name of the integration and the workspace you want to use it with. Hit submit and your internal integration token will be generated.
3. Go back to your database page and click on the _Share_ button on the top right corner. Use the selector to find your integration by its name and then click _Invite_. Your integration now has the requested permissions on the new database. 


<!-- USAGE EXAMPLES -->
## Usage

1. Plug in your Kindle device to your PC.
    
2. You need the following three arguments in hand before running the code:
   1. Take `your_notion_auth_token` from the secret key bearer token provided at 
   2. Find `your_notion_database_id` from the URL of the database you have copied to your workspace. For reference,
      ```
      https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...
                                        |--------- Database ID --------|
      ```
   3. `your_kindle_clippings_file` is the path to your `My Clippings File.txt` on your Kindle.

3. Additionally, you may modify some default parameters of the command-line with the following options of the CLI:
   - ```--enable_highlight_date```  Set to False if you don't want to see the "Date Added" information in Notion.
   - ```--enable_book_cover```      Set to False if you don't want to store the book cover in Notion.
    
4. Export your Kindle highlights and notes to Notion!
   - On MacOS and UNIX,
   ```sh
   kindle2notion 'your_notion_auth_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
   - On Windows
   ```sh
   python -m kindle2notion 'your_notion_auth_token' 'your_notion_table_id' 'your_kindle_clippings_file'
   ```
You may also avail help with the following command:
   ```sh
   kindle2notion --help
   python -m kindle2notion --help
   ```

> **NOTE**
> This code has been tested on a 4th Gen Kindle Paperwhite on both MacOS and Windows.


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
