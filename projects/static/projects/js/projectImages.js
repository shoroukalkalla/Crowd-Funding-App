const uploadedImages = [];
const images_container = document.querySelector(".images_container");
const uploadImage = document.querySelector(".project_images");

uploadImage.addEventListener("change", (e) => previewImage(e));

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

function createImage(imgSrc, imgName) {
    let div = document.createElement("div");
    div.innerHTML = `
    <button onClick = "removeImage(event)" class="btn position-absolute bg-transparent text-danger fw-bold fs-3  top-0 end-0">X</button>
`;
    let img = document.createElement("img");
    img.setAttribute("data-img_name", imgName);

    div.classList.add("m-2", "position-relative");
    img.src = imgSrc;
    div.appendChild(img);
    images_container.append(div);
}

function removeImage(event) {
    let imgName = event.target.nextElementSibling.dataset.img_name;
    let fileIndex = uploadedImages.findIndex((file) => file.name == imgName);
    uploadedImages.splice(fileIndex, 1);
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

    let input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("value", imagesName);
    input.setAttribute("name", "images");
    input.classList.add("d-none");

    e.target.append(input);

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
