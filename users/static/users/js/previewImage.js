const input = document.querySelector(".profile_avatar div input");
const preview = document.querySelector(".profile_avatar .avatar_box img");

input.addEventListener("change", (e) => {
    let reader = new FileReader();
    reader.onload = function () {
        if (reader.readyState == 2) {
            preview.src = reader.result;
        }
    };
    reader.readAsDataURL(e.target.files[0]);
});
