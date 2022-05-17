console.log("Hello, from project folder");



  
const projects = document.querySelectorAll(".projects .project");
projects.forEach((project) =>
    project.addEventListener(
        "click",
        (e) =>
            (window.location.href = `${window.location.href
                .split("/")
                .slice(0, 3)
                .join("/")}/projects/${e.currentTarget.dataset.id}`)
    )
);
