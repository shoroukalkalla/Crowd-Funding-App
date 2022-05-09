const uploadedImages = [];
const images_container = document.querySelector(".images_container");
const uploadImage = document.querySelector(".project_images");
const deletedImages = [];
const Images = [];
uploadImage.addEventListener("change", (e) => previewImage(e));

window.addEventListener("load", (e) => {

    let split = window.location.href.split('/')
    if(split.slice(-1)[0] == "edit" )
    {
        
    let id=split.slice(-2,-1)[0]
    fetch(`http://127.0.0.1:8000/api/images?project_id=${id}`).then(response => {
        return response.json()
    }).then(data => {

        for (let img of data) {
            let imageName = img.image.split('/').pop();
            createImage(img.image,imageName, img.id);
        }
        
    });

}

    });

async function previewImage(e) {
    const files = [...e.target.files].map((file) => {
        const reader = new FileReader();
        return new Promise((resolve) => {
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(file);
        });
    });
    const res = await Promise.all(files);

    for (let i in res) {
        uploadedImages.push(e.target.files[i]);
        createImage(res[i], e.target.files[i].name);
    }
    uploadImage.value = "";
}

function createImage(imgSrc, imgName, id = null) {
    let div = document.createElement("div");
    div.innerHTML = `
    <button onClick = "removeImage(event)" class="btn position-absolute bg-transparent text-danger fw-bold fs-3  top-0 end-0">X</button>
`;
    let img = document.createElement("img");
    img.setAttribute("data-img_name", imgName);
    if(id)
    {
        img.setAttribute("data-img_id", id);
    }
    div.classList.add("m-2", "position-relative");
    img.src = imgSrc;
    div.appendChild(img);
    images_container.append(div);
}

function removeImage(event) {

    let img = event.target.nextElementSibling.dataset

    let imgName = img.img_name;
    let fileIndex = uploadedImages.findIndex((file) => file.name == imgName);
    uploadedImages.splice(fileIndex, 1);



    if(img.img_id)
    {
        deletedImages.push(img.img_id);
    }
    event.target.parentElement.remove();

}

/* ---------------------------------------- */
document.querySelector("form.projects").addEventListener("submit", (e) => {
    e.preventDefault();

    let imagesName = "";
    const formData = new FormData();
    for (let file of uploadedImages) {
        formData.append("images", file);
        imagesName += ` ${file.name}`;
    }

    console.log(imagesName.trim());
    imagesName = imagesName.trim();

    let images = createDataInput(imagesName,"images")
    let deletedIds = createDataInput(deletedImages,"ids")

    e.target.append(images);
    e.target.append(deletedIds);

    fetch(`http://127.0.0.1:8000/upload_images/`, {
        method: "POST",
        body: formData,
        mode: "no-cors",
        headers: {
            Accept: "application/json",
        },
    }).then((res) => {
        // window.location.href = "/projects";
    });
    // .then((data) => console.log(data))
    // .catch((err) => console.log(err));
});

function createDataInput(value,name)
{
    let input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("value", value);
    input.setAttribute("name", name);
    input.classList.add("d-none");

    return input;
}