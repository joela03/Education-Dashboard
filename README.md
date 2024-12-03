# Mathnasium Dashboard

This project aims to create a dashboard to monitor the performance of students at Mathnasium. The dashboard interacts with the Mathnasium Radius website using Selenium, extracts key student data, and analyzes their progress to ensure they are working at an appropriate pace and on track to complete their learning plan within 6 months of starting.

## Features

- **Extract Daily Student Roster**: Automatically extract the daily student roster from the Radius website.
- **Track Student Progress**: For each student, retrieve the last three sessions to calculate the average pages completed per session.
- **Pace Analysis**: Determine if a student is working at an appropriate pace based on average pages completed.
- **Learning Plan Monitoring**: Compare the student's progress against their learning plan to decide whether to assign a progress check or evaluate if the student is on track to finish within 6 months.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Selenium
- WebDriver (Chrome, Firefox, etc.)
- Pandas (for data analysis)
- Other dependencies listed in `requirements.txt`

## Setup

1. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
2. **Download WebDriver**: 
    Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and ensure it is in your system's PATH.
3. **Configure the Script**: 
    You will need to update the script with your Mathnasium login credentials and any specific configurations related to the Radius website.

## How It Works

### 1. **Logging into Radius**
   The script uses Selenium to automate logging into the Radius website by navigating to the login page and entering your credentials (username and password). Once logged in, it proceeds to the student management section.

### 2. **Extracting the Daily Student Roster**
   After login, the script navigates to the section of the website where the daily student roster is available. It extracts the list of students and stores the names and other relevant details (such as student ID or session info) for further analysis.

### 3. **Tracking Student Progress**
   For each student in the roster, the script performs the following steps:
   
   - **Search for the Student**: The script searches for each student in the student management section.
   - **Extract Sessions Data**: For the last three sessions of each student, the script extracts the number of pages completed during each session.
   - **Calculate Average Pages**: The average pages completed per session over the last three sessions are calculated.

### 4. **Pace Analysis**
   The script compares the average pages completed in the last three sessions against a pre-defined threshold to determine if the student is working at an appropriate pace. If the student is completing too few pages per session, it may indicate that they are falling behind in their learning plan.

### 5. **Learning Plan Comparison**
   The script retrieves data on how far the student is through their learning plan and compares it to the expected timeline. The analysis checks if the student is on track to finish the plan within 6 months from the start date. If they are falling behind, the script will recommend whether a progress check is needed or if an intervention is required.
