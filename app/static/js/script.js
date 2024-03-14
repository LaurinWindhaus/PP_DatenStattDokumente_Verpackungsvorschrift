const document_id = document.getElementById('document_id').textContent.trim();
const imagesCount = document.getElementById("image_count").innerHTML;
const images = document.getElementById("images").innerHTML;

const imageContainer = document.getElementById('image_container');
JSON.parse(images).forEach(image => {
    loadImageToDocument(image.url, image.width, image.height);
});

const dragArea = document.getElementById('dragArea');
const fileInput = document.getElementById('fileInput');

document.addEventListener('DOMContentLoaded', function () {
    const toggleEditModeCheckbox = document.getElementById('toogle_edit_mode');
    if (toggleEditModeCheckbox) {
        toggleEditModeCheckbox.addEventListener('change', function () {
            if (this.checked) {
                enableAllFormFields();
            } else {
                disableAllFormFields();
            }
        });
    }
});

dragArea.addEventListener('click', () => fileInput.click());

function handleFilesEvent(event) {
    let files;
    if (event.type === "drop") {
        event.preventDefault();
        files = event.dataTransfer.files;
    } else {
        files = this.files;
    }
    if (files.length > 0) {
        const file = files[0];
        if (file.type.match('image.*')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const width = img.width;
                    const height = img.height;
                    const base64StringWithMimeType = e.target.result;
                    saveFileToStorage(base64StringWithMimeType, width, height);
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            alert("Please select an image file.");
        }
    }
}

fileInput.addEventListener('change', handleFilesEvent, false);
dragArea.addEventListener('drop', handleFilesEvent, false);

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dragArea.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});

function saveFileToStorage(base64StringWithMimeType, width, height) {
    fetch("/fileservice/file/upload", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            base64str: base64StringWithMimeType
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(`Error ${response.status}: ${errorData.message}`);
            });
        }
        return response.json();
    })
    .then(data => {
        saveUrlToDocument(data.url, width, height);
    })
    .catch((error) => {
        console.error('Error:', error);
        if (error.message.includes('Error')) {
            alert("Es ist ein Fehler beim speichern aufgetreten.");
        }
    });
}

function saveUrlToDocument(url, width, height) {
    fetch("/dsd/image/upload", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            document_id: document_id,
            url: url,
            width: width,
            height: height
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(`Error ${response.status}: ${errorData.message}`);
            });
        }
        return response.json();
    })
    .then(data => {
        loadImageToDocument(url, width, height);
    })
}

function loadImageToDocument(url, width, height) {
    subContainer = document.createElement("div");
    subContainer.id = url;
    subContainer.style.margin = "5px";
    deleteButton = document.createElement("button");
    deleteButton.classList = "btn btn-danger edit-mode";
    deleteButton.id = "delete_"+url;
    deleteButton.innerHTML = "Löschen";
    deleteButton.style.margin = "5px";
    deleteButton.onclick = function() {
        deleteImageFromDocument(url);
        document.getElementById(url)
        document.getElementById(url).remove();
        document.getElementById("delete_"+url).remove();
        document.getElementById("slider_"+url).remove();
    };
    slider = document.createElement("input");
    slider.type = "range";
    slider.min = "1";
    slider.max = "200";
    slider.value = "100";
    slider.classList = "edit-mode";
    slider.id = "slider_"+url;
    slider.style.margin = "5px";
    (function(url, width, height) {
        slider.oninput = function() {
            var imageWidth = width * this.value / 100;
            var imageHeight = height * this.value / 100;
            document.getElementById("image_" + url).style.width = imageWidth + "px";
            document.getElementById("image_" + url).style.height = imageHeight + "px"; // Maintain aspect ratio if desired
        };
    })(url, width, height);
    imageContainer.append(slider);
    imageContainer.append(deleteButton);
    image = document.createElement("div");
    image.id = "image_"+url;
    image.style.backgroundImage = "url('"+url+"')";
    image.style.backgroundSize = "contain";
    image.style.backgroundRepeat = "no-repeat";
    image.style.backgroundPosition = "center";
    image.style.width = width+"px"; // Set the width
    image.style.height = height+"px"; // Set the height
    subContainer.append(image);
    imageContainer.append(subContainer);
}

async function deleteImageFromDocument(url) {
    try {
        const response1 = await fetch("/dsd/image/delete", {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: document_id,
                image_url: url
            })
        });
        const data1 = await response1.json();
        if (!response1.ok) {
            throw new Error(`Error ${response1.status}: ${data1.message}`);
        }
        const response2 = await fetch("/fileservice/file/delete", {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: url.split('/').pop()
            })
        });
        const data2 = await response2.json();
        if (!response2.ok) {
            throw new Error(`Error ${response2.status}: ${data2.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Es ist ein Fehler beim Löschen aufgetreten.");
    }
}

function updateDocumentInputValues(document_id) {
    data = {};

    data['datum'] = document.getElementById('datum').value.trim();

    var elementValue = document.getElementById('aenderungsstand').value.trim();
    data['aenderungsstand'] = elementValue == '' ? "0" : (parseInt(elementValue, 10) + 1).toString();

    data['freigabe'] = document.getElementById('freigabe').value.trim();
    data['hpv'] = {};
    data['hpv']['hpv1'] = {};
    data['hpv']['hpv1']['komponente'] = document.getElementById('hpv1_komponente').value.trim();
    data['hpv']['hpv1']['anzahl'] = document.getElementById('hpv1_anzahl').value.trim();
    data['hpv']['hpv2'] = {};
    data['hpv']['hpv2']['komponente'] = document.getElementById('hpv2_komponente').value.trim();
    data['hpv']['hpv2']['anzahl'] = document.getElementById('hpv2_anzahl').value.trim();
    data['hpv']['hpv3'] = {};
    data['hpv']['hpv3']['komponente'] = document.getElementById('hpv3_komponente').value.trim();
    data['hpv']['hpv3']['anzahl'] = document.getElementById('hpv3_anzahl').value.trim();
    data['hpv']['hpv4'] = {};
    data['hpv']['hpv4']['komponente'] = document.getElementById('hpv4_komponente').value.trim();
    data['hpv']['hpv4']['anzahl'] = document.getElementById('hpv4_anzahl').value.trim();
    data['hpv']['hpv5'] = {};
    data['hpv']['hpv5']['komponente'] = document.getElementById('hpv5_komponente').value.trim();
    data['hpv']['hpv5']['anzahl'] = document.getElementById('hpv5_anzahl').value.trim();
    data['hpv']['hpv6'] = {};
    data['hpv']['hpv6']['komponente'] = document.getElementById('hpv6_komponente').value.trim();
    data['hpv']['hpv6']['anzahl'] = document.getElementById('hpv6_anzahl').value.trim();
    data['upv'] = {};
    data['upv']['upv1'] = {};
    data['upv']['upv1']['komponente'] = document.getElementById('upv1_komponente').value.trim();
    data['upv']['upv1']['anzahl'] = document.getElementById('upv1_anzahl').value.trim();
    data['upv']['upv2'] = {};
    data['upv']['upv2']['komponente'] = document.getElementById('upv2_komponente').value.trim();
    data['upv']['upv2']['anzahl'] = document.getElementById('upv2_anzahl').value.trim();
    data['upv']['upv3'] = {};
    data['upv']['upv3']['komponente'] = document.getElementById('upv3_komponente').value.trim();
    data['upv']['upv3']['anzahl'] = document.getElementById('upv3_anzahl').value.trim();
    data['upv']['upv4'] = {};
    data['upv']['upv4']['komponente'] = document.getElementById('upv4_komponente').value.trim();
    data['upv']['upv4']['anzahl'] = document.getElementById('upv4_anzahl').value.trim();
    data['upv']['upv5'] = {};
    data['upv']['upv5']['komponente'] = document.getElementById('upv5_komponente').value.trim();
    data['upv']['upv5']['anzahl'] = document.getElementById('upv5_anzahl').value.trim();
    data['upv']['upv6'] = {};
    data['upv']['upv6']['komponente'] = document.getElementById('upv6_komponente').value.trim();
    data['upv']['upv6']['anzahl'] = document.getElementById('upv6_anzahl').value.trim();
    data['anweisung'] = {};
    data['anweisung']['anweisung1'] = document.getElementById('anweisung1').value.trim();
    data['anweisung']['anweisung2'] = document.getElementById('anweisung2').value.trim();
    data['anweisung']['anweisung3'] = document.getElementById('anweisung3').value.trim();
    data['anweisung']['anweisung4'] = document.getElementById('anweisung4').value.trim();
    data['anweisung']['anweisung5'] = document.getElementById('anweisung5').value.trim();
    data['anweisung']['anweisung6'] = document.getElementById('anweisung6').value.trim();
    data['anweisung']['anweisung7'] = document.getElementById('anweisung7').value.trim();
    data['anweisung']['anweisung8'] = document.getElementById('anweisung8').value.trim();
    data['anweisung']['anweisung9'] = document.getElementById('anweisung9').value.trim();

    fetch("/dsd/document/update/"+document_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data : data
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(`Error ${response.status}: ${errorData.message}`);
            });
        }
        return response.json();
    })
    .catch((error) => {
        console.error('Error:', error);
        if (error.message.includes('Error')) {
            alert("Es ist ein Fehler beim speichern aufgetreten.");
        }
    });
}

function updateDocumentImageValues(document_id) {
    var image_properties = [];
    var images = document.getElementById('image_container').children;
    for (var i = 0; i < images.length; i++) {
        if (images[i].tagName === "DIV") {
            image_properties.push({
                "image_url": images[i].id,
                "width": images[i].querySelector('div').style.width,
                "height": images[i].querySelector('div').style.height
            });
        }    
    }
    console.log(image_properties);
    fetch("/dsd/image/update/"+document_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            images: image_properties 
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(`Error ${response.status}: ${errorData.message}`);
            });
        }
        redirectToMainPage();
        return response.json();
    })
    .catch((error) => {
        console.error('Error:', error);
        if (error.message.includes('Error')) {
            alert("Es ist ein Fehler beim speichern aufgetreten.");
        }
    });
}

function updateDocument(document_id) {
    updateDocumentInputValues(document_id);
    updateDocumentImageValues(document_id);
}

async function deleteDocument(document_id) {
    const imageDeletionPromises = JSON.parse(images).map(image => {
        return deleteImageFromDocument(image.url);
    });
    try {
        await Promise.all(imageDeletionPromises);
        const response = await fetch("/dsd/document/delete/" + document_id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Error ${response.status}: ${errorData.message}`);
        }
        const data = await response.json();
        console.log(data);
        redirectToMainPage();
    } catch (error) {
        console.error('Error:', error);
        alert("Es ist ein Fehler beim Löschen aufgetreten.");
    }
}

function redirectToMainPage() {
  window.location.href = 'https://ppmesktech.poeppelmann.com/KTECH/100_Verpackungsvorschrift/';
}

function disableAllFormFields() {
    var formFields = document.querySelectorAll('.value');

    formFields.forEach(function(field) {
        field.disabled = true;
        field.style.backgroundColor = 'white';
        field.style.border = 'none';
        field.style.outline = 'none';
    });

    var editModeItems = document.querySelectorAll('.edit-mode');
    editModeItems.forEach(function(item) {
        item.style.display = 'none';
    });
}

function enableAllFormFields() {
    var formFields = document.querySelectorAll('.value');

    formFields.forEach(function(field) {
        field.disabled = false;
        field.style.backgroundColor = '';
        field.style.border = '';
        field.style.outline = ''; 
    });

    var editModeItems = document.querySelectorAll('.edit-mode');
    editModeItems.forEach(function(item) {
        item.style.display = '';
    });
}

function pdfErstellen() {
    console.log("PDF erstellen");
}