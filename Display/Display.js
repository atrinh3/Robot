var filename = "order_list.csv";
var orders = 0;
var columns = 0;
var table;

function preload() {
    table = loadTable(filename, 'csv');
}


function setup() {
    createCanvas(displayWidth, displayHeight);
    //fullscreen(createCanvas(displayWidth, displayHeight));
    columns = table.getColumnCount();
}


function draw() {
    background(220);
    updateTableData();
    showTable();
}


function updateTableData() {
	loadTable(filename, 'csv', loadTable_cb, _loadTable_cb);
    orders = table.getRowCount();
}

function loadTable_cb(table) {
    print("Table reload success.");
}

function _loadTable_cb(error) {
    print(error);
}

function showTable() {
    let rowHeight = displayHeight * 0.09;
    let columnWidth = displayWidth * 0.2;
    let startX = displayWidth * 0.05;
    let startY = displayHeight * 0.05;
    let i = 0;
    let j = 0;
    orders = table.getRowCount();
    columns = table.getColumnCount();
    print(columns);
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
