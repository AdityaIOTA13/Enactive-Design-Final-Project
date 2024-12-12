require('p5')

let img;

function preload() {
    window.electronAPI.loadImage('../example.png').then((dataUrl) => {
        img = loadImage(dataUrl);
    });
}

function setup() {
    createCanvas(800, 600);
}

function draw() {
    background(220);
    if (img) {
        image(img, 0, 0);
    }
    if (mouseIsPressed) {
        line(mouseX, mouseY, pmouseX, pmouseY);
    }
}