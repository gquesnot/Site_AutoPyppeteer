# GOOGLE API INSTALLATION

- create a folder in your google drive , change permissions to public if you want people to be able to access it 
- copy content of google_script_base.js to a new project in https://script.google.com/
- create a secret token (20-30 random chararcter), store it in your google script as  const mySecret and in AAPyppeteer/util/token.json as secret
- copy the id of your folder in your google script as myFolderId
- save the script , deploy it as web app for all and save the url to AAPyppeteer/util/token.json
