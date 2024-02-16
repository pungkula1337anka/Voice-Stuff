
<h1 align="center">
<br>
Joke
</h1><br>
<br><br>
Tells a random joke from a file.<br>
<br><br>

- **1: Joke File** <br>
Create an file within your /config folder called 'jokes'<br>
Paste in your jokes in this file.<br>
One line per joke only.<br>


- **2: Command line sensor ** <br>
Create the command line sensor. Paste in code below.<br>

- **3: Intent Script** <br>

Create the file 'intent_script.yaml' file in the /config dir and fill in the code below.


- **4: Custom Sentence** <br>

Create a folder called 'custom_sentences' inside your /config dir.
Inside that folder, once again create a folder named with your language code. 'sv' for swedish, 'en' for english.
In that folder you create a file called 'joke.yaml' and fill in the code from below. 




## 🦆 /config/command_kine.yaml <br>


<br>

```
  - sensor:
      name: joke
      command: 'shuf -n 1 /config/jokes'

```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>

```
Joke:
  speech:
    text: "  {{ states('sensor.joke') }} "

```

<br><br>


## 🦆 /custon_sentences/sv/PlayArtist.yaml <br>


<br>

```
language: "sv"
intents:
  Joke:
    data:
      - sentences:
          - "säg ett skämt" 
```

<br><br>




