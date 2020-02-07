# Space Wiki - A website where all can collaborate in defining space and astronomical terms.

## This site has been created as part of my CodeInstitute milestone project for the data centric development module.

This site is a web application to create, search, vote and delete definitions. In a similar way to Urban Dictionary for example.

The benefit of this application is providing a tool where one can access and contribute to a library of space and astronomical terms.

The intention is for all terms to be collated and created in book form.

## UX

**Wireframes are in the wireframes directory**

**Please note this site does not implement authentication as per the project brief. Therefore anyone can edit and delete another's post. In production I would implement user-registration (e.g. with Google). Deleting/editing would only be allowed by the original author.**

The site had to be simple and intuitive to use.

The project brief did state I can use Urban Dictionary or Wiktionary as inspiration. I liked the use of cards on Urban Dictionary and because of support on Bootstrap I decided on that.

On smaller screens the side bar and nav bar collapses. The cards re-size dynamically.

The colour scheme was chosen using Coolors.co but I did specifically look for one that would fit a space theme - 'cosmic' colours with some dark backgrounds (cards).

The main page loads definitions from the latest descending, but with the caveat that those presented need to be flagged as the top definition.

The concept of top definition allows us to flag which of those have received the most votes. These definitions are flagged with a star (to fit with the theme!).

To facilitate votes, a thumbs up button is implemented on each card. If there is a tie, then the oldest definition wins. New definitions are top automatically.

Edit and delete functionality is also provided for each card.

There is search functionality which searches the back end database for definition names and their text. Comments in the code but this is made possible using a MongoDB Index.

Finally, on the cards, the original author is detailed under the term. At the card footer is the original creation date and time. **If** it has been edited then another footer entry will appear with the editor. Since the project isn't using authentication (comments above), then this allows tracking of definition history.

### User Stories

- As the operator of this site, I wish to collect a definitive list of definitions to eventually publish in a book.
- As a professional in the industry / enthusiast / teacher, I wish to contribute to a collaborative platform to help educate others on definitions.
- As a student, I wish to search for space terms to aid my learning.
- As an astronomer / enthusiast, I wish to search for space terms to aid my learning.

## Features

### Existing Features

- Feature 1 - Ability to create definitions.
- Feature 2 - Ability to edit definitions.
- Feature 3 - Ability to delete definitions.
- Feature 4 - Ability to vote for definitions. Top definition (most votes) is flagged with a star. This allows for easy identification of the most credible definition.
- Feature 5 - Input field allowing users to enter search conditions for definition names and the definition text itself.
- Feature 6 - Search results based on MongoDB index allowing case-insensitive searching across definition names plus the text of the definition itself. Search results ordered newest first, all matches.
- Feature 7 - Original author and date of submission recorded and displayed on card.
- Feature 8 - Editor (if any) added as extra footer on card, along with edit date/time.
- Feature 9 - Main page layout orders by newest first, but **only** top definitions.


## Technologies Used

The following is a list of all the technologies used in this website.

- [Python](https://www.python.org/)
  - This logic of this application is coded in Python.
  
- [Flask](https://flask.palletsprojects.com/)
  - Python logic is augmented with Flask to provide the web page structure.

- [Bootstrap 4.3](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
  - This project uses **Bootstrap** to provide the website's structure. I have relied heavily on its card components and navbar as well as being flexible on mobile devices.

- [FontAwesome](https://fontawesome.com/start)
  - This project uses **FontAwesome** for the various button icons and top definition flag.

- [Google Fonts](https://fonts.google.com/)
  - This project uses **Google Fonts** for the site's fonts. Specifically Asap.

- [MongoDB / MongoDB Atlas](https://cloud.mongodb.com/)
  - The information presented to the page is stored and delivered from MongoDB Atlas

- [Coolors.co](https://coolors.co/)
  - This service was used to generate this application's branding, including logo, images and colour-scheme.

## Testing

1. Navigation / General functionality:
    1. Main page redirects correctly to /space.
    2. Cards are loaded in the order as designed (latest date, descending). When a duplicate exists (tested), only the top definitions are presented.
    3. Search page loads as expected. If there is no match, a flash message correctly shows up with the appropriate message.
    4. When a match is made, the correct card(s) show. When there is more than one match, cards show latest at the top, descending. Regardless of top definition, all matches are displayed in this way.
    5. Tested searching against both the definition name and something within the definition itself. Tried with both upper and lower case. E.g. if I search for "moon" or "Moon", the Moon definition is shown. If I search for 'natural', Moon is returned again because that word appears in the definition.
    
2. Data operations:
    1. Clicking the add new definition button (both navbar and side bar on larger screens), the correct form is displayed.
    2. Creating a new definition works and correctly marks as top definition.
    3. Creating a duplicate definition - successfully created and it, correctly, is not marked as top.
    4. On creation, the author and timestamp is correctly recorded and displayed on the card.
    5. Editing correctly shows form and auto-populates original author in a read-only field. Submitting successfully changes record and correctly shows edited by and edited timestamp.
    6. Cancel button on edit and add works as intended without affecting the record.
    7. Deleting works as intended and flash message is shown providing feedback.
    8. Voting works as intended by incrementing the vote count. Vote count is displayed next to icon.
    9. Voting for a duplicate record correctly evaluates the vote counts and does not mark a record as top until it has more votes. In the event of a tie, the older definition wins.
    10. Voting correctly provides flash message as feedback.

- Responsive Design:
    1. The above tests were carried out with varying screen sizes (using Chrome Dev Tools).
    2. On small screens the navbar collapses and the burger icon is displayed and works. The side bar disappears as designed, leaving just the cards.
    3. Cards reduce in size correctly.

## Deployment

This site was developed using PyCharm and is hosted on Heroku. The backend database is hosted on MongoDB Atlas.

- Installation
    1. Clone Github Repo.
    2. Create MongoDB Atlas database.
    ***** TBC ********

## Credits

### Content

- All text on the page was written by myself.

### Media

- Google images for the local image content.

### Acknowledgements

- W3Schools for various coding help / templates.
- Urban Dictionary for layout and functionality inspiration.