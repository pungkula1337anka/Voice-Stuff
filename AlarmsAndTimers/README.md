
<h1 align="center">
<br>

Alarms And Timers<br>
<br>

![image](https://github.com/pungkula1337anka/Voice-Stuff/assets/105579081/b034fb2d-28a3-4564-aa55-ad5ed24a4d99)


</h1><br>
<br><br>

# __A single, feature packed, intent_script for all your timer needs__ <br><br>


<br>

_Example usage:_
```
- "set an timer for 8 minutes"
. "wake ne up at 10 30"
[...] 
```
<br>

__Features:__

1. __Start up to 3 Timers simultaneously__  <br> 
`Set a timer for 2 minutes 2 hours` <br>
If timer1 is active, and you'll start another it will automatically start the timer2, and so on. <br>

2. __Start up to 3 Alarms simultaneously__  <br> 
`wake me up at 08 30` <br>
If alarm1 is active, and you'll set another it will automatically set the alarm2, and so on. <br>

3. __Snooze Alarm__  <br> 
Say `snooze` if you are tired. <br>
This will trigger the alarm in 9 minutes again. <br>

4. __Remaining Duration Timers__  <br> 
Say `snooze` if you are tired. <br>
This will trigger the alarm in 9 minutes again. <br>

5. __Status check on Alarms__  <br> 
Say `snooze` if you are tired. <br>
This will trigger the alarm in 9 minutes again. <br>

6. __Turn off Timers__  <br> 
Say `snooze` if you are tired. <br>
This will trigger the alarm in 9 minutes again. <br>

7. __Disable Alarms__  <br> 
Say `snooze` if you are tired. <br>
This will trigger the alarm in 9 minutes again. <br>





<br><br>

<br>


- **1: Download Files** <br>

- **2: Custom Sentence** <br>
If you would want to edit any words, you do it in this file. <br> 


<br><br>


## 🦆 Example Automation <br>


<br>


```
alias: wake_up_alarm
description: ""
trigger:
  - platform: time
    at: input_datetime.wakeupalarm
  - platform: event
    event_type: timer.finished
    event_data:
      entity_id: timer.wakeup    
condition:
  - condition: time
    weekday:
      - fri
      - thu
      - wed
      - tue
      - mon
action:
  - service: timer.start
    data: {}
    target:
      entity_id: timer.wakeup
  - service: media_player.volume_set
    data:
      volume_level: 1
    target:
      entity_id: media_player.ha
  - service: media_player.play_media
    data:
      media_content_id: /local/sound/wakeup.mp3
      media_content_type: music
    target:
      entity_id: media_player.ha
  - service: notify.mobile_app_iPhone
    data:
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1
      title: "⚠️ "
      message: VAKNA
  - delay:
      hours: 0
      minutes: 0
      seconds: 4
      milliseconds: 0
  - service: notify.mobile_app_iPhone
    data:
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1
      title: "⚠️ "
      message: VAKNA
```

<br><br>
