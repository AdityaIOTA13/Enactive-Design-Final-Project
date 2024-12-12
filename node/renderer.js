require('p5')
const fs = require("fs");
const { exec } = require('child_process');
const OpenAI = require("openai");


let img;
let currentColor = "#00b624"
let drawing = [];
let currentPath = [];
let canvas = null;
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    dangerouslyAllowBrowser: true
});
let lastOpenSCADcode = ""
let loading = false


function preload() {
}

function loadFSImage(imagePath) {
    const image = fs.readFileSync(imagePath).toString('base64')
    img = loadImage(`data:image/png;base64,${image}`)
}

function setup() {
    canvas = createCanvas(window.innerWidth-20, window.innerHeight-20);
    background(255);

    const button = createButton('Convert Sketch');
    button.position(10, 10);
    button.mousePressed(async () => {
        lastOpenSCADcode = await generateOpenScadCode(lastOpenSCADcode);
        renderOpenScad(lastOpenSCADcode);
    });

    const buttonRed = createButton('Red');
    buttonRed.position(130, 10);
    buttonRed.mousePressed(() => {
        currentColor = "#f80000";
    });

    const buttonGreen = createButton('Green');
    buttonGreen.position(190, 10);
    buttonGreen.mousePressed(() => {
        currentColor = "#00b624";
    });

    const buttonClear = createButton('Clear');
    buttonClear.position(250, 10);
    buttonClear.mousePressed(() => {
        drawing = [];
        img = null;
        lastOpenSCADcode = "";
    });
}

function windowResized() {
    resizeCanvas(window.innerWidth-20, window.innerHeight-20);
    background(255);
}

function draw() {
    background(255);
    if (img) {
        image(img, 0, 0, width, height);
    }

    noFill();
    stroke(0);
    strokeWeight(2);

    for (let i = 0; i < drawing.length; i++) {
        const path = drawing[i];
        stroke(path.color);
        beginShape();
        for (let j = 0; j < path.points.length; j++) {
            vertex(path.points[j].x, path.points[j].y);
        }
        endShape();
    }

    if (loading) {
        drawSpinningWheel();
    }

    if (mouseIsPressed) {
        const point = {
            x: mouseX,
            y: mouseY
        };
        currentPath.points.push(point);
    }
}

function drawSpinningWheel() {
    push();
    translate(width / 2, height / 2);
    rotate(frameCount / 10.0);
    strokeWeight(4);
    stroke(0);
    noFill();
    for (let i = 0; i < 10; i++) {
        line(0, 0, 30, 0);
        rotate(PI / 5);
    }
    pop();
}

function mousePressed() {
    currentPath = { color: currentColor, points: [] };
    drawing.push(currentPath);
}

async function keyPressed() {

}

function renderOpenScad(openscadCode) {
    const openscadFile = 'output.scad';

    fs.writeFileSync(openscadFile, openscadCode, 'utf8');

    const outputFile = 'output.png';

    exec(`openscad -o ${outputFile} ${openscadFile} --autocenter --viewall`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        console.log(`stderr: ${stderr}`);
        console.log(`Rendering successful: ${outputFile}`);
        loadFSImage(outputFile)
        loading = false
        currentPath = [];
        drawing = [];
    });
}


async function generateOpenScadCode(prevCode) {
    const data = canvas.elt.toDataURL()
    loading = true;

    const chatCompletion = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
            { role: "system", content: "You are a system that describe the shapes in this image using the OpenSCAD language. Return only the OpenSCAD code, with no other text or characters before or after. The provided image is a rendered image with lines sketched on top. Shapes sketched in Green should be added to the geometry. Shapes sketched in Red should be subtracted from the geometry. Return OpenSCAD code for a new model with the modifications described in the sketches. Use boolean operations to construct the shape out of primitive shapes. Keep in mind it may require many boolean operations. " },
            {role: "user", content: [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data,
                    }
                },
                {
                    "type": "text",
                    "text": prevCode
                },
                    {
                    "type": "text",
                    "text": "return only the code. Do not return any other text before or after. The code must be different from the code provided to you."
                },
            ],
        }],
    });

    return chatCompletion.choices[0].message.content.replaceAll("```openscad", "").replaceAll("```scss", "").replaceAll("```scad", "").replaceAll("```", "");
}