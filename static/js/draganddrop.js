dropContainer.ondragover = dropContainer.ondragenter = function (evt) {
    evt.preventDefault();
};

dropContainer.ondrop = function (evt) {
    // pretty simple -- but not for IE :(
    fileInput.files = evt.dataTransfer.files;
    evt.preventDefault();
    showUploaded();
};

function showUploaded() {
    if (uploadstuff.style.display == "none") {
        fileInput.value = null;
        uploadstuff.style.display = "block";
        uploadedstuff.style.display = "none";
    } else {
        uploadstuff.style.display = "none";
        uploadedstuff.style.display = "block";
    }
}

document.getElementById("fileInput").onchange = function () {
    showUploaded();
};

dropContainer2.ondragover = dropContainer2.ondragenter = function (evt) {
    evt.preventDefault();
};

dropContainer2.ondrop = function (evt) {
    // pretty simple -- but not for IE :(
    fileInput2.files = evt.dataTransfer.files;
    evt.preventDefault();
    showUploaded2();
};

function showUploaded2() {
    if (uploadstuff2.style.display == "none") {
        fileInput2.value = null;
        uploadstuff2.style.display = "block";
        uploadedstuff2.style.display = "none";
    } else {
        uploadstuff2.style.display = "none";
        uploadedstuff2.style.display = "block";
    }
}

document.getElementById("fileInput2").onchange = function () {
    showUploaded2();
};