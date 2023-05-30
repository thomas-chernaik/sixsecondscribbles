var isDrawing = false;
window.addEventListener('load', function () {
    const canvasContainer = document.getElementById('canvas-container');
    const canvas = document.getElementById('myCanvas');
    const penSize = document.getElementById("mySlider");
    const colorSelector = document.getElementById("myColor");
    var context = canvas.getContext("2d");
    //initialise the canvas with a white background
    context.fillStyle = "white";
    context.fillRect(0, 0, 100000, 100000);


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

        //fill the canvas with white where the image data doesn't reach
        context.fillStyle = "white";
        context.fillRect(0, 0, 100000, 100000);
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


function uploadCanvas() {
    //get the canvas as a png to upload
    var canvas = document.getElementById("myCanvas");
    var dataURL = canvas.toDataURL("image/png");
    // Create an image element
    const image = new Image();

// Set the source of the image as the captured Data URL
    image.src = dataURL;

    //send the png to the server, and the card as form data from the element card-name
    var cardName = document.getElementById("card-name").value;

    // Send the image to the server
    fetch('/uploadImage', {
        method: 'POST',
        body: JSON.stringify({image: dataURL}),
        headers: {
            'Content-Type': 'application/json',
            'card-name': cardName
        }
    })
        .then(response => {
            // Handle the server response
            console.log('Image uploaded successfully');
        })
        .catch(error => {
            // Handle any errors
            console.error('Error uploading image:', error);
        });


}

//call uploadCanvas when k is pressed
document.addEventListener('keydown', function (event) {
    if (event.keyCode == 75) {
        console.log("hi");
        uploadCanvas();
    }
});

//count down timer from 60 to 0
var timeleft = 60;
var downloadTimer = setInterval(function () {
    if (timeleft <= 0) {
        clearInterval(downloadTimer);
        document.getElementById("countdown").innerHTML = "Finished";
        uploadCanvas();
        //disable canvas
        var canvas = document.getElementById("myCanvas");
        canvas.style.pointerEvents = 'none';
    } else {
        document.getElementById("countdown").innerHTML = timeleft + " seconds remaining";
    }
    timeleft -= 1;
}, 1000);

