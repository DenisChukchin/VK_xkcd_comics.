# VK xkcd comics. 
The script downloads comics pictures from the site [xkcd](https://xkcd.com) and publishes it on VK group wall.
## Prerequisites:
+ You will need to create a new group on [VK](https://vk.com).
+ You will need to create an app on [vk.developers](https://vk.com/dev)
+ You will need to get VK API token (_access_token_), follow the instructions [impicilt_flow_user](https://vk.com/dev/implicit_flow_user) 
## Installation.
Install Python3 latest version. Install PyCharm IDE, if you need it.
> To isolate the project, I'd recommend to use a virtual environment model. [vertualenv/venv](https://docs.python.org/3/library/venv.html).
## Preparing to run the script.
+ Create a virtualenv and activate it.
+ Then use pip (or pip3, there is a conflict with Python2) to install the dependencies (use the requirements.txt file):
```bash
% pip install -r requirements.txt
```
> For permanent set, create .env file and add variables:
```python
VK_TOKEN = "YOUR_VK_ACCESS_TOKEN"
GROUP_ID = "YOUR_GROUP_ID"
```
> If you don't want to set environment variables, then for a quick test run, export your private "VK_TOKEN" and "GROUP_ID" by this commands:
``` bash
% export VK_TOKEN="YOUR_VK_ACCESS_TOKEN"
% export GROUP_ID="YOUR_GROUP_ID"
```
## Run the script.
The script will download a picture from the site to your computer, upload and publish it on VK group wall, and finally, the script will delete the picture from your computer. Quick and simple.
Run the script by this command:
``` bash
% python3 main.py
```
## Project goals.
*The program was designed by a student from online web development courses for educational purposes [Devman](https://dvmn.org).*