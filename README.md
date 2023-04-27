# CSC 210 Project 2: Advanced Web Application

## Purpose
Educational site that introduces history and technology for web development, allows users to practice what they learned, and tests users on their web development knowledge.

## Navigation
Navigation is done solely through the navigation bar at the top.  About the Web, Practice, and Test Your Knowledge correspond with "/", "/practice", and "/test" respectively.
### Important URLs
- "/" index page with educational information on web development
- "/practice" page with matching game to let users practice what they learned
- "/test" page with a randomly generated test on web development history and technology
-  "/login" page - login
-  "/logout" page - logout
-  "responses" page - lists the user submitted facts
-  "/sendmessage" page - submit facts about webdev/web history
-  "/signup" page = make an account to login

## Database Configuration
Response columns: id (primary), name, email, subject, message
User columns: id, email, password, name

## Aditional Requirements
- Front end application: sophisticated behavior server-side with JavaScript found in practice.html and used on the "/practice" page.  Users can play a matching game with four sections: history, html, css, and web frameworks.  Each section is shown one at a time.  Matching cards change style when selected and when correctly matched.  Users gain 10 points for a correct match and lose 5 points for an incorrect match, and once all four sections are completed the score is shown.
- JSON parsing for data upon initialization for use on the "/test" page.  The JSON file is parsed in app.py and the data is displayed in a form in test.html.  The JSON file consists of 8 web history questions and 12 web technology questions, all multiple choice with 4 options.  Once the data is parsed in app.py, the order of multiple choice answers are shuffled and half of the questions are randomly chosen to be displayed in the form on test.html.
- Additional Database
- User Authentication

## Group Member Contributions
### Miranda Price
- wrote site content and corresponding html
- set up site navigation
- styled site
- created JSON file for use on "/test page"
- parsed JSON file and used data to create a form on "/test" page
- wrote JavaScript for matching game on "/practice" page

### Sarah 
- worked on DBs, user authentication
