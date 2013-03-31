msie = navigator.appVersion.indexOf("MSIE") != -1;
ns4  = !msie && document.layers;

function layerSupport() {
    return document.all || document.layers || document.getElementById;
}

layers = new Array();
layerX = new Array();
layerY = new Array();
cursorX = 0;
cursorY = 0;

function getViewWidth() {
  if (!ns4)
    return document.body.clientWidth;
  else
    return window.innerWidth;
}

function getViewHeight() {
  if (!ns4)
    return document.body.clientHeight;
  else
    return window.innerHeight;
}

function getViewXOffset() {
  if (msie)
    return document.body.scrollLeft;
  else
    return window.pageXOffset;
}

function getViewYOffset() {
  if (msie)
    return document.body.scrollTop;
  else
    return window.pageYOffset;
}

function getLayerX(i) {
    return layerX[i];
}

function getLayerY(i) {
    return layerY[i];
}

function moveLayer(i, x, y) {
  layerX[i] = x;
  layerY[i] = y;
  if (msie) {
    layers[i].style.pixelLeft = x;
    layers[i].style.pixelTop = y;
  }
  else if (ns4) {
    layers[i].left = x;
    layers[i].top = y;
  }
  else {
    layers[i].style.left = x + "px";
    layers[i].style.top = y + "px";
  }
}


function outOfBounds(config, x, y, w, h) {
  var result = 0;
  
  // note that fudge factor isn't used for bottom
  if (x < getViewXOffset() - config.xFudge)
    result |= 1; // Left
  else if (x + w >= getViewXOffset() + getViewWidth() + config.xFudge)
    result |= 2; // Right
  
  if (y + h >= getViewYOffset() + getViewHeight())
    result |= 4; // Bottom
  else if (y < getViewYOffset() - config.yFudge)
    result |= 8; // Top
    
  return result;
}

function random(bound) {
  return Math.floor(Math.random() * bound);
}

function randomX(config) {
  return getViewXOffset() + random(getViewWidth() - config.imageWidth);
}

function randomY(config) {
  return getViewYOffset() - config.yFudge + random(getViewHeight() + config.yFudge - config.imageHeight);
}

function setVisible(i, show) {
   if (!ns4)
      layers[i].style.visibility = show ? "" : "hidden";
   else
      layers[i].visibility = show ? "show" : "hide";
}

function writeLayer(layercontents, name, x, y) {
    layerX[name] = x;
    layerY[name] = y;
    if (!ns4) {
      document.writeln('<div id="' + name + '" style="position:absolute;left:' + x + ';top:' + y + ';">' + layercontents + '</div>');
      if (msie)
        layers[name] = document.all[name];
      else
        layers[name] = document.getElementById(name);
    }
    else {
      document.writeln('<layer id="' + name + '" left=' + x + ' top=' + y + '>' + layercontents + '</layer>');
      layers[name] = document.layers[name];
    }
}

function writeImage(image, name, x, y) {
    layerX[name] = x;
    layerY[name] = y;
    if (!ns4) {
      document.writeln('<div id="' + name + '" style="position:absolute;left:' + x + ';top:' + y + ';"><img src="' + image + '"></div>');
      if (msie)
        layers[name] = document.all[name];
      else
        layers[name] = document.getElementById(name);
    }
    else {
      document.writeln('<layer id="' + name + '" left=' + x + ' top=' + y + '><img src="' + image + '"></layer>');
      layers[name] = document.layers[name];
    }
}

function writeImages(config) {
  for (var i = 0; i < config.imageCount; i++) {
    var startX = randomX(config);
    var startY = config.startOnScreen ? randomY(config) : -config.imageHeight;
    var name = config.prefix + i;
    writeImage(config.image, name, startX, startY);
  }
}

function cursorXY(e) {
  cursorX = msie ? (getViewXOffset() + event.clientX) : e.pageX;
  cursorY = msie ? (getViewYOffset() + event.clientY) : e.pageY;
}

function captureXY() {
  if (!msie) { document.captureEvents(Event.MOUSEMOVE); }
  document.onmousemove = cursorXY;
}

function config() {
  this.xFudge = 0;
  this.yFudge = 0;
  this.updateInterval = 50;
  this.startOnScreen = true;
  this.imageCount = 1;
}