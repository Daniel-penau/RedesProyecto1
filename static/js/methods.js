
async function imagesToVideo() {
    var fileList = document.getElementById("images_to_video").files;
    if (fileList.length < 1) {
        alert("Es necesario ingresar al menos 1 archivo");
    } else {
        let formData = new FormData();
        for (let i = 0; i < fileList.length; i++) {
            formData.append("files", fileList[i]);
        }
        const ctrl = new AbortController()    // timeout
        setTimeout(() => ctrl.abort(), 5000);

        await fetch('methods/images_to_video',
            {method: "POST", body: formData, signal: ctrl.signal}
        ).then(function(response){
            alert("AAAAAAAAAAAAAAAAAAAA");
        });

    }
}

function extractAudio() {
    var fileList = document.getElementById("video_to_audio").files;
    if (fileList.length < 1) {
        alert("Es necesario ingresar al menos 1 archivo");
    } else if (fileList.length > 1) {
        alert("Solo puedes ingresar 1 archivo")
    } else {
        try {
            let formData = new FormData();
            formData.append("files", fileList[0]);
            //await
            fetch('methods/extract_audio',
                {method: "POST", body: formData})
                .then(resp => resp.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'result.mp3'
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert("Completado")
                })
        } catch (e) {
            console.log(e)
        }
    }
}

function resizeVideo() {
    var fileList = document.getElementById("video_resize").files;
    var videoWidth = document.getElementById("video_width").value;
    var videoHeight = document.getElementById("video_height").value;

    if (fileList.length < 1) {
        alert("Es necesario ingresar al menos 1 archivo");
    } else if (fileList.length > 1) {
        alert("Solo puedes ingresar 1 archivo");
    } else if(videoWidth < 1){
        alert("El ancho debe ser mayor a 1");
    } else if(videoHeight < 1){
        alert("El alto debe ser mayor a 1")
    } else {
        try {
            let formData = new FormData();
            formData.append("files", fileList[0]);
            formData.append("width", videoWidth);
            formData.append("height", videoHeight);
            //await
            fetch('methods/resize_video',
                {method: "POST", body: formData})
                .then(resp => resp.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'result.mp4'
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert("Completado")
                })
        } catch (e) {
            console.log(e)
        }
    }
}

function trimVideo() {
    var fileList = document.getElementById("video_cut").files;
    var startFrame = document.getElementById("start_frame").value;
    var endFrame = document.getElementById("end_frame").value;

    if (fileList.length < 1) {
        alert("Es necesario ingresar al menos 1 archivo");
    } else if (fileList.length > 1) {
        alert("Solo puedes ingresar 1 archivo");
    } else if(startFrame < 0){
        alert("El frame de inicio debe ser mayor a 0");
    } else if(endFrame <= startFrame){
        alert("El frame final debe ser mayor al inicial")
    } else {
        try {
            let formData = new FormData();
            formData.append("files", fileList[0]);
            formData.append("start", startFrame);
            formData.append("end", endFrame);
            //await
            fetch('methods/trim_video',
                {method: "POST", body: formData})
                .then(resp => resp.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'result.mp4'
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert("Completado")
                })
        } catch (e) {
            console.log(e)
        }
    }
}

function extractFrames() {
    var fileList = document.getElementById("video_frame").files;
    if (fileList.length < 1) {
        alert("Es necesario ingresar al menos 1 archivo");
    } else if (fileList.length > 1) {
        alert("Solo puedes ingresar 1 archivo")
    } else {
        try {
            let formData = new FormData();
            formData.append("files", fileList[0]);
            //await
            fetch('methods/video_frames',
                {method: "POST", body: formData})
                .then(resp => resp.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'result.zip'
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert("Completado")
                })
        } catch (e) {
            console.log(e)
        }
    }
}


function sendResult(response){
    alert(response["link"]);
}