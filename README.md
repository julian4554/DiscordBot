<h1>Discord Bot</h1>



<h2>Description</h2>
Here i just created a Discord Bot within some days for my friends and for learning purposes.
Initially i created Herman for a friend that asked whether i could track his League of Legends ranked games in our Discord Channel.
This Discord bot also offers several automated features. It tracks the International Space Station (ISS) to determine if it's passing over our heads and then sends a message greeting us. Additionally, Herman provides daily weather updates for a predefined location and shares them with us. It sends a daily quote from "Herr der Ringe" (Lord of the Rings) and the NASA Picture of the Day to the Discord group. 
The provided code defines several asynchronous functions and uses the apscheduler library to schedule and execute these functions at specific intervals. 
<br />

<h2>Improvements and future ideas</h2>
Lately i learned a lot about Data Science and Machine Learning Models so i thought about updating the functions.
I want the Bot to run 24/7 on a Raspberry Pi with Docker but due to the global Semiconductor Shortage and other factors(2022) i have yet not ordered a new one where i would run the bot on.
Anyway if i get one i will update the player analysis of the game function with regression models and more.



<h2>Languages and Utilities Used</h2>

- <b>Python</b> 
- <b>Discord.py</b>
- <b>APScheduler</b>
- <b>Geopy</b>
- <b>Api requests</b>
- <b>And more...</b>

<h2>Program walk-through:</h2>

<p align="center">
Function 1: Notification when ISS is orbiting over us <br/>
<img src="https://github.com/julian4554/DiscordBot/assets/28981754/7dd155b8-79b1-4674-80e0-e5d1aba6dfb9" height="80%" width="80%" alt="Notification if ISS is orbiting over us"/>
<br />
  Function 1 Code: <br />
  <img src="https://github.com/julian4554/DiscordBot/assets/28981754/4d8df1f8-825c-4a34-910c-a5002053e55f" height="80%" width="80%" alt="Notification if ISS is orbiting over us"/>
<br />
Function 2: Weather notification in the morning <br/>
<img src="https://github.com/julian4554/DiscordBot/assets/28981754/bdbc3ca5-9dc3-4cd0-9f47-dc6e7e4197e3" height="80%" width="80%" alt=""/>
<br />
  Function 2 Code: <br />
  <img src="https://github.com/julian4554/DiscordBot/assets/28981754/f8f797a5-374d-4e3f-86c0-a7451b4460dd" height="80%" width="80%" alt=""/>
<br />
Function 3: Sends Nasa picture of the day <br/>
<img src="https://github.com/julian4554/DiscordBot/assets/28981754/dcbbbfdf-4b0d-4beb-b95a-0c06418b3b84" height="80%" width="80%" alt=""/>
<br />
  Function 3 Code: <br />
  <img src="https://github.com/julian4554/DiscordBot/assets/28981754/031975a0-2b42-4393-b3c9-228dd9c528d9" height="80%" width="80%" alt=""/>
<br />
  Function 4: Notification when a friend finishes a League of Legends match. Information via RiotDev Api <br/>
<img src="https://github.com/julian4554/DiscordBot/assets/28981754/c5f57ac7-b3d2-4b32-af1f-f2c5fc17e9c9" height="80%" width="80%" alt="Notification if ISS is orbiting over us"/>
<br />
  Function 4 Code: <br />
  <img src="https://github.com/julian4554/DiscordBot/assets/28981754/74e3ef11-b0eb-4a20-813e-84b69eb77114" height="80%" width="80%" alt="Notification if ISS is orbiting over us"/>
<br />
<img src="https://github.com/julian4554/DiscordBot/assets/28981754/64d71582-ab18-4e08-bf5c-d9ec431fe8b2" height="80%" width="80%" alt="Notification if ISS is orbiting over us"/>
<br />
</p>

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
