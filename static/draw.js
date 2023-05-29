var isDrawing = false;
window.addEventListener('load', function () {
    const canvasContainer = document.getElementById('canvas-container');
    const canvas = document.getElementById('myCanvas');
    const penSize = document.getElementById("mySlider");
    const colorSelector = document.getElementById("myColor");
    var context = canvas.getContext("2d");


    function resizeCanvas() {
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const screenWidth = window.innerWidth;
        var padding = screenWidth * 0.05;
        const canvasSizeW = screenWidth - 2 * padding;
        const screenHeight = window.innerHeight;
        var padding = screenHeight * 0.25;
        const canvasSizeH = screenHeight - 2 * padding;
        const canvasSize = Math.min(canvasSizeH, canvasSizeW);

        canvas.width = canvasSize;
        canvas.height = canvasSize;

        canvasContainer.style.width = canvasSize + 'px';
        canvasContainer.style.height = canvasSize + 'px';

        context.putImageData(imageData, 0, 0);

    }

    // Initial canvas resize
    resizeCanvas();

    // Resize canvas on window resize
    window.addEventListener('resize', resizeCanvas);


    // Get the canvas element
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

// Function to draw on the canvas
    function draw(e) {
        if (!isDrawing) return;
        context.lineWidth = penSize.value;
        context.lineCap = 'round';
        context.strokeStyle = colorSelector.value;

        context.beginPath();
        context.moveTo(lastX, lastY);
        context.lineTo(e.offsetX, e.offsetY);
        context.stroke();

        lastX = e.offsetX;
        lastY = e.offsetY;
    }

// Event listeners
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        lastX = e.offsetX;
        lastY = e.offsetY;
    });

    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', () => (isDrawing = false));
    canvas.addEventListener('mouseout', () => (isDrawing = false));

    window.addEventListener('resize', () => {
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;
        context.putImageData(imageData, 0, 0);
    });
    penSize.addEventListener('input', () => {
        document.getElementById("penSizeNum").innerText = penSize.value;
        ;
    });
    document.getElementById("penSizeNum").innerText = penSize.value;
    ;

});