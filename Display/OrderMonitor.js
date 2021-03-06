var filename = "order_list.csv";
var rowHeight = displayHeight * 0.09;
var columnWidth = displayWidth * 0.2;
var startX = displayWidth * 0.05;
var startY = displayHeight * 0.05;
var orders;
var columns;
var table;

function preload() {
    table = loadTable(filename, 'csv');
}


function setup() {
    createCanvas(displayWidth, displayHeight);
    //fullscreen(createCanvas(displayWidth, displayHeight));
    columns = table.getColumnCount();
    frameRate(5);
}


function draw() {
    background(220);
    showTable();
    updateTableData();
}


function updateTableData() {
    orders = table.getRowCount();
    table = loadTable(filename, 'csv', loadTable_cb, _loadTable_cb);
}

function loadTable_cb(t) {
    print("Table reload success.");
}

function _loadTable_cb(error) {
    print("ERROR: " + error);
}

function showTable() {
    let i = 0;
    let j = 0;
    showHeader(startX, startY, columnWidth, rowHeight);
    textSize(20);
    for (i = 0; i < orders; i++) {
        for (j = 0; j < columns; j++) {  
            text(table.getString(i, j),
                startX + (columnWidth * (j)),
                startY + (rowHeight * (i + 1)),
                rowHeight,
                columnWidth);
        }
    }
}

function showHeader(x, y, width, height) {
    textSize(30);
    text("Order Number", x, y, width, height);
    text("Name", x + width, y, width, height);
    text("Order", x + width * 2, y, width, height);
    text("Status", x + width * 3, y, width, height);
}
