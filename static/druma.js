const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
span = dropArea.querySelector("span");
icon = dropArea.querySelector(".icon");
input = document.querySelector("input");
let file;
let form; 

button.onclick = ()=>{
  input.click(); 
}

input.addEventListener("change", function(){
  file = this.files[0];
  dropArea.classList.add("active");
  showFile();
});


dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});


dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});


dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); 
  file = event.dataTransfer.files[0];
  showFile(); 
});

function getFormData(file){
  var formData = new FormData(document.querySelector('form'));
  formData.set("files", file, file.name);
  return formData
}

function upload(){
  $('#loading').show();
  var form = getFormData(file);
  //document.querySelector(".input_form").closest('.input_form').remove();
  //document.querySelector(".input_file").closest('.input_file').remove();
  fetch('/predict', {method: "POST", body: form});
  console.log("Request sent")
}



function showFile(){
  let fileType = file.type; 
  let fileName = file.name;
  let validExtensions = ["image/jpeg", "image/jpg", "image/png", "image/tiff"]; //adding some valid image extensions in array

  if(validExtensions.includes(fileType)){ //if user selected file is an image file
    span.style.visibility = "hidden";
    button.style.visibility = "hidden";
    icon.style.visibility = "hidden";
    let fileReader = new FileReader(); //creating new FileReader object

    if ((fileType == validExtensions[0]) || (fileType == validExtensions[1]) || (fileType == validExtensions[2])) {
      fileReader.onload = ()=>{
        let fileURL = fileReader.result; 
        let imgTag = `<img src="${fileURL}" alt="">`; 
        dropArea.innerHTML = imgTag;
      }
      fileReader.readAsDataURL(file);
    }else if (fileType == validExtensions[3]){
      fileReader.onload = ()=>{
        let imgName= `<p>${fileName}</p>`; 
        dropArea.innerHTML = imgName;
      }
      fileReader.readAsDataURL(file);
    }

  }else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}