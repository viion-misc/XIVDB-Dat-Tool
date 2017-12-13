## This tool is dead, no development is being done it.

Please use: https://github.com/ufx/SaintCoinach


---

---

# XIVDB Data Extraction Tool

This is not really in development anymore. I am replacing it all at some point with an improved version but with far better tools out there. I would like to release this for research purposes. It is not built by me, so I may not be able to answer everything, head to https://github.com/viion/XIV-Datamining for better research/discussions.

---

# How to use

- Make sure you have Python 3+
- Copy `config.cfg.dist` to `config.cfg`
- Edit `config.cfg` and add your game path`
- Open Windows Command Prompt/Terminal in the same location as `xivdmcli.py`
- Run one of the commands below, eg `python xivdmcli.py extract exd` to export all EXD


---

**Last Tested and Verified**
- Patch 3.0+
- Nov 2015
- Sound extract will not work for 3.0 music
- Model extract will not work
- Certain bites do not extract in csvs

**Cache**
- To reduce searching, the application will cache icon and map tile paths, when a new patch is
out you will need to reset this by going into the cache folder and deleting the gz files.

**Requirements**
- Python 3.4

**Commands**
- python xivdmcli.py extract -h

- python xivdmcli.py extract exd
- python xivdmcli.py extract exh
- python xivdmcli.py extract view
- python xivdmcli.py extract music
- python xivdmcli.py extract folder -n ui/uld/
- python xivdmcli.py extract gen -n icons
- python xivdmcli.py extract gen -n maps_icons
- python xivdmcli.py extract gen -n models
