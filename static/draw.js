var isDrawing = false;
var socket = io.connect();
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
        var padding = screenWidth * 0.01;
        const canvasSizeW = screenWidth - 2 * padding;
        const screenHeight = window.innerHeight;
        var padding = screenHeight * 0.25;
        const canvasSizeH = screenHeight - 2 * padding;
        var canvasSize = Math.min(canvasSizeH, canvasSizeW);
        if (screenHeight > screenWidth) {
            canvasSize = canvasSizeW;
        }

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
        if (e.type.startsWith('touch')) {
            var touch = e.touches[0];
            var rect = canvas.getBoundingClientRect();
            offsetX = touch.clientX - rect.left;
            offsetY = touch.clientY - rect.top;
        } else {
            offsetX = e.offsetX;
            offsetY = e.offsetY;
        }
        context.beginPath();
        context.moveTo(lastX, lastY);
        context.lineTo(offsetX, offsetY);
        context.stroke();

        lastX = offsetX;
        lastY = offsetY;
    }

    // Prevent scrolling while touching the canvas
    document.addEventListener('touchmove', function (e) {
        if (e.target === canvas) {
            e.preventDefault();
        }
    }, {passive: false});
// Event listeners for touchscreen devices
    canvas.addEventListener('touchstart', (e) => {
        isDrawing = true;
        var touch = e.touches[0];
        lastX = touch.pageX - canvas.offsetLeft;
        lastY = touch.pageY - canvas.offsetTop;
    });

    canvas.addEventListener('touchmove', draw);
    canvas.addEventListener('touchend', () => (isDrawing = false));
    canvas.addEventListener('touchcancel', () => (isDrawing = false));
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
var timeleft = 10;
var downloadTimer = setInterval(function () {
    if (timeleft == 0) {
        document.getElementById("countdown").innerHTML = "Finished";
        uploadCanvas();
        //disable canvas
        var canvas = document.getElementById("myCanvas");
        canvas.style.pointerEvents = 'none';
    } else if (timeleft <= -1) {
        //make all cards clickable
        makeCardsClickable();
        replaceCanvasItemsWithImage();
        getCardTitle();
        clearInterval(downloadTimer);
        console.log("hi");
    } else if (timeleft > 0) {
        document.getElementById("countdown").innerHTML = timeleft + " seconds remaining";
    }
    timeleft -= 1;
}, 1000);


function getCardTitle() {
    //get the card title from a request to the server using a get request to /getCardTitle
    fetch('/getCardTitle', {
        method: 'GET'
    })
        .then(response => {
            // Handle the server response
            console.log('Card title received successfully');
            return response.text(); // Convert response to text
        })
        .then(data => {
            // Process the response data
            console.log(data); // Log the response data
            var title = document.createElement("h4");
            title.style.textAlign = "center";
            title.innerText = data; // Set the response data as the title text
            document.body.prepend(title);
        })
        .catch(error => {
            // Handle any errors
            console.error('Error receiving card title:', error);
        });

}

function makeCardsClickable() {
    //make all cards clickable
    var iframe = document.getElementById("card-iframe");
    var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
    var cards = innerDoc.getElementsByClassName("card");
    for (var i = 0; i < cards.length; i++) {
        //make the card #00ff00 when clicked, or #e3cc99 if it is already green
        cards[i].addEventListener("click", function () {
            if (this.style.backgroundColor != "rgb(0, 255, 0)") {
                this.style.backgroundColor = "#00ff00";
            } else {
                this.style.backgroundColor = "#e3cc99";
            }
        });
    }
}

function replaceCanvasItemsWithImage() {
    var canvasItems = document.getElementById("canvas-items").children;
    //remove all canvas items
    while (canvasItems.length > 0) {
        canvasItems[0].remove();
    }
    //add the image
    var image = document.createElement("img");
    image.src = "/getImage";
    //apply the formatting from the canvas to the image
    var padding = 0.05 * window.innerWidth;
    var imageSizeW = window.innerWidth - 2 * padding;
    var padding = 0.25 * window.innerHeight;
    var imageSizeH = window.innerHeight - 2 * padding;
    var imageSize = Math.min(imageSizeH, imageSizeW);
    image.style.width = imageSize + "px";
    image.style.height = imageSize + "px";
    //create a new bootstrap div to hold the image and center it
    var newDiv = document.createElement("div");
    newDiv.className = "d-flex justify-content-center";
    newDiv.appendChild(image);
    //add the div to the canvas
    document.getElementById("canvas-items").appendChild(newDiv);

    //make the submit button visible
    document.getElementById("submit-btn").style.visibility = "visible";


}

function submitCards() {
    //count the number of green cards
    var iframe = document.getElementById("card-iframe");
    var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
    var cards = innerDoc.getElementsByClassName("card");
    var greenCards = 0;
    for (var i = 0; i < cards.length; i++) {
        if (cards[i].style.backgroundColor == "rgb(0, 255, 0)") {
            greenCards++;
        }
    }
    //send the number of green cards to the server
    fetch('/submitCard', {
            method: 'POST',
            body: JSON.stringify({numCards: greenCards}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    );
    //disable the submit button
    document.getElementById("submit-btn").disabled = true;
    //rename the submit button to "waiting for other players to score"
    document.getElementById("submit-btn").innerText = "Waiting for other players to score";

}

socket.on('displayLeaderboard', function (data) {
    //redirect to leaderboard
    window.location.href = "/leaderboard";
});
