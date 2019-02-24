# PyMessenger

**This project is unmaintained.**

*My attempt at making the Facebook Messenger API as stateful as it deserves to be, taking design inspiration from discord.py*

Facebook Messenger has a pretty cool bot API. That said, it's not really friendly to people who would like to get started. Also, one of its biggest drawbacks is that, while most Messenger bots use buttons to navigate between menus and help users achieve their purposes, it doesn't offer any kind of user-state management in its webhooks and API calls. 

Taking inspiration from the great (to say the least) API that [discord.py](https://github.com/Rapptz/discord.py) is, I decided to create a Pythonic wrapper for Messenger. Its goals are mainly:

* To help with state management 
  * By allowing the developer to pass callbacks for each displayed button when sending a message (internally, the API stores that callback in some kind of map and associates it with a hash that it will get back from the webhook later), it's as cool as it sounds
* To make the API more expressive by using decorators (especially `handler` associated with a given state name)

[Click here to see a cool example!](https://github.com/KowalskiThomas/PyMessenger/blob/master/example.py)
