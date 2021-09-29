
let myFolderId = "folder_ID"
let mySecret = "secret_KEY"

function doGet(request) {

    let secret = request.parameters.secret
    if (secret == mySecret) {
        let type = request.parameters.type
        if (type == "insert_sheet") {
            return getSheet(request)
        } else if (type == "get_sheet") {
            return insertSheet(request)
        }
        else if (type == "create_slide"){
            return createSlide(request)
        }
        else if (type == "create_doc"){
            return createDoc(request)
        }
    }
    return ContentService.createTextOutput("badToken");


}


function createDoc(request){
      let templateId = request.parameters.templateId
    let myDatas = JSON.parse(request.parameters.datas);
    let file = DriveApp.getFileById(templateId)
    let folder = DriveApp.getFolderById(myFolderId);
    let file2 = file.makeCopy()
    file2.moveTo(folder)
    let doc = DocumentApp.openById(file2.getId())
    let docBody= doc.getBody()
    for (const [key, value] of Object.entries(myDatas)) {
      docBody.replaceText("{{"+key+"}}",value)

    }
    let url = doc.getUrl()
    doc.saveAndClose()
    return ContentService.createTextOutput(JSON.stringify(url));
}

function createSlide(request) {
    let templateId = request.parameters.templateId
    let myDatas = JSON.parse(request.parameters.datas);
    let file = DriveApp.getFileById(templateId)
    let folder = DriveApp.getFolderById(myFolderId);
    let file2 = file.makeCopy()
    file2.moveTo(folder)
    let slides = SlidesApp.openById(file2.getId())
    for (const [key, value] of Object.entries(myDatas)) {
      slides.replaceAllText("{{"+key+"}}",value)
    }
    let url = slides.getUrl()
    slides.saveAndClose()
    return ContentService.createTextOutput(JSON.stringify(url));
}

function getSheet(request) {
    let id = request.parameters.id;
    let sheetName = request.parameters.sheetName;
    let startR = request.parameters.startR;
    let endR = request.parameters.endR;
    let startC = request.parameters.startC;
    let endC = request.parameters.endC;
    let ssheet = SpreadsheetApp.openById(id);
    let sheet = ssheet.getSheetByName(sheetName);
    let dataOut = sheet.getSheetValues(startR, startC, endR, endC);
    return ContentService.createTextOutput(JSON.stringify(dataOut));
}

function insertSheet(request) {
    let myDatas = JSON.parse(request.parameters.datas);
    let startR = request.parameters.startR;
    let endR = request.parameters.endR;
    let startC = request.parameters.startC;
    let endC = request.parameters.endC;
    let spreedsheet = SpreadsheetApp.create("new spreadsheet");
    let sheet = spreedsheet.getSheets()[0];
    sheet.getRange(startR, startC, endR, endC).setValues(myDatas);
    let file = DriveApp.getFileById(spreedsheet.getId());
    let folder = DriveApp.getFolderById(myFolderId);
    let newFile = file.moveTo(folder);
    console.log(newFile.getUrl());
    return ContentService.createTextOutput(file.getUrl());
}