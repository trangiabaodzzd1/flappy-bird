import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird",
    page_icon="🐦",
    layout="centered"
)

st.title("🐦 Flappy Bird")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: #87CEEB;
    overflow: hidden;
    font-family: Arial;
    text-align: center;
}

canvas {
    background: linear-gradient(#70c5ce, #dff6ff);
    border: 4px solid #333;
    border-radius: 10px;
    max-width: 100%;
}

#info {
    font-size: 22px;
    font-weight: bold;
    margin: 8px;
}

button {
    background: #ffca28;
    border: none;
    padding: 10px 25px;
    border-radius: 8px;
    font-size: 18px;
    cursor: pointer;
    font-weight: bold;
}

button:hover {
    background: #ffc107;
}
</style>
</head>

<body>

<div id="info">
    Điểm: <span id="score">0</span>
</div>

<canvas id="game" width="400" height="600"></canvas>

<br><br>

<button onclick="restartGame()">🔄 Chơi lại</button>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let bird;
let pipes;
let score;
let gameOver;
let started;

const gravity = 0.45;
const jump = -7.5;
const pipeWidth = 65;
const pipeGap = 160;
const pipeSpeed = 2.5;

function startGame() {

    bird = {
        x: 80,
        y: 300,
        radius: 16,
        velocity: 0
    };

    pipes = [];
    score = 0;
    gameOver = false;
    started = true;

    document.getElementById("score").innerText = score;

    createPipe();
}

function createPipe() {

    const minTop = 60;
    const maxTop = canvas.height - pipeGap - 80;

    const topHeight =
        Math.random() * (maxTop - minTop) + minTop;

    pipes.push({
        x: canvas.width,
        top: topHeight,
        passed: false
    });
}

function flap() {

    if (gameOver) {
        restartGame();
        return;
    }

    bird.velocity = jump;
}

document.addEventListener("keydown", function(event) {

    if (
        event.code === "Space" ||
        event.code === "ArrowUp"
    ) {
        event.preventDefault();
        flap();
    }
});

canvas.addEventListener("mousedown", function() {
    flap();
});

canvas.addEventListener("touchstart", function() {
    flap();
});

function update() {

    if (!started || gameOver) {
        return;
    }

    bird.velocity += gravity;
    bird.y += bird.velocity;

    for (let pipe of pipes) {

        pipe.x -= pipeSpeed;

        if (
            !pipe.passed &&
            pipe.x + pipeWidth < bird.x
        ) {

            pipe.passed = true;
            score++;

            document.getElementById("score").innerText = score;
        }
    }

    if (
        pipes.length === 0 ||
        pipes[pipes.length - 1].x < 220
    ) {
        createPipe();
    }

    if (pipes[0].x + pipeWidth < 0) {
        pipes.shift();
    }

    if (
        bird.y - bird.radius < 0 ||
        bird.y + bird.radius > canvas.height
    ) {
        endGame();
    }

    for (let pipe of pipes) {

        const hitX =
            bird.x + bird.radius > pipe.x &&
            bird.x - bird.radius < pipe.x + pipeWidth;

        const hitTop =
            bird.y - bird.radius < pipe.top;

        const bottomY =
            pipe.top + pipeGap;

        const hitBottom =
            bird.y + bird.radius > bottomY;

        if (hitX && (hitTop || hitBottom)) {
            endGame();
        }
    }
}

function endGame() {
    gameOver = true;
}

function drawBird() {

    ctx.fillStyle = "#FFD93D";

    ctx.beginPath();

    ctx.arc(
        bird.x,
        bird.y,
        bird.radius,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle = "#F4A62A";

    ctx.beginPath();

    ctx.ellipse(
        bird.x - 5,
        bird.y + 5,
        9,
        5,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle = "white";

    ctx.beginPath();

    ctx.arc(
        bird.x + 6,
        bird.y - 6,
        5,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle = "black";

    ctx.beginPath();

    ctx.arc(
        bird.x + 8,
        bird.y - 6,
        2,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle = "#FF7043";

    ctx.beginPath();

    ctx.moveTo(bird.x + 15, bird.y);
    ctx.lineTo(bird.x + 27, bird.y + 5);
    ctx.lineTo(bird.x + 15, bird.y + 9);

    ctx.fill();
}

function drawPipe(pipe) {

    ctx.fillStyle = "#42B72A";

    ctx.fillRect(
        pipe.x,
        0,
        pipeWidth,
        pipe.top
    );

    ctx.fillStyle = "#31951F";

    ctx.fillRect(
        pipe.x - 5,
        pipe.top - 20,
        pipeWidth + 10,
        20
    );

    const bottomY = pipe.top + pipeGap;

    ctx.fillStyle = "#42B72A";

    ctx.fillRect(
        pipe.x,
        bottomY,
        pipeWidth,
        canvas.height - bottomY
    );

    ctx.fillStyle = "#31951F";

    ctx.fillRect(
        pipe.x - 5,
        bottomY,
        pipeWidth + 10,
        20
    );
}

function draw() {

    ctx.fillStyle = "#70C5CE";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    ctx.fillStyle = "rgba(255,255,255,0.8)";

    ctx.beginPath();

    ctx.arc(70, 100, 25, 0, Math.PI * 2);
    ctx.arc(100, 100, 35, 0, Math.PI * 2);
    ctx.arc(135, 100, 25, 0, Math.PI * 2);

    ctx.fill();

    for (let pipe of pipes) {
        drawPipe(pipe);
    }

    drawBird();

    if (!started) {

        ctx.fillStyle = "rgba(0,0,0,0.45)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle = "white";

        ctx.font = "bold 30px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "🐦 FLAPPY BIRD",
            canvas.width / 2,
            250
        );

        ctx.font = "20px Arial";

        ctx.fillText(
            "Nhấn SPACE hoặc CLICK",
            canvas.width / 2,
            300
        );

        ctx.fillText(
            "để bắt đầu",
            canvas.width / 2,
            330
        );
    }

    if (gameOver) {

        ctx.fillStyle = "rgba(0,0,0,0.55)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle = "white";

        ctx.font = "bold 40px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "GAME OVER",
            canvas.width / 2,
            260
        );

        ctx.font = "24px Arial";

        ctx.fillText(
            "Điểm: " + score,
            canvas.width / 2,
            310
        );

        ctx.font = "18px Arial";

        ctx.fillText(
            "Click hoặc SPACE để chơi lại",
            canvas.width / 2,
            350
        );
    }
}

function gameLoop() {

    update();
    draw();

    requestAnimationFrame(gameLoop);
}

startGame();

started = false;

gameLoop();

function restartGame() {
    startGame();
}

</script>

</body>
</html>
"""

components.html(
    game,
    height=720,
    scrolling=False
)
