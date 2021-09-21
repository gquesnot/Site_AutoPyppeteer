const myFolderId = "FOLDER ID"
const mySecret = "SECRET"

function doGet(request) {
    var secret = request.parameters.secret
    if (secret == mySecret) {
        var type = request.parameters.type
        if (type == "insert_sheet") {
            return getSheet(request)
        } else if (type == "get_sheet") {
            return insertSheet(request)
        }
    }
    return ContentService.createTextOutput("badToken");


}


function getSheet(request) {
    var id = request.parameters.id;
    var sheetName = request.parameters.sheetName;
    var startR = request.parameters.startR;
    var endR = request.parameters.endR;
    var startC = request.parameters.startC;
    var endC = request.parameters.endC;
    var ssheet = SpreadsheetApp.openById(id);
    var sheet = ssheet.getSheetByName(sheetName);
    var dataOut = sheet.getSheetValues(startR, startC, endR, endC);
    return ContentService.createTextOutput(JSON.stringify(dataOut));
}

function insertSheet(request) {
    var myDatas = JSON.parse(request.parameters.datas);
    var startR = request.parameters.startR;
    var endR = request.parameters.endR;
    var startC = request.parameters.startC;
    var endC = request.parameters.endC;
    var spreedsheet = SpreadsheetApp.create("new spreadsheet");
    var sheet = spreedsheet.getSheets()[0];
    sheet.getRange(startR, startC, endR, endC).setValues(myDatas);
    var file = DriveApp.getFileById(spreedsheet.getId());
    var folder = DriveApp.getFolderById(myFolderId);
    var newFile = file.moveTo(folder);
    console.log(newFile.getUrl());
    return ContentService.createTextOutput(file.getUrl());
}
