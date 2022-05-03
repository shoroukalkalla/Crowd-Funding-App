const input = document.querySelector(".profile_avatar input");
const preview = document.querySelector(".profile_avatar .avatar_box img");

console.log(input);
console.log(preview);

input.addEventListener("change", (e) => {
    console.log("render script");
    let reader = new FileReader();
    reader.onload = function () {
        if (reader.readyState == 2) {
            preview.src = reader.result;
        }
    };
    reader.readAsDataURL(e.target.files[0]);
});
