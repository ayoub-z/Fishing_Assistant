<p>
   <div align="center">
   <img width="900" src="https://github.com/ayoub-z/Fishing_Assistant/blob/master/Poster.png"></a>
   </div>
</p>

---

## Demo video - Fishbot &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Demo video - Escape feature

<a href="http://www.youtube.com/watch?feature=player_embedded&v=Bm_ktmQUGPc
" target="_blank"><img src="http://img.youtube.com/vi/Bm_ktmQUGPc/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="380" height="285" border="10" /></a>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=hZyNFjJBaTk
" target="_blank"><img src="http://img.youtube.com/vi/hZyNFjJBaTk/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="380" height="285" border="10" /></a>
---

<details open>
<summary>Install</summary>
 
Clone repo and install [requirements.txt](https://github.com/ayoub-z/Fishing_Assistant/blob/master/requirements.txt). Make sure to have [**Python 3.9.0**](https://www.python.org/downloads) or higher.

```bash
git clone https://github.com/ayoub-z/Fishing_Assistant  # clone
cd Fishing_Assistant
pip install -r requirements.txt  # install
```
  
</details>

---

<details open>
<summary>User guide - fishing bot</summary>
In order to use the Fishing Assistant, you will need to setup some things. <br>
If you don't care about the escape feature, then you only need to setup "template image" and "threshold". Everything else can stay on the default valuees.  

1. **Fishing ability**: <br>
   Set the fishing ability to the default key '1'. To change the default key, head to the function `start_fishing()` in [bot.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py).
2. A **template image** of the fishing bobber: <br>
   Take a screenshot of the current bobber in the water and crop the image so only the fishing bobber remains.<br>
   It is recommended to zoom the camera out slightly, instead of zooming in all the way when taking the screenshot, as this has given better results.
3. **Threshold** (recommended to be between 0.4 - 0.8): <br>
   To get the most optimal threshold, set `calculate_best_threshold` to True in [main.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py) and run the code. The assistant will find the best threshold for the current bobber.
4. Apply **fishing lure**: <br>
   Set `apply_lure` to True in [main.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py) to apply the lure every 10 min. The default key for applying the fishing lure is '2'. To change this key, head to the function `start_fishing()` in [bot.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py).
5. **Live feed** of what the bot sees: <br>
   Set `live_feed` to True in [main.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py).
</details>

<details open>
<summary>User guide - escape feature</summary>  
In order to use the **Escape feature**, you need to setup the following: <br>
For this you will need the following: <br>
  
1. Set `escape_feature` to True in [main.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py). <br>
2. You will need the addon ElvUI. Inside ElvUI, you need to set the enemy frames' healtbar to be red. <br>
3. You will need to setup a macro with the abilities `/cast Shadowmeld` and `/cast Flight Form`. <br>
4. Place the macro on the key 'g'. To change this key, head to the function `escape_feature()` in [bot.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/main.py).<br>
5. The x and y position of the enemy frame as well as it's height and width. You can set this up in the `find()` function under the 'find_enemy' if statement in [vision.py](https://github.com/ayoub-z/Fishing_Assistant/blob/master/vision.py).
  
---
 </details> 
 
 ## <div align="center">Ban safety</div>
 During the making of this project, the Fishing Assistant has been tested for 75+ hours, with the testing being no more than 3 hours at a time in a specific location. After all that testing, there have been no bans, as it is virtually undetectable by the game. It is advised to not run the bot for long periods of time as this can seem as suspisious behavior that may lead to a ban. Use at your own risk.
