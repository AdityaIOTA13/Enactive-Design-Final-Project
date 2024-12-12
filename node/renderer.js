require('p5')
const fs = require("fs");
const { exec } = require('child_process');
const OpenAI = require("openai");


let img;
let drawing = [];
let currentPath = [];
let canvas = null;
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    dangerouslyAllowBrowser: true
});
let lastOpenSCADcode = ""


function preload() {
}

function loadFSImage(imagePath) {
    const image = fs.readFileSync(imagePath).toString('base64')
    img = loadImage(`data:image/png;base64,${image}`)
}

function setup() {
    canvas = createCanvas(window.innerWidth, window.innerHeight);
    background(255);
}

function draw() {
    background(255);
    if (img) {
        image(img, 0, 0);
    }

    noFill();
    stroke(0);
    strokeWeight(2);

    for (let i = 0; i < drawing.length; i++) {
        const path = drawing[i];
        beginShape();
        for (let j = 0; j < path.length; j++) {
            vertex(path[j].x, path[j].y);
        }
        endShape();
    }

    if (mouseIsPressed) {
        const point = {
            x: mouseX,
            y: mouseY
        };
        currentPath.push(point);
    }
}

function mousePressed() {
    currentPath = [];
    drawing.push(currentPath);
}

async function keyPressed() {
    if (keyCode === ENTER) {
        lastOpenSCADcode = await generateOpenScadCode(lastOpenSCADcode);
        renderOpenScad(lastOpenSCADcode);
    }
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
    });
}

async function generateOpenScadCode(prevCode) {
    const chatCompletion = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
            { role: "system", content: "You are a system that describe the shapes in this image using the OpenSCAD language. Return only the code, with no other text or characters before or after.  The sketched portion is to be added. The rendered portion is defined by the attached OpenSCAD code. Use boolean operations to construct the shape out of primitive shapes. Keep in mind it may require many boolean operations. " },
            {role: "user", content: [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": canvas.elt.toDataURL(),
                    }
                },
                {
                    "type": "text",
                    "text": prevCode
                },
            ],
        }],
    });

    return chatCompletion.choices[0].message.content.replaceAll("```openscad", "").replaceAll("```", "");
}