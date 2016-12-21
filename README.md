# Online Game Store -- Plan

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


<<<<EXPLAIN ABOUT LOGIN & REGISTER UI??>>>>


When the user chooses to buy game and clicks buy, the application will open a small window
asking users confirmation of the purchase. If user accepts, game will be purchased and added
to user’s inventory and the pop-up window will be closed. The game is now available for player
to play but in case of declining the purchase, pop-up will just be closed. 

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
### Risk Analysis