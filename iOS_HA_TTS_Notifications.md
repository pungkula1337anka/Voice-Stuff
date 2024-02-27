
<h1 align="center">
<br>

Home Assistant Text to Speak Notifications

</h1><br>
<br><br>


According to the Home Assistant docs iOS TTS notfications is not possible. <br>
This is technically not true. Here is a workaround using iOS settings. <br>
Follow insctructions below to get it turned on. <br> 
<br><br><br>


- **1: Grab your Apple device and lets get starteds** <br>

I have iOS set to Swedish, so will do my best to guess here.. <br>

Settings > Siri > Read notifications > Toggle the Read notifications button. <br>

- **2: Scoll down to Home Assistant** <br>

When your in Settings > Siri > Read notifications > Home Assistant, turn it on at the top. <br>
Then scroll down and toggle the All notifications button<br>



<br><br>




## 🦆 Ready to try it out? <br>


<br>


```
service: notify.mobile_app_antons_iphonetest
data:
  message: I am not reading this?
  title: This is not text to speak?
  data:
    push:
      sound:
        name: default
        critical: 1	# Talks when its on silnce.
        volume: 1
```

<br><br>



