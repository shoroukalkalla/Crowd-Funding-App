console.log("Hello, from project folder");

const projects = document.querySelectorAll(".projects .project");
projects.forEach((project) =>
    project.addEventListener(
        "click",
        (e) => (window.location.href = `${e.currentTarget.dataset.id}`)
    )
);
