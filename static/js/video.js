//获得video摄像头区域
let video = document.getElementById("video");

function getMedia() {
    let constraints = {
        video: {
            width: 500,
            height: 500
        },
        audio: true
    };
    /*
    这里介绍新的方法:H5新媒体接口 navigator.mediaDevices.getUserMedia()
    这个方法会提示用户是否允许媒体输入,(媒体输入主要包括相机,视频采集设备,屏幕共享服务,麦克风,A/D转换器等)
    返回的是一个Promise对象。
    如果用户同意使用权限,则会将 MediaStream对象作为resolve()的参数传给then()
    如果用户拒绝使用权限,或者请求的媒体资源不可用,则会将 PermissionDeniedError作为reject()的参数传给catch()
    */
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function(MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    }).catch(function(PermissionDeniedError) {
        console.log(PermissionDeniedError);
    })
}
getMedia();

