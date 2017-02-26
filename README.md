# Online Game Store -- Plan and [document](#document)

### Team
529523: Karri Lehtiranta
294557: Ville Viinikka
479864: Jonatan Lehtinen    

### Overview
Our project goal is to implement an online game store for JavaScript games, 
which allows game developers to play and add their games to be available for 
purchasing and players to buy and play these games online. Developers and 
players can log in to access account restricted functionalities, but the store 
will also be visible for logged out users, but they won’t have any developer
or player functionalities available. 

In addition to these basic functions, we are planning to also implement extra 
features to our store including RESTful API, mobile friendliness, 3rd party login, 
social media sharing and save/load game. To implement this web application,
we will be using Django framework and combined with jQuery and Bootstrap we ensure 
efficient development and mobile friendliness of the user interface.
Our results will be deployed to Heroku. 

### Plans
#### Database:

The planned database schema is illustrated in the ER-diagram below. 
This diagram can be translated into the following relations:

User (email, name, password) 
Player(email, name, password) 
Developer(email, name, password) 
Game (ID, name, description, category, price, purchaseCount, developerEmail)
GamesOfPlayer (gameID, username, highscore, gameState)

User is a relation provided by Django authentication, and will be used in our project. The Player
and Developer relations are created as subclasses of User thus dividing the different
functionalities they require but keeping them both as a user.

In the Game relation we have the unique game ID as key and several self-explanatory fields.
Category field can be one of several pre-determined categories for games. DeveloperEmail is
the email of the developer of the game.

![alt text](https://git.niksula.hut.fi/lehtinj14/online-game-store/raw/master/img/ER-onlinegamestore.png)

GamesOfPlayer relation contains information about player’s owned games. Keys from Game
and Player relations will be the key of this relation together. The relation also contains
information the highscore of the player and the saved game state of the particular game.

With this data structure we can enable Developers to buy and play games too. 

#### User Interface:

![alt text](https://git.niksula.hut.fi/lehtinj14/online-game-store/raw/master/img/ui%201.png)
![alt text](https://git.niksula.hut.fi/lehtinj14/online-game-store/raw/master/img/ui_2.png)
![alt text](https://git.niksula.hut.fi/lehtinj14/online-game-store/raw/master/img/ui_3.png)
The user interface as seen above consists of one simple menu with these options: Store and
Categories (drop down menu) and depending on the state of the session: Log in, Log out,
Register, My games, Manage Games. In addition, there is a search bar where the user can filter
the games in the store or his own library.

The basic view of the website is to show tiles of games, where in each tile contains the following
information of the game: Name, image if provided and either the price of the game if the player
doesn’t own the game or text ‘Owned’ if the player owns the game. Clicking on the game opens
the game page with the following functionalities: If the user owns the game, he can play it in this 
view. This view also shows the global highscores for the particular game. If the user hasn’t 
purchased this game, the page will show the game description and has a button to buy the
game, which opens the buying view. Note that an user doesn’t have to be logged in to browse
the games, but he cannot play or buy the games unless he logs in or registers.

Using categories or the search will modify the above view only by reducing the amount of tiles
which are listed. The ‘My Games’ view of the user works similarly, but only showing the games
he/she owns. 

The view of the ‘developer’ is similar to the ‘player’ view as the player can also buy games. The 
only addition is the ‘Manage Games’ tab in the menu where the developer can see the games 
he has listed in the store. The button opens a view similar to other game browsing views with a 
few differences: The first tile in the UI will be a ‘Add game’ tile and by clicking it will open a 
pop-up view where the developer can add a new game to the service and when the developer
has chosen the game, he will see a view where he can edit all the information of the game as
well as delete the game.

Users will have to register to the site to access all of its functionality. The registration will
will be implemented as a separate form where the user can fill their personal information. If the
user isn't currently logged in, there will be a link to the login and registration pages on every
page. During registration, the user can choose if they want to create a developer or a player
account. The login page will be the same for both user types. We will also provide the ability to
log in with a Facebook account. Only registered users can buy games. If the user isn't logged in,
instead of a buy button, there will be a suggestion to log in or register.

When the user chooses to buy game and clicks buy, the application will open a small window
asking users confirmation of the purchase. If user accepts, game will be purchased and added
to user’s inventory and the pop-up window will be closed. The game is now available for player
to play but in case of declining the purchase, pop-up will just be closed. 

#### Authentication

To authenticate to the site, the user will have to have a valid username and password combination
and to also have validated their email address with a automated message. Alternatively, they can
use a Facebook account to log in. Django auth will be used for user management and authentication.
To securely transport personal information and passwords, HTTPS will be used as the protocol for
communication. 

#### Player’s functionalities:

The player can find games using the store where the games will first be ordered by the number
of purchases the game has and the player can then filter the games by category or by searching
for a game. Player can buy games (payment description below) and after the purchase the
game will be added to GamesOfPlayer model which the application will the query and see if the
player is allowed to play the game. The player will also have access to ‘Your Games’ view where
the player can see all the games he owns.

#### Payment: 

The payment will be implemented using external Simple Payment service where we post 
different parameters according to its documentation to simulate payment. We first display a
simple form which shows user the amount of the payment and user then has a possibility to
accept or decline the payment. Form also includes hidden instances which are sent to the
payment system such as payment id and reference number, but they are invisible to the user.
When payment is complete, user will be redirected to the game in case of successful
purchasing.

#### Developers’ functionalities:

The functionality for developers’ to have a possibility to see their own game inventory, 
modify their games and displaying downloads will be implemented using our models for they 
are containing everything we need to display this information. This is also a secure path 
since this model is only modified, when developer adds a new game, so it’s not possible for
example to modify someone else’s game.

#### RESTful API:

To implement this extra feature we will be using Django Rest framework. Our goal is to offer an 
API where high scores and available games can be fetched and we even offer sale numbers for authenticated developers. 

#### Social media sharing:

We will enable the users to share their games on Facebook. For this we will use the Facebook API.


### Process and Time Schedule
#### Communication:

General communication is done in the project Telegram group. We also have a Trello board 
for our project where we can track the current status of the project. The work distribution 
is also visible there. Branches are used on our GitLab-project. We have also scheduled a meeting 
every week for 1-2 hours for discussing the situation of the project, current workload and possible problems.

#### Schedule:

Preliminary schedule is the following:

Weeks 1 - 2: -Basic UI functionalities, creating the database, games can be played and added, basic authentication, basic deployment to Heroku.

Weeks 3 - 5: UI almost ready, payment system, communication with the game, 3rd party login, 
basic views of the website are ready and functional: Games can be browsed, add, modified and deleted. Highscores will be shown. 

Weeks 6- 7: Social media sharing, refining UI and the views, RESTful API. Testing, documenting and deploying. 


### Testing

Automated test cases will be provided for the most critical functionality. Rest will be tested manually
at the same pace as new functionality is added. Testing the user authentication verification and
security will be a high priority for us.

### Risk Analysis

The team members are well committed to the project and should have all the resources to execute
the project as planned. Time management and communication can be challenges for our project,
but the use of Trello for task management and having regular meetings should improve accountablity and
communication.

# Document

### Task division

In the beginning of the project when deciding the main features and planning the project we also divided the tasks as equally as we could. 
We created a Trello board for all these tasks and for all tasks we marked the person in charge. 
Link to this board https://trello.com/b/rPwbd7Ux/wonderful-app where the work distribution can be found. 

### Implemented features

#### Basic player functionalities: 

Player can browse through games by using search querys and categories. While searching, the games will automatically be loaded into the page. 
New games can also be loaded dynamically by scrolling the page (if the store contains that many games). A player can view his own games in 'My Games' view. 
Player is capable of buying a new game using the payment system provided by the course’s mockup payment service. This feature should be secure since 
the payment service uses checksums to validate the posted data and on our server checksum is also validated. The most difficult part was to make sure 
this functionality is secure and that it can’t be misused.

#### Basic developer functionalities: 

Developer can add games and manage his own games. When developer is trying to add new game or modify one, our implemented functions check that 
the data posted by the developer to our server is valid and that it doesn’t for example cause any constraint violations to our database. 
It was straightforward to implement this data validation using Django’s Forms but problems arose when user tried to set game’s name to one that 
already existed and after this trying to return a view so that the user experience wouldn’t suffer. Developers are also capable of checking their 
sale statistics from the manage view and the security restrictions including that developer can only modify his own games are also implemented. 
As we have implemented every required feature from we would give ourselves the maximum points this category.

#### RESTful API:

As an extra feature, we have also implemented an REST api to offer highscores, information about available games and 
sales statistics and it is implemented using Django REST Framework. Access to these sales statistics requires Developer 
account and this api uses Tokens to authenticate the GET request. Tokens are only distributed to Developers and the token has 
to be included in the headers of the GET request so no normal user can access information about developer’s sales statistics. 
There were no problems implementing this feature and we were hoping to get the maximum points from this feature.  


#### Mobile Friendly:
The website was made mobile and tablet friendly by cleverly using the CSS-library Bootstrap and its features. 
The page will scale itself according to the size of the window use. Mobile friendliness has also been kept in mind 
when positioning items and in general design. A challenging thing was to make all the elements not overlap or overflow from their
containers when resizing windows.

#### Game/service interaction
The complete set of game-service interaction features was implemented for the site. This includes saving and loading the game state data,
which is done using ajax from the server. High score list is updated locally to minimize latency, but the updates are also propagated to
the server database. The site will inform the game if any of the operations fail or are invalid.

#### Social media sharing
Games can be shares on Facebook. The share will include the game's image, title and description.

#### 3rd party login
Login using Facebook account was enabled by using Python Social Auth modules social-core and social-app-django.

#### Authentication
In addition to Facebook login, the user can also register a account directly to the site. The use of Django Auth features
should guarantee the robustness of the system. Since we have implemented the email verification and the other features well, 
we would like to get the maximum points.

#### Quality of work:

When implementing this project our goal has been to write quality code and use the model-view-template structure, 
although in some cases it has not been easy to follow DRY policy, for example when parsing posted data. 
We have commented our code and ensured with automatic tests and manual tests functionality and security of our main functions. 
We have tried to make the user experience as smooth as possible by making a clean UI with multiple smart functionalities like instant search, 
dynamic page loading and mobile friendliness. Since we have tried to make certain that our work is of high quality, 
we would like to get the maximum points.   


### How to use:

The website is located in https://frozen-stream-39780.herokuapp.com/. The website has developers and players. 
Player functionalities can be tested by using your Facebook-account or by creating an account by using the register functionality. 
You can choose whether you want to create a player or a developer. Facebook accounts will automatically be of player-type. 
A confirmation email is sent to the email you specified if you created your account without Facebook. 
As the course documentation suggested, this was implemented with Django's Console Backend, so no actual emails are sent.




