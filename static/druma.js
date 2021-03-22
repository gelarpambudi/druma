//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
span = dropArea.querySelector("span");
icon = dropArea.querySelector(".icon");
let file; //this is a global variable and we'll use it inside multiple functions

button.onclick = ()=>{
  input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile(){
  let fileType = file.type; //getting selected file type
  let fileName = file.name;
  let validExtensions = ["image/jpeg", "image/jpg", "image/png", "image/tiff"]; //adding some valid image extensions in array
  if(validExtensions.includes(fileType)){ //if user selected file is an image file
    dropArea.removeChild(dragText);
    dropArea.removeChild(button);
    dropArea.removeChild(icon);
    dropArea.removeChild(span);
    let fileReader = new FileReader(); //creating new FileReader object
    if ((fileType == validExtensions[0]) || (fileType == validExtensions[1]) || (fileType == validExtensions[2])) {
      fileReader.onload = ()=>{
        let fileURL = fileReader.result; //passing user file source in fileURL variable
        let imgTag = document.createElement("img");
        imgTag.src = `${fileURL}`; //creating an img tag and passing user selected file source inside src attribute
        dropArea.innerHTML += imgTag;
      }
      fileReader.readAsDataURL(file);
    }else if (fileType == validExtensions[3]){
      fileReader.onload = ()=>{
        let imgName = document.createElement("P");
        imgName.innerText = `${fileName}`; 
        dropArea.innerHTML += imgName;
      }
      fileReader.readAsDataURL(file);
    }
    
  }else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}