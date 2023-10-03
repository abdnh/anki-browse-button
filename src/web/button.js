class BrowseButton extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: "open" });
        const anchor = document.createElement("a");
        anchor.href = 'javascript:pycmd("browse_button")';
        anchor.style.display = "block";
        anchor.style.width = "32px";
        anchor.append(...this.childNodes);
        anchor.querySelectorAll("svg").forEach((el) => (el.part = "icon"));
        anchor.querySelectorAll("path").forEach((el) => (el.part = "path"));

        shadow.appendChild(anchor);
    }
}

customElements.define("browse-button", BrowseButton);
