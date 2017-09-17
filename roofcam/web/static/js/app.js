const $ = document.querySelector.bind(document);

const snapshotEl = $("#snapshot");
const prevImgEl = $("#prevImg");
const nextImgEl = $("#nextImg");
const keyWEl = $("#key-w");
const keyDEl = $("#key-d");
const keyNEl = $("#key-n");

const snapshotDateEls = document.querySelectorAll(".snapshot-date");

/* DOM event handlers */

document.onkeydown = function (evt) {
    evt = evt || window.event;
    if (evt.keyCode == 37) {
        prevNextHandler("prev" /* <- */)();
    } else if (evt.keyCode == 39) {
        prevNextHandler("next" /* -> */)();
    } else if (evt.keyCode == 87 /* W */) {
        classifyCurrentSnapshot("WET");
    } else if (evt.keyCode == 68 /* D */) {
        classifyCurrentSnapshot("DRY");
    } else if (evt.keyCode == 78 /* N */) {
        classifyCurrentSnapshot("NIGHT");
    }
};

keyWEl.onclick = function () {
    classifyCurrentSnapshot("WET");
};

keyDEl.onclick = function () {
    classifyCurrentSnapshot("DRY");
};

keyNEl.onclick = function () {
    classifyCurrentSnapshot("NIGHT");
};

for (i = 0; i < snapshotDateEls.length; i++) {
    snapshotDateEls[i].onclick = specificImageHandler(snapshotDateEls[i].dataset.snapshot);
}

prevImgEl.onclick = prevNextHandler("prev");
nextImgEl.onclick = prevNextHandler("next");


function prevNextHandler(direction) {
    return function () {
        const snapshot = snapshotEl.src.split("/").pop();
        const url = "/" + direction + "/" + snapshot;
        loadSnapshot(url);
        return false;
    }
};

function specificImageHandler(snapshotDate) {
    return function () {
        console.log("/snapshotdata/" + snapshotDate);
        loadSnapshot("/snapshotdata/" + snapshotDate);
        return false;
    };
};


/* Back-end interaction */


function classifyCurrentSnapshot(clazz) {
    const snapshot = snapshotEl.src.split("/").pop();
    console.log(snapshot, "=>", clazz);
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        var data = JSON.parse(this.responseText);
        $("#predictedClass").innerHTML = data.prediction;
        $("#targetClass").innerHTML = data.target;
    });
    oReq.open("POST", "/classify/" + snapshot, true);
    oReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    oReq.send("class=" + clazz);

};

function loadSnapshot(url) {
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        var data = JSON.parse(this.responseText);
        $("#snapshot-name").innerHTML = data.snapshot;
        snapshotEl.src = snapshotEl.src = "snapshot/" + data.snapshot;
        $("#predictedClass").innerHTML = data.prediction;
        $("#targetClass").innerHTML = data.target;

    });
    oReq.open("GET", url);
    oReq.send();

}

