var map = new BMap.Map("container");
// 创建地图实例
var point = new BMap.Point(117.16255,38.891118);
// 创建点坐标
map.centerAndZoom(point, 18);


//设置地图风格
map.setMapStyleV2({
    styleId: 'e2b0fb96c0350da28d86ce2ed812c257'
});

map.disableDragging();     //禁止拖拽
map.disableScrollWheelZoom();//禁止缩放
map.disableDoubleClickZoom(); //禁止双击放大

//标注贩卖机的位置
// var marker = new BMap.Marker(point);  // 创建标注
// map.addOverlay(marker);              // 将标注添加到地图中
// var opts = {
//     width : 200,     // 信息窗口宽度
//     height: 100,     // 信息窗口高度
//     title : "1号贩卖机" , // 信息窗口标题
//     enableMessage:true,//设置允许信息窗发送短息
//     message:"杜蕾斯"
// }
// var infoWindow = new BMap.InfoWindow("剩余杜蕾斯为0", opts);  // 创建信息窗口对象
// marker.addEventListener("click", function(){
//     map.openInfoWindow(infoWindow,point); //开启信息窗口
// });

var data_info = [
    // [117.165202,38.890109,"1号贩卖机"],
    [117.163938,38.888205,"2号贩卖机"],
    [117.160718,38.892154,"3号贩卖机"]
];
var opts = {
    width : 250,     // 信息窗口宽度
    height: 80,     // 信息窗口高度
    title : "饮料机" , // 信息窗口标题
    enableMessage:true//设置允许信息窗发送短息
};
for(var i=0;i<data_info.length;i++){
    var marker = new BMap.Marker(new BMap.Point(data_info[i][0],data_info[i][1]));  // 创建标注
    var content = data_info[i][2];
    map.addOverlay(marker);               // 将标注添加到地图中
    addClickHandler(content,marker);
}
function addClickHandler(content,marker){
    marker.addEventListener("click",function(e){
        openInfo(content,e)}
    );
}
function openInfo(content,e){
    var p = e.target;
    var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
    var infoWindow = new BMap.InfoWindow(content,opts);  // 创建信息窗口对象
    map.openInfoWindow(infoWindow,point); //开启信息窗口
}



// map.centerAndZoom(new BMap.Point(117.16255,38.891118), 18);//学校的坐标，放大的倍数
//
// map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
// //增加滚轮放大功能
// setTimeout(function(){
//     map.setZoom(14);
// }, 2000);  //2秒后放大到14级
// map.enableScrollWheelZoom(true);
//
// var  mapStyle ={
//     features: ["road", "building","water","land"],//隐藏地图上的poi
//     style : "midnight"  //设置地图风格为高端黑
// }
// map.setMapStyle(mapStyle);
//
// //设置地图显示范围
// var b = new BMap.Bounds(new BMap.Point(116.027143, 39.772348),new BMap.Point(116.832025, 40.126349));
// try {
//     BMapLib.AreaRestriction.setBounds(map, b);
// } catch (e) {
//     alert(e);
// }
//
// function checkhHtml5()
// {
//     if (typeof(Worker) === "undefined")
//     {
//         if(navigator.userAgent.indexOf("MSIE 9.0")<=0)
//         {
//             alert("定制个性地图示例：IE9以下不兼容，推荐使用百度浏览器、chrome、firefox、safari、IE10");
//         }
//
//     }
// }
// checkhHtml5();