import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ComfyUI-SaveAs",
    async setupExtension() {
        // This function will be called when the extension is loaded
    },
    async nodeCreated(node) {
        if (node.comfyClass === "ComfyUISaveAs") {
            node.addWidget("preview", "preview", "", (value) => {
                updatePreview(node, value);
            });
        }
    },
});

function updatePreview(node, previewUrl) {
    const previewElement = node.widgets.find(w => w.name === "preview");
    if (!previewElement) return;

    const container = document.createElement('div');
    container.style.maxWidth = '200px';
    container.style.maxHeight = '200px';
    container.style.overflow = 'hidden';

    if (previewUrl.startsWith('data:video')) {
        const video = document.createElement('video');
        video.src = previewUrl;
        video.controls = true;
        video.style.width = '100%';
        container.appendChild(video);
    } else {
        const img = document.createElement('img');
        img.src = previewUrl;
        img.style.width = '100%';
        container.appendChild(img);
    }

    previewElement.element.innerHTML = '';
    previewElement.element.appendChild(container);
}
