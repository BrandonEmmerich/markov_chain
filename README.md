# Simmons Text Generator

Use a [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) to automatically generate text that, although utterly nonsense, sounds unmistakably like Bill Simmons.

* _"basketball jesus with the spurs and fifth if anyone can beat seattle in round 1 series ever" belt 2010 celts-lakers 2012 celts-heat 1979 bullets-spurs ice blows a 3-1 hole after winning those three seasons even though every inch of a public pariah on par with oj simpson and gluten and before we"_


* _"november 2009 dirk had already carried the mavs to the finals won an mvp he hasnt even won 80 games yet including the playoffs and he couldnt give us decent wi-fi? where is chris paul???"_


* _"nba history who could have handled the v stiviano saga if donald sterling owned them (and not the clippers)? yikes but none of that matters now nobody believes in us or wants to watch him play unfrozen caveman nba coach"_


* _"goodell came off as either a completely and utterly incompetent or b someone who unequivocally said multiple things that turned out my advice: stay humble stay self-deprecating always sound like you dont know me well enough feels like a classic in the making im giddy enjoy the weekend"_


* _"ewing theory potential can get me excited about any of this? if you look at the self-sabotage blueprint that phillys new owners and gm sam hinkie have followed and that was a fairly tough catch i would have thrown in the obligatory "do you know the team i would not trade teams for anyone"_

## How Does it Work?

This program applies a Markov Chain to a corpus of archived Bill Simmons blog posts from his time at Grantland. Specifically, program automatically generates text by determining a random next word given the preceeding three words.

To run the program, first you need the training data to build a [conditional frequency distribution](https://en.wikipedia.org/wiki/Conditional_probability_distribution). Run the `get_corpus.py` program to scrape all 250 Simmons columns from the Grantland archive page.

You can follow the Markov Bill Simmons bot, @markovsimmons.
