
# I51 AutoSS Script
## Author

- [@asdJPasc / I51](https://github.com/asdJPasc)

This script automates the task of capturing full-page screenshots of multiple web pages listed in an Excel file. It utilizes the power of Python and the Playwright library to navigate through websites, remove unwanted elements, and capture comprehensive screenshots, providing users with a visual snapshot of each webpage.


## Features

- Effortless Automation: The script handles everything automatically, saving you time and effort.
- Customizable Configuration: Easily customize the interval between screenshot captures, ensuring flexibility to meet specific needs.
- Dynamic Element Removal: Unwanted elements like headers, footers, or pop-ups are automatically removed before capturing screenshots, ensuring clean and focused images.
- Captcha Detection: The script intelligently detects and skips web pages with CAPTCHA challenges, preventing interruptions in the automation process.
- Persistent Browser Context: With a persistent browser context, the script efficiently manages resources, optimizing performance and reliability.
- Interrupt Handling: The script gracefully handles interruptions such as keyboard interrupts, ensuring a smooth exit while maintaining browser integrity.
- Easy Setup: Simply provide the URLs in an Excel file, specify the capture settings, and let the script do the rest.


## Ideal Use Cases:
- Monitoring website changes for competitive analysis.

- Tracking online content for compliance or regulatory purposes.

- Collecting visual data for research or trend analysis.

- Automating periodic website snapshots for archival or historical records.
## Current Limitation and Ongoing Development:
- Captcha Puzzle Handling: The script currently lacks the capability to bypass captcha puzzles automatically. Once a captcha puzzle is detected, it notifies the user to manually capture the specific row ID for further action. Development is ongoing to implement captcha solving mechanisms.

- Partial Website Configuration: Not all websites listed in the Excel file may be fully configured to navigate and capture screenshots seamlessly. Additional configuration may be required for specific websites to handle unique elements or interactions effectively. Users are encouraged to request guidance from the developer for the necessary steps needed to configure these websites before capturing the required content.

These limitations are being actively addressed by the developer to enhance the script's functionality and user experience. Your feedback and suggestions are invaluable in driving future improvements.
## How to Use:
Notes: Ensure you have latest Python installed:

- Download the script [HERE](https://github.com/asdJPasc/AutoSS/archive/refs/heads/master.zip)
- Extract the downloaded ZIP file to your desktop.
- Open the extracted folder named "AutoSS-master".
- Inside the folder, locate and double-click on the "install.py" file.
- Open the "agent.xlxs" file using Microsoft Excel or a compatible spreadsheet program.
- In the spreadsheet, set the URLs, RowID, Folder, and Extension.
- Save the "agent.xlxs" file after configuring the settings.
- Return to the folder containing the script and the "agents.xlxs" file.
- Run the script by double-clicking the auto.py.


